# Automation Hat Binary Sensor Integration

This enhancement adds binary sensor support to the Home Assistant Automation Hat custom component, enabling monitoring of the three digital inputs available on the Pimoroni Automation Hat.

## Features Added

### 1. Binary Sensor Platform (`binary_sensor.py`)
- **Three digital inputs**: Input 1, Input 2, and Input 3
- **Real-time monitoring**: Background polling of input states
- **Home Assistant integration**: Proper entity registration and device linking
- **Configurable device classes**: Each input can have different device classes (opening, motion, occupancy)
- **State change detection**: Only publishes updates when input states change

### 2. Enhanced Automation Hat Class (`automation_hat.py`)
- **Input state management**: Tracks current state of all digital inputs
- **Hardware interface**: Reads from actual Automation Hat hardware using the `automationhat` library
- **Background polling**: Continuous monitoring at 1-second intervals
- **Error handling**: Graceful handling of hardware read errors
- **Logging**: Comprehensive logging for debugging

### 3. Constants and Configuration (`const.py`)
```python
INPUT_NAMES = ["one", "two", "three"]

INPUT_DISPLAY_NAMES = {
    "one": "Digital Input 1",
    "two": "Digital Input 2", 
    "three": "Digital Input 3"
}

INPUT_DEVICE_CLASSES = {
    "one": "opening",     # For door/window sensors
    "two": "motion",      # For motion detectors
    "three": "occupancy"  # For occupancy sensors
}
```

### 4. Integration Updates (`__init__.py`)
- Added `Platform.BINARY_SENSOR` to platforms list
- Added cleanup for input polling on integration unload

## Hardware Mapping

The integration maps to the Automation Hat's digital inputs:
- **Input 1** (`ah.input.one`) → Binary Sensor "Digital Input 1"
- **Input 2** (`ah.input.two`) → Binary Sensor "Digital Input 2"  
- **Input 3** (`ah.input.three`) → Binary Sensor "Digital Input 3"

All inputs are 24V tolerant with the following characteristics:
- Switch on at: 3V
- Switch off at: 1V
- Protected by: 20kΩ resistor and 3.3V zener diode
- Current limit: ~1mA

## Usage

Once the integration is installed and configured, the binary sensors will automatically appear in Home Assistant:

- `binary_sensor.automation_hat_digital_input_1`
- `binary_sensor.automation_hat_digital_input_2`
- `binary_sensor.automation_hat_digital_input_3`

### Example Automations

```yaml
# Motion detection using Input 2
automation:
  - alias: "Motion Detected"
    trigger:
      - platform: state
        entity_id: binary_sensor.automation_hat_digital_input_2
        to: 'on'
    action:
      - service: light.turn_on
        target:
          entity_id: light.hallway_light

# Door sensor using Input 1
automation:
  - alias: "Door Opened"
    trigger:
      - platform: state
        entity_id: binary_sensor.automation_hat_digital_input_1
        to: 'on'
    action:
      - service: notify.mobile_app
        data:
          message: "Front door opened"
```

## File Structure

```
custom_components/automationhat/
├── __init__.py              # Integration setup, now includes binary sensors
├── automation_hat.py        # Enhanced with input monitoring
├── binary_sensor.py         # New binary sensor platform
├── const.py                 # Constants including input definitions
├── button.py               # Existing button platform
├── config_flow.py          # Existing configuration flow
├── light.py                # Existing light platform
├── manifest.json           # Integration manifest
├── strings.json            # UI strings
├── switch.py               # Existing switch platform
└── translations/           # Translation files
```

## Technical Implementation

### Background Polling
- Runs continuously at 1-second intervals
- Uses asyncio task for non-blocking operation
- Automatically starts when first binary sensor is added
- Stops when integration is unloaded

### State Management
- Internal state tracking prevents unnecessary updates
- Only publishes changes to Home Assistant when input states change
- Graceful error handling maintains last known state on hardware errors

### Hardware Access
- Uses the official `automationhat` Python library
- Threaded hardware access using `asyncio.to_thread()` 
- Proper hardware initialization with `ah.setup()`

### Entity Configuration
- Unique IDs: `{hat_id}_{input_name}_input`
- Device linking: All sensors linked to main Automation Hat device
- Device classes: Configurable per input for proper Home Assistant categorization
