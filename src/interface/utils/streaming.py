import numpy as np
import cv2
import base64
import sys

from ...constant import *
from . import client

def streaming(img : np.ndarray):
    try:
        __, con = cv2.imencode(".png", img)
        con = base64.b64encode(con)
        con = con.decode("utf-8")
        con = "data:image/png;base64," + con
        if client.connected:
            client.emit("streaming", con, namespace=NAMESPACE)
    except:
        client.disconnect()
        sys.exit(0)