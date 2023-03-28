import sys
sys.path.append("./")

import threading
import time
from src.interface.utils import mqtt_service, mqtt_end
from src.interface.utils import mqtt
from src.interface.utils.topic import _analyze, _build

try:
    threading.Thread(name="MQTT Service", target=mqtt_service) \
        .start()
    time.sleep(2.5)
    while True:
        code = input("Nhập lệnh điều khiển: ")
        mqtt.publish(_build("classification"), code)
except:
    mqtt_end()