# Home Assistant + Node-RED Gate Control Setup

This guide will help you integrate your Automation HAT with Home Assistant and Node-RED to control a gate via HTTP commands.

---

## Prerequisites

- Home Assistant OS (Raspberry Pi or other supported device)
- Automation HAT installed and connected to the Pi

---

## 1. Install Required Add-ons

- **SSH/Terminal Add-on**:  
  Install from the Add-on Store for command-line access.

- **Node-RED Add-on**:  
  Install from the Add-on Store for visual automation.

- **HACS (Home Assistant Community Store)**:  
  [HACS Installation Guide](https://hacs.xyz/docs/setup/download)

---

## 2. Enable I2C Support

- Enable I2C on your device using the [HassOS I2C Configurator](https://community.home-assistant.io/t/add-on-hassos-i2c-configurator/264167).

---

## 3. Install AutomationHAT Custom Integration

- Go to **HACS > Integrations > Custom Repositories**
- Add the following repository:
  ```
  https://github.com/Aaron-Gardien/ha-automationhat
  ```
- Follow HACS prompts to install and configure the integration.

---

## 4. Node-RED: Gate 1 Example Flow

Import the following flow into Node-RED (`Menu > Import > Paste flow JSON`):

```json
[
    {
        "id": "0e9cd66578f40acb",
        "type": "http in",
        "z": "4a2f3a3073346261",
        "name": "",
        "url": "/endpoint/gate1",
        "method": "get",
        "upload": false,
        "swaggerDoc": "",
        "wires": [["fb3c1cd017fce351"]]
    },
    {
        "id": "fb3c1cd017fce351",
        "type": "function",
        "z": "4a2f3a3073346261",
        "name": "Parse Command",
        "func": "// Parse command from query parameter\nconst cmd = msg.req.query.cmd;\nif (cmd === \"open\") {\n    msg.payload = \"Gate Open Command Received\";\n    // Add logic to trigger the Automation HAT relay here\n    return msg;\n}\nif (cmd === \"close\") {\n    msg.payload = \"Gate Close Command Received\";\n    // Add logic to trigger the Automation HAT relay here\n    return msg;\n}\nmsg.payload = \"Unknown command\";\nreturn msg;",
        "outputs": 1,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 350,
        "y": 100,
        "wires": [["ce8c5ee5c2514edd"]]
    },
    {
        "id": "ce8c5ee5c2514edd",
        "type": "http response",
        "z": "4a2f3a3073346261",
        "name": "",
        "statusCode": "",
        "headers": {},
        "x": 610,
        "y": 100,
        "wires": []
    }
]
```

---

## 5. Usage

Send HTTP GET requests to control the gate:

- Open gate:  
  `http://<home-assistant-ip>:1880/endpoint/gate1?cmd=open`
- Close gate:  
  `http://<home-assistant-ip>:1880/endpoint/gate1?cmd=close`

Node-RED will process the command and trigger the appropriate output on the Automation HAT.

---

## 6. Troubleshooting

- Ensure all add-ons are **started** and **running**
- Confirm I2C is enabled (`/dev/i2c-1` should exist)
- Click **Deploy** in Node-RED after importing or editing flows
- Check Node-RED logs for errors if the endpoint doesn't respond as expected

---

## Links

- [AutomationHAT Home Assistant Integration](https://github.com/Aaron-Gardien/ha-automationhat)
- [HassOS I2C Configurator](https://community.home-assistant.io/t/add-on-hassos-i2c-configurator/264167)
- [Node-RED Documentation](https://nodered.org/docs/user-guide/)
- [HACS Setup](https://hacs.xyz/docs/setup/download)

---


