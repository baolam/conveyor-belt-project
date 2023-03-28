import cv2
import datetime

from torch import load
from torch import Tensor
from ...constant import *
from ... import client
from ...preprocess import running_transform
from ...train import _MyDataset

print("Nạp các mô hình deep learning...")
vegetable = load("vegetable.pt")
garbage = load("garbage.pt")
color = load("color.pt")
print("Hoàn thành nạp các mô hình")

Vegetable_Dataset = _MyDataset([TOMATO_DS_PẠTH, POTATO_DS_PATH])
Garbage_Dataset = _MyDataset([METAL_DS_PATH, NYLON_DS_PATH])
Color_Dataset = _MyDataset([RED_DS_PATH, YELLOW_DS_PATH])

from .mqtt import _build

class Working:
    def __init__(self, threshold : float = 0.5):
        self._mode = -1
        self.allow = False
        self.threshold = threshold
    
    def update(self, mode : int):
        self._mode = mode
    
    def is_run(self, allow):
        '''
            Có cho phép nhận dạng hay không
        '''
        self.allow = allow

    def _direction(self, res):
        if res == 0:
            res = "L"
        elif res == 1:
            res = "R"
        else: res = "F"
        return res
    
    def run(self, img):
        if not self.allow:
            return
        if self.allow and self._mode == -1:
            return
        img = cv2.resize(img, (HEIGHT, WIDTH))
        # 125 -> 125
        # WHEIGHT, WWIDTH
        ch, cw = HEIGHT // 2, WIDTH // 2
        _ch, _cw = WHEIGHT // 2, WWIDTH // 2
        img = img[ch - _ch:ch + _ch, cw - _cw:cw + _cw]
        img : Tensor = running_transform(img)
        img = img.unsqueeze(0)

        result, _type = self.__classify(img)
        code = self._direction(result)
        self._send(_type, code)

        # Gọi lệnh này để gửi gói tin sang thiết bị
        mqtt.publish(_build("classification"), 
            self._direction(code))
        
        self.allow = False
    
    def __classify(self, img):
        '''
            Tiến hành phân loại + Xác định nhãn
        '''
        labels = Vegetable_Dataset.labels
        res = 0

        img = img.to(device)
        if self._mode == 0:
            res = vegetable.forward(img).item()
        if self._mode == 1:
            labels = Garbage_Dataset.labels
            res = garbage.forward(img).item()
        elif self._mode == 2:
            labels = Color_Dataset.labels
            res = color.forward(img).item()

        if res < self.threshold:
            res = 0
        else: res = 1

        return res, labels[res]

    def _send(self, _type, result):
        '''
            Gửi kết quả đến người dùng
        '''
        r = datetime.datetime.now()
        t = '{}:{}:{}'.format(r.hour, r.minute, r.second)
        con = 'Vào lúc {}, nhận dạng được {}'.format(t, _type)
        client.emit("update-classification", data={
            "msg" : con,
            "res" : result
        }, namespace=NAMESPACE)

def _mode(mode):
    print("Chế độ nhận được là:", mode)
    working.update(mode)

client.on("mode", handler=_mode, namespace=NAMESPACE)
working = Working()

from .mqtt import mqtt
from .topic import _analyze

def on_message(_client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode()
    if _analyze(topic) == "detect":
        if message == "wanna":
            if client.connected:
                client.emit(
                    "notification", 
                    "Có vật thể muốn nhận dạng, vui lòng mở trình duyệt web và truy cập localhost:3000 để quản lí", 
                    namespace=NAMESPACE
                )
            working.is_run(True)
    if _analyze(topic) == "testing":
        print("Gửi bình thường")

# def on_log(client,userdata,level,buff):
#     print(buff)

mqtt.on_message = on_message

def mqtt_service():
    mqtt.connect(MQTT_SERVER, MQTT_PORT)
    mqtt.loop_forever()

def mqtt_end():
    mqtt.disconnect()