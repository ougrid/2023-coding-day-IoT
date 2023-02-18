from paho.mqtt.client import Client
import logging
import json

from tuya.decode import TuyaDecoder
from tuya.command import TuyaCommand
import logging

# ------------------------------------------------------------------------------------------------

class MosquittoMqttLocalHandler(TuyaDecoder):
    def __init__(self, address: str):
        self.ext_addr = address
        super(TuyaDecoder, self).__init__() # placeholder

    def on_connect(self, client, userdata, flags, rc):
        logging.info(rc)
        self.command = TuyaCommand(client)
        if rc == 0:
            logging.info("Local MQTT connected")
            topic = f"zigbee2mqtt/{self.ext_addr}"
            client.subscribe(topic)
            self.command.turn_on_smart_plug(self.ext_addr)

    def on_message(self, client, userdata, msg):

        # Some info logging
        logging.info(f"Receiving message from topic : {msg.topic}")
        # logging.info(f"Message data : {str(msg.payload.decode('utf-8'))}")
        zigbee_payload = json.loads(msg.payload.decode('utf-8'))

        logging.info(f"Message from sensor: {self.decode_smart_plug(zigbee_payload)}")

# ------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    # Setup logging
    logging.basicConfig(level=logging.DEBUG,format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.StreamHandler()])

    USER = "trinity"
    PASS = "trinity"
    ZIGBEE_ADDRESS = "0xa4c138f5ce6b8db6"

    # Connect local mqtt
    local_mqtt_client = Client()
    local_mosquitto_handler = MosquittoMqttLocalHandler(ZIGBEE_ADDRESS)
    local_mqtt_client.on_connect = local_mosquitto_handler.on_connect
    local_mqtt_client.on_message = local_mosquitto_handler.on_message
    local_mqtt_client.username_pw_set(USER, PASS)

    # Try to connect to MQTT (wait untill mqtt broker is ready)
    host = "localhost"
    mqtt_local_port = 1883
    connect_success = False
    while not connect_success:
        try:
            local_mqtt_client.connect(host, mqtt_local_port, 60)
            local_mqtt_client.loop_forever()
            connect_success = True
        except ConnectionRefusedError as e:
            logging.error("Can't connect to local mqtt broker")
            logging.error("Retry in 5 seconds")
            time.sleep(5)