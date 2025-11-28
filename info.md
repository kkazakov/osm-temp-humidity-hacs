# OpenSenseMap Integration

Integrate OpenSenseMap sensors into Home Assistant.

## Features

- Temperature sensors
- Humidity sensors
- Pressure sensors
- PM2.5 and PM10 air quality sensors
- Automatic updates every 5 minutes
- Configuration through UI
- Proper device classes and units

## Quick Start

1. Install via HACS
2. Restart Home Assistant
3. Go to Settings → Devices & Services
4. Click "Add Integration" and search for "OpenSenseMap"
5. Enter your Sensor Box ID from OpenSenseMap.org

## Finding Your Box ID

Visit OpenSenseMap.org, find your sensor, and copy the Box ID from the URL:
```
https://opensensemap.org/explore/YOUR_BOX_ID_HERE
```

## Support

For issues, open a ticket on [GitHub](https://github.com/kkazakov/osm-temp-humidity-hacs/issues).