"""Config flow for OpenSenseMap integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

DOMAIN = "opensensemap_sensors"
API_BASE_URL = "https://api.opensensemap.org"

CONF_SENSOR_ID = "sensor_id"


class OpenSenseMapConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            sensor_id = user_input[CONF_SENSOR_ID]
            
            session = async_get_clientsession(self.hass)
            try:
                url = f"{API_BASE_URL}/boxes/{sensor_id}"
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        name = data.get("name", f"OpenSenseMap {sensor_id}")
                        
                        await self.async_set_unique_id(sensor_id)
                        self._abort_if_unique_id_configured()
                        
                        return self.async_create_entry(
                            title=name,
                            data={
                                CONF_SENSOR_ID: sensor_id,
                                CONF_NAME: name,
                            },
                        )
                    elif response.status == 404:
                        errors["base"] = "sensor_not_found"
                    else:
                        errors["base"] = "cannot_connect"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SENSOR_ID): str,
                }
            ),
            errors=errors,
        )