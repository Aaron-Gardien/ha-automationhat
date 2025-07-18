from __future__ import annotations

import asyncio
from asyncio import to_thread
import random
from typing import Callable
import logging

from homeassistant.core import HomeAssistant

import automationhat as ah

from .const import DOMAIN, INPUT_NAMES

# Polling interval for inputs in seconds
INPUT_POLL_INTERVAL = 1.0

_LOGGER = logging.getLogger(__name__)


class AutomationHat:

    def __init__(self, hass: HomeAssistant, data: dict) -> None:
        """Init AutomationHat roller."""
        self._id = "automationhat"
        self._name = "Automation Hat"
        self._model = "PIM213"
        self._manufacturer = "Pimoroni"
        self._online = True
        self._data = data

        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        self._polling_task = None

        self._relay_state = {
            "one": False,
            "two": False,
            "three": False
        }

        self._light_state = {
            "power": False,
            "comm": False,
            "warn": False
        }

        self._input_state = {input_name: False for input_name in INPUT_NAMES}

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._id)},
            "name": self._name,
            "manufacturer": self._manufacturer,
            "model": self._model,
        }

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @property
    def online(self) -> str:
        return self._online

    @property
    def model(self) -> str:
        return self._model

    @property
    def name(self) -> str:
        return self._name

    @property
    def data(self) -> dict:
        return self._data

    @property
    def hat_id(self) -> str:
        """Return ID for roller."""

        return self._id

    async def test_hat(self) -> bool:
        try:
            await to_thread(ah.setup)
        except Exception:
            return False
        return True

    async def set_relay_on(self, number) -> None:
        self._relay_state[number] = True
        await self.publish_updates()

    async def get_relay_state(self, number) -> bool:
        return self._relay_state[number]

    async def set_relay_off(self, number) -> None:
        """Publish updates, with a random delay to emulate interaction with device."""
        self._relay_state[number] = False
        await self.publish_updates()

    async def set_light_on(self, number) -> None:
        self._light_state[number] = True
        await self.publish_updates()

    async def get_light_state(self, number) -> bool:
        return self._light_state[number]

    async def set_light_off(self, number) -> None:
        """Publish updates, with a random delay to emulate interaction with device."""
        self._light_state[number] = False
        await self.publish_updates()

    async def get_input_state(self, number) -> bool:
        """Get the current state of a digital input."""
        try:
            await to_thread(ah.setup)
            # Use the automation hat library to read the actual input state
            if number == "one":
                state = await to_thread(ah.input.one.read)
            elif number == "two":
                state = await to_thread(ah.input.two.read) 
            elif number == "three":
                state = await to_thread(ah.input.three.read)
            else:
                _LOGGER.warning("Unknown input number: %s", number)
                return False
            
            # Update internal state and publish if changed
            if self._input_state[number] != state:
                _LOGGER.debug("Input %s changed from %s to %s", number, self._input_state[number], state)
                self._input_state[number] = state
                await self.publish_updates()
            
            return state
        except Exception as e:
            _LOGGER.error("Error reading input %s: %s", number, e)
            return self._input_state[number]

    async def update_input_states(self) -> None:
        """Update all input states from the hardware."""
        for input_name in INPUT_NAMES:
            await self.get_input_state(input_name)

    async def _input_polling_loop(self) -> None:
        """Background task to continuously poll input states."""
        _LOGGER.info("Starting input polling loop")
        while True:
            try:
                await self.update_input_states()
                await asyncio.sleep(INPUT_POLL_INTERVAL)
            except asyncio.CancelledError:
                _LOGGER.info("Input polling loop cancelled")
                break
            except Exception as e:
                _LOGGER.error("Error in input polling loop: %s", e)
                await asyncio.sleep(INPUT_POLL_INTERVAL)

    def start_input_polling(self) -> None:
        """Start the input polling background task."""
        if self._polling_task is None or self._polling_task.done():
            _LOGGER.info("Starting input polling")
            self._polling_task = asyncio.create_task(self._input_polling_loop())

    def stop_input_polling(self) -> None:
        """Stop the input polling background task."""
        if self._polling_task and not self._polling_task.done():
            _LOGGER.info("Stopping input polling")
            self._polling_task.cancel()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    async def publish_updates(self) -> None:
        """Schedule call all registered callbacks."""
        for callback in self._callbacks:
            callback()

    @property
    def online(self) -> float:
        """Automation hat is online."""
        return True
