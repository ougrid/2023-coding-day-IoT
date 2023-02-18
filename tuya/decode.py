class TuyaDecoder():
    """
    Class to decode mqtt payload from Tuya device using Zigbee2MQTT
    """

    def __init__(self):
        pass

    @staticmethod
    def decode_temp_humid_display(zigbee_payload: dict) -> dict:
        """
        Supported devices:
        - JM-TRH-ZGB-V1 (https://www.zigbee2mqtt.io/devices/JM-TRH-ZGB-V1.html)
            Minimum report interval : 5 mins

        Payload:
        {
        "battery": 100,
        "device": {
            "applicationVersion": 72,
            "dateCode": "",
            "friendlyName": "0xa4c1382e1273c6da",
            "hardwareVersion": 1,
            "ieeeAddr": "0xa4c1382e1273c6da",
            "manufacturerID": 4417,
            "manufacturerName": "_TZE200_whkgqxse",
            "model": "JM-TRH-ZGB-V1",
            "networkAddress": 32337,
            "powerSource": "Battery",
            "stackVersion": 0,
            "type": "EndDevice",
            "zclVersion": 3
        },
        "humidity": 68,
        "humidity_alarm": "upper_alarm",
        "linkquality": 149,
        "max_humidity": 7,
        "max_temperature": 36,
        "min_humidity": 2,
        "min_temperature": 20,
        "report_interval": 5,
        "temperature": 31.3,
        "temperature_alarm": "upper_alarm",
        "temperature_unit_convert": "celsius"
        }
        """
        temp = zigbee_payload.get("temperature")
        humid = zigbee_payload.get("humidity")
        return {
            "tuya_temperature": temp,
            "tuya_humidity": humid,
        }
    
    @staticmethod
    def decode_smart_plug(zigbee_payload: dict) -> dict:
        """
        Supported devices:
        - TS011F (Thailand model)
            On Zigbee2mqtt, it support only non-TH model.
            I have adjust some converter to make TH model supported by Zigbee2mqtt (demo purpose only)

        Payload:
        {
            "child_lock": "UNLOCK",
            "current": 0,
            "device": {
                "applicationVersion": 77,
                "dateCode": "",
                "friendlyName": "0xa4c138acc52bffe0",
                "hardwareVersion": 1,
                "ieeeAddr": "0xa4c138acc52bffe0",
                "manufacturerID": 4417,
                "manufacturerName": "_TZ3000_fgwhjm9j",
                "model": "TS011F_plug_1",
                "networkAddress": 54835,
                "powerSource": "Mains (single phase)",
                "stackVersion": 0,
                "type": "Router",
                "zclVersion": 3
            },
            "energy": 0,
            "indicator_mode": "off/on",
            "linkquality": 127,
            "power": 0,
            "power_outage_memory": "restore",
            "state": "OFF",
            "update": {
                "state": null
            },
            "update_available": null,
            "voltage": 230
        }
        """
        state = zigbee_payload.get("state") # "ON" or "OFF"
        voltage = zigbee_payload.get("voltage") # V
        current = zigbee_payload.get("current") # A
        power = zigbee_payload.get("power") # W
        switch_on = None
        if state == "ON":
            switch_on = True
        elif state == "OFF": 
            switch_on = False
        return {
            "switch_on": switch_on,
            "voltage": voltage,
            "current": current,
            "power": power,
        }