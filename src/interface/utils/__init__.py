import cv2
import datetime

from torch import load
from torch import nn
from torch import Tensor
from ...constant import *
from ... import client
from ...preprocess import running_transform
from ...train import _MyDataset

print("Nạp các mô hình deep learning...")
vegetable = load("vegetable.pt")
garbage = load("garbage.pt")
color = load("color.pt")
# Mô hình auto-encoder
auc_veget = load("auc_veget.pt")
auc_garbage = load("auc_garbage.pt")
auc_color = load("auc_color.pt")
print("Hoàn thành nạp các mô hình")
print("Cài đặt chế độ hoạt động của các mô hình...")
vegetable.eval(), garbage.eval(), color.eval()
auc_veget.eval(), auc_garbage.eval(), auc_color.eval()
print("Hoàn thành cài đặt chế độ hoạt động")

Vegetable_Dataset = _MyDataset([TOMATO_DS_PẠTH, POTATO_DS_PATH])
Garbage_Dataset = _MyDataset([METAL_DS_PATH, NYLON_DS_PATH])
Color_Dataset = _MyDataset([RED_DS_PATH, YELLOW_DS_PATH])

from .mqtt import _build
diff_measure = nn.MSELoss()
class Working:
    def __init__(self, threshold : float = 0.5):
        self._mode = -1
        self.allow = False
        self.threshold = threshold

        self.outlier = {
            0 : 0.01,
            1 : 0.92,
            2 : 1.5
        }
    
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

        code = "F"
        _type = "N-O-N-E"
        if self.__choose(img) == 0:
            result, _type = self.__classify(img)
            code = self._direction(result)
        self._send(_type, code)

        # Gọi lệnh này để gửi gói tin sang thiết bị
        mqtt.publish(_build("classification"), 
            self._direction(code))
        
        self.allow = False
    
    def __classify(self, img, allow_probability : bool = False):
        '''
            Tiến hành phân loại + Xác định nhãn
        '''
        labels = Vegetable_Dataset.labels
        prob = 0

        img = img.to(device)
        if self._mode == 0:
            prob = vegetable.forward(img).item()
        if self._mode == 1:
            labels = Garbage_Dataset.labels
            prob = garbage.forward(img).item()
        elif self._mode == 2:
            labels = Color_Dataset.labels
            prob = color.forward(img).item()

        res = 0
        if prob >= self.threshold:
            res = 1

        if allow_probability:
            return res, labels[res], prob

        return res, labels[res]

    def __choose(self, img : Tensor, allow_theta = False):
        '''
            Gọi hàm này để trả về trường hợp có phải ngoại lai hay không
            0 --> Không phải
            1 --> Phải
        '''
        img = img.reshape(img.size()[0], -1)
        y_hat = 0

        img = img.to(device)
        if self._mode == 0:
            y_hat = auc_veget.forward(img)
        elif self._mode == 1:
            y_hat = auc_garbage.forward(img)
        elif self._mode == 2:
            y_hat = auc_color.forward(img)
        
        theta = diff_measure(y_hat, img) \
            .item()
        
        r = 1
        if theta <= self.outlier[self._mode]:
            r = 0
        
        if allow_theta:
            return r, theta
        
        return r

    def classify(self, img):
        return self.__classify(img, True)

    def choose(self, img):
        return self.__choose(img, True)

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