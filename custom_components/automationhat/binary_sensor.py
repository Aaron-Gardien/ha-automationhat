"""Binary sensor platform for the Automation Hat integration."""

from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AHConfigEntry
from .const import DOMAIN, INPUT_NAMES, INPUT_DISPLAY_NAMES, INPUT_DEVICE_CLASSES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: AHConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Automation Hat binary sensor platform."""
    automation_hat = config_entry.runtime_data

    # Create binary sensors for the three digital inputs
    entities = [
        AutomationHatBinarySensor(automation_hat, input_name, INPUT_DISPLAY_NAMES[input_name], INPUT_DEVICE_CLASSES[input_name])
        for input_name in INPUT_NAMES
    ]

    async_add_entities(entities)


class AutomationHatBinarySensor(BinarySensorEntity):
    """Representation of an Automation Hat digital input as a binary sensor."""

    def __init__(self, automation_hat, input_number: str, name: str, device_class: str) -> None:
        """Initialize the binary sensor."""
        self._automation_hat = automation_hat
        self._input_number = input_number
        self._name = name
        self._attr_name = f"Automation Hat {name}"
        self._attr_unique_id = f"{automation_hat.hat_id}_{input_number}_input"
        self._attr_device_class = getattr(BinarySensorDeviceClass, device_class.upper())
        self._attr_is_on = False

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return self._automation_hat.device_info

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self._attr_is_on

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        _LOGGER.info("Adding binary sensor for input %s", self._input_number)
        self._automation_hat.register_callback(self.async_write_ha_state)
        
        # Start input polling when first sensor is added
        self._automation_hat.start_input_polling()
        
        # Initial state update
        await self._update_state()

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        await super().async_will_remove_from_hass()
        self._automation_hat.remove_callback(self.async_write_ha_state)

    async def _update_state(self) -> None:
        """Update the sensor state from the automation hat."""
        try:
            # Get the cached state from the automation hat, which is updated by polling
            state = self._automation_hat._input_state.get(self._input_number, False)
            self._attr_is_on = state
        except Exception:
            # Keep the last known state if we can't read from hardware
            pass

    async def async_update(self) -> None:
        """Update the binary sensor state."""
        await self._update_state()

    @callback
    def async_write_ha_state(self) -> None:
        """Write the state to Home Assistant."""
        self.hass.async_create_task(self._update_state())
        super().async_write_ha_state()
