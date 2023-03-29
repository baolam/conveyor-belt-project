from yolobit import *
import machine
from i2c_motor_driver import MotorDriver4Channel
import _thread
from mqtt import *
from yolobit import *
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1
from hcsr04 import HCSR04
import time

driver = MotorDriver4Channel(machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000))

# Mô tả hàm này...
def conveyor_belt(working, speed):
  if working:
    driver.set_motor(1,speed)
  else:
    driver.set_motor(1,0)

def escape_camera():
  global default_conveyor_belt
  driver.set_motor_time(1, 90, 3)
  
# Hàm nhận kết quả từ phía máy tính
def classification_result(res):
  global has_object, default_conveyor_belt
  #mqtt.publish("testing", "okok")
  
  # Lệnh này đóng vai trò quan trọng
  driver.set_motor_time(0, 0, 0.5)
  
  # Chắc chắn là có hàng hóa
  if has_object != 2:
    return
  
  if res == "L":
    classify_with_bars(1)
    escape_camera()
    classify_with_bars(0)
  
  if res == "R":
    classify_with_bars(0)
    escape_camera()
    classify_with_bars(1)
    
  if res == "F":
    #display.scroll(4)
    conveyor_belt(1, default_conveyor_belt)
    time.sleep_ms(2500)
    
  has_object = 0
  
# Khởi tạo cảm biến siêu âm
def initalize_sensor():
  global detect_object, yellow_stack, blue_stack, white_stack
  detect_object = HCSR04(trigger_pin=pin3.pin, echo_pin=pin6.pin)
  yellow_stack = HCSR04(trigger_pin=pin10.pin, echo_pin=pin13.pin)
  blue_stack = HCSR04(trigger_pin=pin14.pin, echo_pin=pin15.pin)
  white_stack = HCSR04(trigger_pin=pin12.pin, echo_pin=pin16.pin)

# Hàm này hoạt động (điều khiển băng chuyền khi không có vật thể)
def camera():
  global detect_object, has_object
  if has_object != 0:
    return
  
  if detect_object.distance_cm() < 10:
    has_object = 1
    driver.set_motor(1,(-90))
    time.sleep_ms(750)
    conveyor_belt(0, default_conveyor_belt)
  else:
    has_object = 0
    conveyor_belt(1, default_conveyor_belt)

# Hàm kết nối wifi và mqtt đến thiết bị
def wifi():
  mqtt.connect_wifi('VNPT-VINH CHANH', '0967030483')
  mqtt.connect_broker(server='mqtt.ohstem.vn', port=1883, username='nguyenducbaolam', password='0339588476')
  mqtt.on_receive_message("classification", classification_result)
  
# Hàm thực hiện phân loại hàng hóa qua hai bên
def classify_with_bars(left, durate = 1.2):
  # Bằng 0 nghĩa là đi sang trái, 1 nghĩa là sang phải
  if left == 0:
    driver.set_motor_time(0, -50, durate)
  else:
    driver.set_motor_time(0, 50, durate)
  #time.sleep_ms(int(durate * 100))

default_conveyor_belt = 90
has_object = 0

display.clear()
initalize_sensor()
wifi()

# Phần khởi động động cơ
classify_with_bars(0) # Trái
classify_with_bars(1) # Phải
  
while True:
  mqtt.check_message()
  camera()
  #display.scroll(has_object)
  if has_object == 1:
    conveyor_belt(0, default_conveyor_belt)
    mqtt.publish("detect", "wanna")
    has_object = 2

# https://app.ohstem.vn/#!/share/yolobit/2NdrCfxHHj2ZyGQFVRR6UNXrIzE