import sys
sys.path.append("./")

import threading
import time
from src.interface.utils import mqtt_service, mqtt_end
from src.interface.utils import mqtt
from src.interface.utils.topic import _analyze, _build

try:
    #mqtt_service()
    threading.Thread(name="MQTT Service", target=mqtt_service) \
        .start()
    while True:
        time.sleep(2)
        mqtt.publish(_build("classification"), "2")
except:
    mqtt_end()