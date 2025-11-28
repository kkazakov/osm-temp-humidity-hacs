# OpenSenseMap Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A custom Home Assistant integration to display sensor data from [OpenSenseMap](https://opensensemap.org/) sensors.

## Features

- Support for temperature, humidity, pressure, PM2.5, PM10, and other sensors
- Automatic updates every 5 minutes
- Configuration via UI
- Proper device classes and units of measurement
- Additional sensor attributes (sensor ID, last measurement time)

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/kkazakov/osm-temp-humidity-hacs`
6. Select category: "Integration"
7. Click "Add"
8. Find "OpenSenseMap Sensors" in the list and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/opensensemap` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
### Local Testing

For local development and testing without GitHub:

1. Locate your Home Assistant configuration directory (where `configuration.yaml` is located)
2. Create a `custom_components` directory if it doesn't exist
3. Copy the entire `custom_components/opensensemap` directory from this project into your Home Assistant's `custom_components` directory
4. The structure should look like:
   ```
   config/
   ├── configuration.yaml
   └── custom_components/
       └── opensensemap/
           ├── __init__.py
           ├── sensor.py
           ├── config_flow.py
           ├── manifest.json
           ├── strings.json
           └── translations/
               └── en.json
   ```
5. Restart Home Assistant
6. Go to Settings → Devices & Services → Add Integration
7. Search for "OpenSenseMap Sensors" and configure it

For development with auto-reload:
- Enable debug logging in `configuration.yaml`:
  ```yaml
  logger:
    default: info
    logs:
      custom_components.opensensemap: debug
  ```
- Check logs in Settings → System → Logs


## Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "OpenSenseMap"
4. Enter your Sensor Box ID (found in the URL at https://opensensemap.org/explore/YOUR_BOX_ID)
5. Click "Submit"

## Finding Your Sensor Box ID

1. Visit [OpenSenseMap](https://opensensemap.org/)
2. Browse or search for your sensor
3. Click on the sensor to open its details
4. Copy the Box ID from the URL (e.g., `https://opensensemap.org/explore/5a1b2c3d4e5f6a7b8c9d0e1f`)
5. The Box ID is: `5a1b2c3d4e5f6a7b8c9d0e1f`

## Supported Sensor Types

The integration automatically detects and configures sensor types including:

- Temperature (°C)
- Humidity (%)
- Pressure (hPa)
- PM2.5 (µg/m³)
- PM10 (µg/m³)

All other sensor types from your OpenSenseMap box are also imported with their respective units.

## Usage Example

Once configured, sensors will appear as entities in Home Assistant. You can:

- Add them to your dashboard
- Use them in automations
- View historical data
- Create alerts based on sensor values

Example automation:
```yaml
automation:
  - alias: "High Temperature Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.opensensemap_temperature
        above: 30
    action:
      - service: notify.mobile_app
        data:
          message: "Temperature is above 30°C!"
```

## Troubleshooting

### Sensor Not Found

- Verify the Box ID is correct
- Ensure the sensor is public and active on OpenSenseMap
- Check your internet connection

### No Data

- Some sensors may not have recent measurements
- Check the OpenSenseMap website to verify the sensor is reporting data

### API Errors

- The integration polls the OpenSenseMap API every 5 minutes
- If you experience rate limiting, this is normal and the integration will retry

## Contributing

Contributions are welcome. Submit a Pull Request for review.

## License

MIT License

## Support

For issues, open a ticket on [GitHub](https://github.com/kkazakov/osm-temp-humidity-hacs/issues).