"""SenseME Discovery.

This class periodically broadcasts discovery packets and listens for response messages
from SenseME devices by Big Ass Fans. Discovered devices are announced via callbacks.

Based on work from Bruce at http://bruce.pennypacker.org/tag/senseme-plugin/
and https://github.com/bpennypacker/SenseME-Indigo-Plugin

Based on work from TomFaulkner at https://github.com/TomFaulkner/SenseMe

Source can be found at https://github.com/mikelawrence/aiosenseme
"""
import asyncio
import inspect
import ipaddress
import logging
import random
import socket
import sys
import time
import traceback

import ifaddr

from .device import DEVICE_TYPES, IGNORE_MODELS, SensemeDevice, SensemeFan, SensemeLight

_LOGGER = logging.getLogger(__name__)

PORT = 31415

# the default windows event loop (ProactorEventLoop) does not support
# create_datagram_endpoint() needed by this module. Switching to the
# SelectorEventLoop fixes this problem but may have unintended consequences.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop()  # start the loop
    _LOGGER.debug("Changing event loop for Windows")


class SensemeDiscoveryEndpoint:
    """High-level endpoint for SenseME Discovery protocol."""

    # one receive queue for all endpoints
    receive_queue = asyncio.Queue()

    def __init__(self, ip: str = None):
        """Initialize Senseme Discovery Endpoint."""
        self.opened = False
        self.transport = None
        self.ip = ip

    def abort(self):
        """Close the transport immediately.

        Buffered write data will be lost.
        """
        self.opened = False
        if self.transport is None:
            return
        self.transport.abort()
        self.close()

    def close(self):
        """Close the transport gracefully.

        Buffered write data will be sent.
        """
        self.opened = False
        if self.transport is None:
            return
        self.receive_queue.put_nowait(None)  # tell receive() socket is closed
        if self.transport:
            self.transport.close()

    def is_closing(self) -> bool:
        """Return True if the endpoint is closed or closing."""
        if not self.opened:
            return True  # unopened connection is closed
        if self.transport is None:
            return True  # opened connection but no transport is closed
        return self.transport.is_closing()

    async def receive(self) -> SensemeDevice:
        """Wait for discovered device and return it.

        Return None when the socket is closed.
        This method is a coroutine.
        """
        while True:
            if self.receive_queue.empty() and self.transport.is_closing():
                return None
            rsp = await self.receive_queue.get()
            if rsp is None:
                return None
            msg = rsp[0]
            addr = rsp[1]
            if len(msg) > 200 or len(msg) < 31:
                continue
            if msg[0] != "(" or msg[-1] != ")":
                continue
            msg = msg[1:-1]
            msg_data = msg.split(";")
            if len(msg_data) != 5:
                continue
            if msg_data[4].upper() in IGNORE_MODELS:
                _LOGGER.debug("Ignored '%s' on %s", msg, self.ip)
                continue
            _LOGGER.debug("Received '%s' from %s on %s", msg, addr, self.ip)
            device_type = DEVICE_TYPES.get(msg_data[4], "FAN")
            if device_type == "FAN":
                device = SensemeFan(
                    name=msg_data[0], id=msg_data[3], ip=addr, model=msg_data[4]
                )
            elif device_type == "LIGHT":
                device = SensemeLight(
                    name=msg_data[0], id=msg_data[3], ip=addr, model=msg_data[4]
                )
            return device

    def send_broadcast(self):
        """Send the SenseME Discovery broadcast packet."""
        if not self.is_closing():
            data = "<ALL;DEVICE;ID;GET>".encode("utf-8")
            self.transport.sendto(data, ("<broadcast>", PORT))
            _LOGGER.debug("Discovery broadcast on %s", self.ip)


class SensemeDiscoveryProtocol(asyncio.DatagramProtocol):
    """Datagram protocol for SenseME Discovery."""

    def __init__(self, endpoint: SensemeDiscoveryEndpoint):
        """Initialize Senseme Discovery Protocol."""
        self._endpoint = endpoint

    # Protocol methods
    def connection_made(self, transport: asyncio.Protocol):
        """Socket connect on SenseME Discovery Protocol."""
        self._endpoint.transport = transport
        self._endpoint.opened = True
        _LOGGER.debug("Listening on %s", self._endpoint.ip)
        self._endpoint.send_broadcast()

    def connection_lost(self, exc):  # pylint: disable=unused-argument
        """Lost connection SenseME Discovery Protocol."""
        _LOGGER.debug("Listener closed on %s", self._endpoint.ip)
        self._endpoint.close()  # half-closed connections are not permitted

    # Datagram protocol methods
    def datagram_received(self, data: str, addr: str):
        """UDP packet received on SenseME Discovery Protocol."""
        if data:
            msg = data.decode("utf-8")
            try:
                self._endpoint.receive_queue.put_nowait((msg, addr[0]))
            except asyncio.QueueFull:
                _LOGGER.error("Receive queue full")

    def error_received(self, exc):
        """Error on SenseME Discovery Protocol."""
        _LOGGER.debug(
            "Protocol error on %s\n%s", self._endpoint.ip, traceback.format_exc()
        )
        self._endpoint.close()


class SensemeDiscovery:
    """SenseME Discovery Class.

    This class periodically broadcasts discovery packets and listens
    for response messages from SenseME devices by Big Ass Fans.
    """

    _devices = []  # all SensemeDiscovery objects use the same device list

    def __init__(self, start_first: bool = True, refresh_minutes: int = 5):
        """Initialize Senseme Discovery Protocol."""
        self.start_first = start_first
        self.refresh_minutes = refresh_minutes
        self._is_running = False
        self._callbacks = []
        self._broadcaster_task = None

    @property
    def devices(self):
        """Get the current list of discovered devices."""
        return self._devices

    def add_callback(self, callback):
        """Add callback function/coroutine.

        Called when parameters are updated.
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)
            if inspect.iscoroutinefunction(callback):
                asyncio.create_task(callback(self._devices.copy()))
                _LOGGER.debug("Added coroutine callback")
            else:
                callback(self._devices.copy())
                _LOGGER.debug("Added function callback")

    def remove_callback(self, callback):
        """Remove existing callback function/coroutine."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
            _LOGGER.debug("Removed callback")

    async def _create_endpoints(self):
        """Create an endpoint per interface and return as a list of endpoints."""
        endpoints = []
        loop = asyncio.get_running_loop()
        listening = 0
        for adapter in ifaddr.get_adapters():
            for ip in adapter.ips:
                if ip.is_IPv4 and not ipaddress.ip_address(ip.ip).is_loopback:
                    # _LOGGER.debug("Found IPv4 %s", ip.ip)
                    try:
                        endpoint = SensemeDiscoveryEndpoint(ip.ip)
                        await loop.create_datagram_endpoint(
                            lambda ep=endpoint: SensemeDiscoveryProtocol(ep),
                            local_addr=(ip.ip, PORT),
                            family=socket.AF_INET,
                            allow_broadcast=True,
                        )
                        endpoints.append(endpoint)
                        listening += 1
                    except OSError:
                        last_error = (
                            f"Create datagram endpoint error on {ip.ip}\n"
                            f"{traceback.format_exc()}"
                        )
                        _LOGGER.debug(last_error)
        if listening == 0:
            # failed to bind to any address
            _LOGGER.error(
                "Failed to listen for discovery responses on any address. "
                "Last error\n%s",
                last_error,
            )

        return endpoints

    async def _broadcaster(self):
        """Periodically broadcast discovery packet.

        If the underlying socket has an error this task will exit.
        This method is a coroutine.
        """
        self._is_running = True
        device = None
        while True:
            try:
                endpoints = await self._create_endpoints()
                start = time.time()
                while True:
                    try:
                        device = await asyncio.wait_for(endpoints[0].receive(), 1)
                    except asyncio.TimeoutError:
                        device = None
                        if time.time() - start < 5:
                            for endpoint in endpoints:
                                endpoint.send_broadcast()
                        else:
                            for endpoint in endpoints:
                                endpoint.abort()
                            endpoints = []
                            break
                    if device is not None:
                        if device not in self._devices:
                            if self.start_first:
                                if await device.update():
                                    self._devices.append(device)
                                    _LOGGER.debug("Discovered %s", device)
                                else:
                                    _LOGGER.debug("Failed to start %s", device.name)
                            else:
                                if await device.fill_out_sec_info():
                                    self._devices.append(device)
                                    _LOGGER.debug("Discovered %s", device)
                                else:
                                    _LOGGER.debug(
                                        "Failed to retrieve secondary info for %s",
                                        device.name,
                                    )
                        for callback in self._callbacks:
                            if inspect.iscoroutinefunction(callback):
                                asyncio.create_task(callback(self._devices.copy()))
                            else:
                                callback(self._devices.copy())
                await asyncio.sleep(1)
                wait = self.refresh_minutes * 60 + random.uniform(-10, 10)
                _LOGGER.debug("Currently %s known senseme devices", len(self._devices))
                _LOGGER.debug("Discovery waiting for %s seconds", int(wait))
                await asyncio.sleep(wait)
            except asyncio.CancelledError:
                _LOGGER.debug("Broadcaster task cancelled")
                return
            except Exception:
                _LOGGER.error("Broadcaster task error\n%s", traceback.format_exc())
                raise
            finally:
                for endpoint in endpoints:
                    endpoint.abort()
                endpoints = None
        _LOGGER.error("Broadcaster task ended")

    def start(self):
        """Start broadcaster task.

        Will maintain a list of discovered devices.
        """
        if not self._is_running:
            self._broadcaster_task = asyncio.create_task(self._broadcaster())

    def stop(self):
        """Stop broadcaster task.

        Any discovered devices will remain in memory and will continue to update.
        """
        if self._is_running is True:
            self._broadcaster_task.cancel()
            self._is_running = False

    def remove_discovered_devices(self):
        """Stop broadcaster task.

        Any discovered devices will be stopped and removed from memory.
        """
        self.stop()
        for device in self._devices:
            device.stop()
        self._devices = []


async def discover_any(timeout_seconds=5) -> bool:
    """Return True if any SenseME devices are found on the network.

    This function will always take timeout_seconds to complete.
    This method is a coroutine.
    """
    discovery = SensemeDiscovery(True, 1)
    discovery.start()
    await asyncio.sleep(timeout_seconds)
    count = len(discovery.devices)
    discovery.stop()
    _LOGGER.debug("Discovered %s device%s", count, "" if count == 1 else "s")
    return count > 0


async def discover(value, timeout_seconds=5) -> SensemeDevice:
    """Discover a device with a name, room name or IP Address.

    None is returned if the device was not found.
    This function will take up timeout_seconds to complete.
    This method is a coroutine.
    """
    start = time.time()
    discovery = SensemeDiscovery(False, 1)
    try:
        discovery.start()
        while True:
            await asyncio.sleep(0.1)
            devices = discovery.devices.copy()
            for device in devices:
                if device == value:
                    await device.fill_out_sec_info()
                    device.start()
                    await device.update()
                    return device
            if time.time() - start > timeout_seconds:
                return None
    finally:
        discovery.stop()
