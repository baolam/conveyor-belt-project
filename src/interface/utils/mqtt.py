from paho.mqtt import client as mqtt_client
from ...constant import *
from .topic import _build

mqtt = mqtt_client.Client()
mqtt.username_pw_set(MQTT_USER, MQTT_PASS)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect")
    mqtt.subscribe(_build("detect"))
    mqtt.subscribe(_build("classification"))
    mqtt.subscribe(_build("testing"))

mqtt.on_connect = on_connect