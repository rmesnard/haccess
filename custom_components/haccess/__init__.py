from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
import voluptuous as vol
import logging

from .const import DOMAIN,HACCESS_TOPIC

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the haccess component."""

    _LOGGER.debug("Setting up haccess")
    topic = HACCESS_TOPIC
    entity_id = 'haccess.last_message'

    # Listen to a message on MQTT.
    @callback
    def message_received(topic: str, payload: str, qos: int) -> None:
        """A new MQTT message has been received."""
        _LOGGER.debug("A new MQTT message has been received")
        hass.states.async_set(entity_id, payload)

    await hass.components.mqtt.async_subscribe(topic, message_received)

    hass.states.async_set(entity_id, 'No messages')

    # Return boolean to indicate that initialization was successfully.
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True

async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of an entry.

    Args:
        hass: Home Assistant instance
        entry: Config entry being removed
    """
    # Clean up any resources if needed