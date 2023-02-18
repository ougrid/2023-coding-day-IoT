import time
import json
from datetime import datetime
import paho.mqtt.client as mqtt
import struct
import logging
import yaml
import json

## ------------------------------------------------------------------------------------

class MosquittoMqttLocalHandler():
    def __init__(self, ieee_addr_list):
        self.placeholder = 0
        self.ieee_addr_list = ieee_addr_list

    def on_connect(self, client, userdata, flags, rc):
        logging.info(rc)
        if rc == 0:
            logging.info("Local MQTT connected")
            for addr in self.ieee_addr_list:
                topic = f"zigbee2mqtt/{addr}"
                client.subscribe(topic)
            topic = f"zigbee2mqtt/0xa4c1385adf6c00ce"
            client.subscribe(topic)
            logging.info(f"Subscribe to topic {topic} is completed")
            # client.publish("zigbee2mqtt/0xa4c138acc52bffe0/set", json.dumps({"state": "ON"}))
            # client.publish("zigbee2mqtt/0xa4c1382e1273c6da/set", json.dumps({"temperature_unit_convert": "celsius"}))
            # client.publish("zigbee2mqtt/0xa4c1382e1273c6da/set", json.dumps({"temperature_unit_convert": "fahrenheit"}))

    def on_message(self, client, userdata, msg):
        logging.info(f"Receving message from topic : {msg.topic}")
        logging.info(f"Message data : {str(msg.payload.decode('utf-8'))}")

class YamlReader():
    def __init__(self, yaml_path: str):
        self.yaml_path = yaml_path
        self.read()

    def read(self):
        self.read_yaml()

    def read_yaml(self):
        with open(self.yaml_path) as file:
            self.yaml_dict = yaml.load(file, Loader = yaml.FullLoader)
        return self.yaml_dict
    
    def get_all_zigbee_ieee_addr(self):
        device_list = []
        if self.yaml_dict.get("devices"):
            device_list = list(self.yaml_dict.get("devices").keys())
        else:
            logging.warning("No paired zigbee devices was found")
        return device_list

## ------------------------------------------------------------------------------------

if __name__ == "__main__":

    # Setup logging
    logging.basicConfig(level=logging.DEBUG,format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.StreamHandler()])
    
    # Read all zigbee devices from zigbee2mqtt configuration file
    zigbee2mqtt_config_path = f'/home/trinity/home_assistant/zigbee2mqtt/data/configuration.yaml'
    reader = YamlReader(zigbee2mqtt_config_path)
    zigbee2mqtt_config = reader.read()
    device_list = reader.get_all_zigbee_ieee_addr()
    
    host = "localhost"
    mqtt_local_port = 1883
    username = "trinity"
    password = "trinity"

    local_mqtt_client = mqtt.Client()
    local_mosquitto_handler = MosquittoMqttLocalHandler(device_list)
    local_mqtt_client.on_connect = local_mosquitto_handler.on_connect
    local_mqtt_client.on_message = local_mosquitto_handler.on_message
    local_mqtt_client.username_pw_set(username, password)
    local_mqtt_client.connect(host, mqtt_local_port, 60)

    try:
        logging.info("Hello world")
        local_mqtt_client.loop_forever()

    except:
        logging.error("Error occur", exc_info = True)