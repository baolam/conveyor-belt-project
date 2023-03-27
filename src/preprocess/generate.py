from ..constant import *

import numpy as np
import cv2
import os
import time

if os.path.exists(STORAGE_PATH) == False:
    os.makedirs(STORAGE_PATH)

from sklearn.feature_extraction import image
from tqdm import tqdm
def __stride(img : np.ndarray):
    res = image.extract_patches_2d(img, (WHEIGHT, WWIDTH))
    return res

def analyze(root_path : str):
    label = root_path.split('/')[3]
    storage = STORAGE_PATH + "/" + label

    if os.path.exists(storage) == False:
        os.makedirs(storage)
    
    files = os.listdir(root_path)
    for file in files:
        try:
            prefix = file.split('.')[0]
            img = cv2.imread(root_path + "/" + file)
            img = cv2.resize(img, (HEIGHT, WIDTH))
            img = img[SKIP:HEIGHT-SKIP,SKIP:WIDTH-SKIP]
            #print(img.shape)
            patches = __stride(img)

            n = patches.shape[0]
            for i in tqdm(range(n)):
                code = time.time()
                fname = '{}/{}_{}.png'.format(storage, prefix, code)
                cv2.imwrite(fname, patches[i])
        except:
            pass

# analyze(TOMATO_PATH)
# analyze(POTATO_PATH)