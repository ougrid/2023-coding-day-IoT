from paho.mqtt.client import Client as paho_client
import json
import logging

class TuyaCommand():
    """
    Class to set/command Tuya device using Zigbee2MQTT
    """
    def __init__(self, local_client: paho_client):
        self.mqtt_client = local_client

    def change_temp_unit(self, ieee_addr: str, unit: str):
        """
        Change temperature unit between degree Celsius and degree Fahrenheit
        """
        if unit in ["fahrenheit", "celsius"]:
            self.mqtt_client.publish(
                f"zigbee2mqtt/{ieee_addr}/set",
                json.dumps({"temperature_unit_convert": unit})
            )
        else:
            logging.error("Unit of temperature is not supported. Please choose between ['celsius', 'fahrenheit']")

    def turn_on_smart_plug(self, ieee_addr: str):
        """
        Turn on smart plug
        """
        self.mqtt_client.publish(
            f"zigbee2mqtt/{ieee_addr}/set",
            json.dumps({"state": "ON"})
        )

    def turn_off_smart_plug(self, ieee_addr: str):
        """
        Turn off smart plug
        """
        self.mqtt_client.publish(
            f"zigbee2mqtt/{ieee_addr}/set",
            json.dumps({"state": "OFF"})
        )

