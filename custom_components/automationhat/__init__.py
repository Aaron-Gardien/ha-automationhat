"""The Detailed Hello World Push integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .automation_hat import AutomationHat

if TYPE_CHECKING:
    from typing import TypeAlias

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.SWITCH,
    Platform.LIGHT]

# Type alias for config entry
AHConfigEntry: TypeAlias = ConfigEntry[AutomationHat]


async def async_setup_entry(hass: HomeAssistant, entry: AHConfigEntry) -> bool:
    entry.runtime_data = AutomationHat(hass, entry.data)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Stop input polling
    if hasattr(entry, 'runtime_data') and entry.runtime_data:
        entry.runtime_data.stop_input_polling()
    
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok
