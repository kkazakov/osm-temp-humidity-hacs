"""Support for OpenSenseMap sensors."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfPressure,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)
API_BASE_URL = "https://api.opensensemap.org"

SENSOR_TYPES = {
    "temperature": {
        "device_class": SensorDeviceClass.TEMPERATURE,
        "unit": UnitOfTemperature.CELSIUS,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "humidity": {
        "device_class": SensorDeviceClass.HUMIDITY,
        "unit": PERCENTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "pressure": {
        "device_class": SensorDeviceClass.PRESSURE,
        "unit": UnitOfPressure.HPA,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "pm2.5": {
        "device_class": SensorDeviceClass.PM25,
        "unit": "µg/m³",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "pm10": {
        "device_class": SensorDeviceClass.PM10,
        "unit": "µg/m³",
        "state_class": SensorStateClass.MEASUREMENT,
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    sensor_id = entry.data["sensor_id"]
    session = hass.data["opensensemap_sensors"][entry.entry_id]["session"]

    coordinator = OpenSenseMapDataUpdateCoordinator(
        hass,
        session,
        sensor_id,
    )

    await coordinator.async_config_entry_first_refresh()

    entities = []
    if coordinator.data:
        for sensor_data in coordinator.data.get("sensors", []):
            entities.append(
                OpenSenseMapSensor(
                    coordinator,
                    sensor_id,
                    sensor_data,
                )
            )

    async_add_entities(entities)


class OpenSenseMapDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        sensor_id: str,
    ) -> None:
        self.sensor_id = sensor_id
        self.session = session

        super().__init__(
            hass,
            _LOGGER,
            name="OpenSenseMap",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            url = f"{API_BASE_URL}/boxes/{self.sensor_id}"
            async with self.session.get(url, timeout=10) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error fetching data: {response.status}")
                data = await response.json()
                return data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err


class OpenSenseMapSensor(CoordinatorEntity, SensorEntity):

    def __init__(
        self,
        coordinator: OpenSenseMapDataUpdateCoordinator,
        box_id: str,
        sensor_data: dict[str, Any],
    ) -> None:
        super().__init__(coordinator)
        self._box_id = box_id
        self._sensor_id = sensor_data["_id"]
        self._phenomenon = sensor_data.get("title", "").lower()
        self._attr_name = f"OpenSenseMap {sensor_data.get('title', 'Sensor')}"
        self._attr_unique_id = f"opensensemap_sensors_{box_id}_{self._sensor_id}"
        
        sensor_config = SENSOR_TYPES.get(self._phenomenon, {})
        self._attr_device_class = sensor_config.get("device_class")
        self._attr_native_unit_of_measurement = sensor_data.get("unit") or sensor_config.get("unit")
        self._attr_state_class = sensor_config.get("state_class")

    @property
    def native_value(self) -> float | None:
        if not self.coordinator.data:
            return None
        
        for sensor in self.coordinator.data.get("sensors", []):
            if sensor["_id"] == self._sensor_id:
                if "lastMeasurement" in sensor and sensor["lastMeasurement"]:
                    try:
                        return float(sensor["lastMeasurement"]["value"])
                    except (ValueError, KeyError, TypeError):
                        return None
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        if not self.coordinator.data:
            return {}
        
        for sensor in self.coordinator.data.get("sensors", []):
            if sensor["_id"] == self._sensor_id:
                attrs = {
                    "sensor_id": self._sensor_id,
                    "box_id": self._box_id,
                    "phenomenon": self._phenomenon,
                }
                if "lastMeasurement" in sensor and sensor["lastMeasurement"]:
                    attrs["last_measurement_at"] = sensor["lastMeasurement"].get("createdAt")
                return attrs
        return {}

    @property
    def device_info(self) -> dict[str, Any]:
        return {
            "identifiers": {("opensensemap_sensors", self._box_id)},
            "name": self.coordinator.data.get("name", "OpenSenseMap Sensor"),
            "manufacturer": "OpenSenseMap",
            "model": self.coordinator.data.get("model", "SenseBox"),
        }