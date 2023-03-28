import cv2
import threading
import time

video = cv2.VideoCapture(1)

from src.constant import *
from src import server_service
from src import client_service
from src import client
from src.interface.utils import working
from src.interface.utils.streaming import streaming
from src.interface.utils import mqtt_service
from src.interface.utils import mqtt_end

def _end():
    mqtt_end()
    client.disconnect()
    cv2.destroyAllWindows()

try:
    threading.Thread(name="Server", target=server_service) \
        .start()

    time.sleep(2)

    threading.Thread(name="Socket service", target=client_service) \
        .start()

    threading.Thread(name="Mqtt service", target=mqtt_service) \
        .start()

    print("Camera đã hoạt động")

    while True:
        __, frame = video.read()
        streaming(frame)
        working.run(frame)

        cv2.imshow("TESTING", frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    
    _end()
except Exception as e:
    print("Thoát chương trình")
    print(e)
    _end()