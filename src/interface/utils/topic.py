from ...constant import *

def _build(code):
    return '{}/feeds/{}'.format(MQTT_USER, code)

def _analyze(topic):
    return topic.split('/')[2]
