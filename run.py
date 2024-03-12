import time

import solarman_mqtt.environment as environment
from solarman_mqtt.solarman import SolarmanAPI, State
from solarman_mqtt.homebridge_mqtt import HomebridgeMQTT

if __name__ == "__main__":
    print("Booting")
    print(f"Will poll every {environment.POLL_INTERVAL} seconds")
    solarman_api = SolarmanAPI(
        environment.SOLARMAN_APPID,
        environment.SOLARMAN_APPSECRET,
        environment.SOLARMAN_EMAIL,
        environment.SOLARMAN_PASSWORD,
        environment.SOLARMAN_INVERTER
    )
    homebridge_mqtt = HomebridgeMQTT(environment.MQTT_BROKER_HOST, port=environment.MQTT_BROKER_PORT)
    while True:
        state: State = solarman_api.get_state()
        homebridge_mqtt.publish_state(state)
        time.sleep(environment.POLL_INTERVAL)
