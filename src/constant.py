from typing import Final

TOMATO_PATH : Final = "./src/samples/tomatoes"
POTATO_PATH : Final = "./src/samples/potatoes"
METAL_PATH : Final = "./src/samples/metal"
NYLON_PATH : Final = "./src/samples/nylon"
RED_PATH : Final = "./src/samples/red"
YELLOW_PATH : Final = "./src/samples/yellow"

STORAGE_PATH : Final = "./src/datasets"

HEIGHT : Final = 250
WIDTH : Final = 250
CHANNEL : Final = 3
WHEIGHT : Final = 64
WWIDTH : Final = 64
SKIP : Final = 75

TOMATO_DS_PẠTH : Final = "./src/datasets/tomatoes"
POTATO_DS_PATH : Final = "./src/datasets/potatoes"
METAL_DS_PATH : Final = "./src/datasets/metal"
NYLON_DS_PATH : Final = "./src/datasets/nylon"
RED_DS_PATH : Final = "./src/datasets/red"
YELLOW_DS_PATH : Final = "./src/datasets/yellow"

from torch import cuda
device = "cpu"
if cuda.is_available():
    device = "cuda:0"
print("Mô hình AI cài đặt chạy trên thiết bị:", device)

STREAMING_FILE : Final = "./src/interface/layout/build/stream.png"
DEFAULT_SYMBOL_STREAMING : Final = "./src/interface/layout/build/camera.png"

NAMESPACE : Final = "/device"
MQTT_USER : Final = "nguyenducbaolam"
MQTT_PASS : Final = "0339588476"
MQTT_SERVER : Final = "mqtt.ohstem.vn"
MQTT_PORT : Final = 1883 