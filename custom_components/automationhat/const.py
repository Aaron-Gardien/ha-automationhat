"""Constants for the Detailed Hello World Push integration."""

# This is the internal name of the integration, it should also match the directory
# name for the integration.
DOMAIN = "automationhat"

# Digital input names
INPUT_NAMES = ["one", "two", "three"]

# Input display names
INPUT_DISPLAY_NAMES = {
    "one": "Input 1",
    "two": "Input 2", 
    "three": "Input 3"
}

# Input device classes (can be customized per input)
INPUT_DEVICE_CLASSES = {
    "one": "opening",
    "two": "opening",
    "three": "opening"
}
