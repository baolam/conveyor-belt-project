from paho.mqtt import client as mqtt_client
from ...constant import *

mqtt = mqtt_client.Client()
mqtt.username_pw_set(MQTT_USER, MQTT_PASS)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect")

mqtt.on_connect = on_connect