import sys
sys.path.append("./")

from src.constant import *
from src.preprocess.transform import running_transform
from src.interface.utils import working
from torch import Tensor

import cv2
import time
video = cv2.VideoCapture(0)
working.update(0)

while True:
    __, frame = video.read()
    frame = cv2.resize(frame, ((HEIGHT, WIDTH)))

    cv2.imshow("TESTING", frame)
    
    ch, cw = HEIGHT // 2, WIDTH // 2
    _ch, _cw = WHEIGHT // 2, WWIDTH // 2
    img = frame[ch - _ch:ch + _ch, cw - _cw:cw + _cw]

    cv2.imshow("OBJ", img)

    img : Tensor = running_transform(img)
    img = img.unsqueeze(0)

    prev = time.time()
    out = working.classify(img)
    code = working.choose(img)
    curr = time.time()

    print("===============================")
    print("Time = {:.5f}s".format(curr-prev))
    print(out)
    print(code)
    print("===============================")
    print()

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
