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
[{"id":"4a2f3a3073346261","type":"tab","label":"Flow 1","disabled":false,"info":"","env":[]},{"id":"b858f669a3193b17","type":"inject","z":"4a2f3a3073346261","name":"Open Gate","props":[{"p":"payload"},{"p":"topic","vt":"str"}],"repeat":"","crontab":"","once":false,"onceDelay":0.1,"topic":"","payload":"","payloadType":"date","x":140,"y":200,"wires":[["cd0255c0b96d8dad"]]},{"id":"e560273ec5ef7d41","type":"delay","z":"4a2f3a3073346261","name":"500ms","pauseType":"delay","timeout":"500","timeoutUnits":"milliseconds","rate":"1","nbRateUnits":"1","rateUnits":"second","randomFirst":"1","randomLast":"5","randomUnits":"seconds","drop":false,"allowrate":false,"outputs":1,"x":910,"y":300,"wires":[["3e34a4595f5ee575"]]},{"id":"796cdc8e65b68dd2","type":"tcp in","z":"4a2f3a3073346261","name":"Inner Range","server":"server","host":"","port":"5000","datamode":"stream","datatype":"buffer","newline":"","topic":"","trim":false,"base64":false,"tls":"","x":110,"y":60,"wires":[["fb3c1cd017fce351"]]},{"id":"ddbd4e9de42ac606","type":"switch","z":"4a2f3a3073346261","name":"","property":"payload","propertyType":"msg","rules":[{"t":"eq","v":"open","vt":"str"},{"t":"eq","v":"close","vt":"str"}],"checkall":"true","repair":false,"outputs":2,"x":390,"y":140,"wires":[["cd0255c0b96d8dad"],["30a4735efbd9dc44"]]},{"id":"1c97dee02e78b128","type":"debug","z":"4a2f3a3073346261","name":"debug 2","active":false,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","statusVal":"","statusType":"auto","x":1140,"y":440,"wires":[]},{"id":"bcf17b219e44492b","type":"server-state-changed","z":"4a2f3a3073346261","name":"Gate Status Changed","server":"ce1052b5.632be","version":6,"outputs":2,"exposeAsEntityConfig":"","entities":{"entity":["binary_sensor.gate_1_status"],"substring":[],"regex":[]},"outputInitially":false,"stateType":"str","ifState":"on","ifStateType":"str","ifStateOperator":"is","outputOnlyOnStateChange":true,"for":"0","forType":"num","forUnits":"minutes","ignorePrevStateNull":false,"ignorePrevStateUnknown":false,"ignorePrevStateUnavailable":false,"ignoreCurrentStateUnknown":false,"ignoreCurrentStateUnavailable":false,"outputProperties":[{"property":"payload","propertyType":"msg","value":"","valueType":"entityState"},{"property":"data","propertyType":"msg","value":"","valueType":"eventData"},{"property":"topic","propertyType":"msg","value":"","valueType":"triggerId"}],"x":340,"y":500,"wires":[["b78878e023396182"],["9c5bb8a082363e66"]]},{"id":"cd0255c0b96d8dad","type":"api-current-state","z":"4a2f3a3073346261","name":"Check if Gate is Open","server":"ce1052b5.632be","version":3,"outputs":2,"halt_if":"off","halt_if_type":"str","halt_if_compare":"is","entity_id":"binary_sensor.gate_1_status","state_type":"str","blockInputOverrides":true,"outputProperties":[{"property":"payload","propertyType":"msg","value":"","valueType":"entityState"},{"property":"data","propertyType":"msg","value":"","valueType":"entity"}],"for":"0","forType":"num","forUnits":"minutes","override_topic":false,"state_location":"payload","override_payload":"msg","entity_location":"data","override_data":"msg","x":440,"y":200,"wires":[["3aeef04409808423"],[]]},{"id":"3aeef04409808423","type":"api-call-service","z":"4a2f3a3073346261","name":"","server":"ce1052b5.632be","version":7,"debugenabled":false,"action":"switch.turn_on","floorId":[],"areaId":[],"deviceId":[],"entityId":["switch.relay_one"],"labelId":[],"data":"","dataType":"jsonata","mergeContext":"","mustacheAltTags":false,"outputProperties":[],"queue":"none","blockInputOverrides":true,"domain":"switch","service":"turn_on","x":700,"y":180,"wires":[["e560273ec5ef7d41"]]},{"id":"3d8e7ac788cf4f01","type":"inject","z":"4a2f3a3073346261","name":"Close Gate","props":[{"p":"payload"},{"p":"topic","vt":"str"}],"repeat":"","crontab":"","once":false,"onceDelay":0.1,"topic":"","payload":"","payloadType":"date","x":140,"y":260,"wires":[["30a4735efbd9dc44"]]},{"id":"d90f9d21cfed2227","type":"api-call-service","z":"4a2f3a3073346261","name":"","server":"ce1052b5.632be","version":7,"debugenabled":false,"action":"switch.turn_on","floorId":[],"areaId":[],"deviceId":[],"entityId":["switch.relay_one"],"labelId":[],"data":"","dataType":"jsonata","mergeContext":"","mustacheAltTags":false,"outputProperties":[],"queue":"none","blockInputOverrides":true,"domain":"switch","service":"turn_on","x":700,"y":240,"wires":[["e560273ec5ef7d41"]]},{"id":"30a4735efbd9dc44","type":"api-current-state","z":"4a2f3a3073346261","name":"Check if Gate is Closed","server":"ce1052b5.632be","version":3,"outputs":2,"halt_if":"on","halt_if_type":"str","halt_if_compare":"is","entity_id":"binary_sensor.gate_1_status","state_type":"str","blockInputOverrides":true,"outputProperties":[{"property":"payload","propertyType":"msg","value":"","valueType":"entityState"},{"property":"data","propertyType":"msg","value":"","valueType":"entity"}],"for":"0","forType":"num","forUnits":"minutes","override_topic":false,"state_location":"payload","override_payload":"msg","entity_location":"data","override_data":"msg","x":450,"y":260,"wires":[["d90f9d21cfed2227"],[]]},{"id":"b78878e023396182","type":"api-call-service","z":"4a2f3a3073346261","name":"Gate Status Light On","server":"ce1052b5.632be","version":7,"debugenabled":false,"action":"light.turn_on","floorId":[],"areaId":[],"deviceId":[],"entityId":["light.light_comms"],"labelId":[],"data":"","dataType":"jsonata","mergeContext":"","mustacheAltTags":false,"outputProperties":[],"queue":"none","blockInputOverrides":true,"domain":"light","service":"turn_on","x":740,"y":440,"wires":[["2dea709ee03492f0"]]},{"id":"3e34a4595f5ee575","type":"api-call-service","z":"4a2f3a3073346261","name":"","server":"ce1052b5.632be","version":7,"debugenabled":false,"action":"switch.turn_off","floorId":[],"areaId":[],"deviceId":[],"entityId":["switch.relay_one"],"labelId":[],"data":"","dataType":"jsonata","mergeContext":"","mustacheAltTags":false,"outputProperties":[],"queue":"none","blockInputOverrides":true,"domain":"switch","service":"turn_off","x":1080,"y":300,"wires":[[]]},{"id":"9c5bb8a082363e66","type":"api-call-service","z":"4a2f3a3073346261","name":"Gate Status Light Off","server":"ce1052b5.632be","version":7,"debugenabled":false,"action":"light.turn_off","floorId":[],"areaId":[],"deviceId":[],"entityId":["light.light_comms"],"labelId":[],"data":"","dataType":"jsonata","mergeContext":"","mustacheAltTags":false,"outputProperties":[],"queue":"none","blockInputOverrides":true,"domain":"light","service":"turn_off","x":740,"y":520,"wires":[["2dea709ee03492f0"]]},{"id":"fb3c1cd017fce351","type":"function","z":"4a2f3a3073346261","name":"function 1","func":"// Assume msg.payload = { \"msg\": \"open\" } or { \"msg\": \"close\" }\nif (msg.payload.msg === \"open\") {\n    // Handle 'open' command\n    msg.payload = \"open\";\n    // or do something else (set msg.url, trigger relay, etc.)\n    return msg;\n}\nif (msg.payload.msg === \"close\") {\n    // Handle 'close' command\n    msg.payload = \"close\";\n    // or do something else\n    return msg;\n}\n// Handle unknown command\nmsg.payload = \"Unknown command\";\nreturn msg;","outputs":1,"timeout":0,"noerr":0,"initialize":"","finalize":"","libs":[],"x":300,"y":80,"wires":[["ddbd4e9de42ac606","72c3218e75a4db5c"]]},{"id":"2dea709ee03492f0","type":"change","z":"4a2f3a3073346261","name":"","rules":[{"t":"change","p":"payload","pt":"msg","from":"on","fromt":"str","to":"open","tot":"str"},{"t":"change","p":"payload","pt":"msg","from":"off","fromt":"str","to":"closed","tot":"str"}],"action":"","property":"","from":"","to":"","reg":false,"x":960,"y":480,"wires":[["1c97dee02e78b128","82bf10cdf3e8701c"]]},{"id":"1c71eb4490093c7d","type":"http request","z":"4a2f3a3073346261","name":"","method":"GET","ret":"txt","paytoqs":"ignore","url":"","tls":"","persist":true,"proxy":"","insecureHTTPParser":false,"authType":"basic","senderr":false,"headers":[],"x":1290,"y":480,"wires":[["8de0732bba4c2092"]]},{"id":"8de0732bba4c2092","type":"debug","z":"4a2f3a3073346261","name":"Inner Range Response","active":false,"tosidebar":true,"console":false,"tostatus":false,"complete":"payload","targetType":"msg","statusVal":"","statusType":"auto","x":1500,"y":480,"wires":[]},{"id":"82bf10cdf3e8701c","type":"function","z":"4a2f3a3073346261","name":"Set Url","func":"const baseUrl = \"http://IN94045852.local/receive_http_connection?key=gate&message=\";\n    msg.url = baseUrl + msg.payload;\n    return msg;\n","outputs":1,"timeout":0,"noerr":0,"initialize":"","finalize":"","libs":[],"x":1130,"y":480,"wires":[["1c71eb4490093c7d"]]},{"id":"2cdcbf66fc45a813","type":"api-current-state","z":"4a2f3a3073346261","name":"Check Gate Status","server":"ce1052b5.632be","version":3,"outputs":2,"halt_if":"on","halt_if_type":"str","halt_if_compare":"is","entity_id":"binary_sensor.gate_1_status","state_type":"str","blockInputOverrides":true,"outputProperties":[{"property":"payload","propertyType":"msg","value":"","valueType":"entityState"},{"property":"data","propertyType":"msg","value":"","valueType":"entity"}],"for":"0","forType":"num","forUnits":"minutes","override_topic":false,"state_location":"payload","override_payload":"msg","entity_location":"data","override_data":"msg","x":330,"y":460,"wires":[["b78878e023396182"],["9c5bb8a082363e66"]]},{"id":"8d17c09d4128d3a5","type":"inject","z":"4a2f3a3073346261","name":"","props":[{"p":"payload"},{"p":"topic","vt":"str"}],"repeat":"1","crontab":"","once":true,"onceDelay":"6","topic":"","payload":"","payloadType":"date","x":110,"y":460,"wires":[["2cdcbf66fc45a813"]]},{"id":"ce8c5ee5c2514edd","type":"http response","z":"4a2f3a3073346261","name":"","statusCode":"","headers":{},"x":330,"y":20,"wires":[]},{"id":"5ef8a28b9c28d7d5","type":"http in","z":"4a2f3a3073346261","name":"","url":"/gate1","method":"get","upload":false,"swaggerDoc":"","x":140,"y":20,"wires":[["fb3c1cd017fce351","ce8c5ee5c2514edd"]]},{"id":"72c3218e75a4db5c","type":"debug","z":"4a2f3a3073346261","name":"debug 1","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","statusVal":"","statusType":"auto","x":560,"y":80,"wires":[]},{"id":"ce1052b5.632be","type":"server","name":"Home Assistant","addon":true}]
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
