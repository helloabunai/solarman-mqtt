# solarman-mqtt
> Poll Solarman APIs and display data in HomeKit via MQTT broker
> WIP Fork/update to polling solarman APIs after the database split to separate global/chinese regions + API format change
> Implementation currently ongoing. Not ready for use.

# Features
- [x] Display battery power as a light sensor
- [x] Display "Inverter Supply" as a contact sensor (useful for checking if supply is from Inverter or Grid)
- [x] Display battery SOC as a meta property on the contact sensor
- [x] Display low battery alert below a configured threshold
- [x] Display if battery is charging

# Screenshots
![Grid supplying power](./docs/images/1.PNG)
![Battery level](./docs/images/2.PNG)
![Inverter supplying power and battery power](./docs/images/3.PNG)
![Low Battery Warning](./docs/images/4.PNG)

# Disclaimer
- This has only been tested on a SofarSolar inverter with a Solarman WiFi data logger.
- The docker image has only been tested with linux/amd64 in mind.
- The original developer's armV7 docker target has not been tested at all.

# Prerequisites
- docker
- docker-compose
- homebridge
- [homebridge-mqtt plugin](https://github.com/cflurin/homebridge-mqtt)

# MQTT Broker
In my setup, I am utilising a [Mosquitto](https://github.com/eclipse/mosquitto) MQTT broker, running on my Synology NAS. It is available from the synology Package Store. Homebridge is also running on the same Synology machine, so to connect Homebridge<->MQTT<->SolarMan involves internal network IPs. If you run MQTT brokers on different devices than your target docker machine, you probably don't need assistance in getting the softwares communicating with each other.

# Limitations
- The Solarman WiFi loggers only send data every 15 minutes or so (the `POLL_INTERVAL` should be set accordingly)
- Power values (usually watts) are modelled as a light sensor in HomeKit (in Lux). HomeKit does not support any sensor capable of displaying watts.

# Setup
See the example `docker-compose.yml` for details. You will need to contact solarman customer support to be granted API access for the new API.
If working locally then please create a .env file in the root of the project (see .example-env).
