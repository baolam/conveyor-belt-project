from typing import List

from torch.utils.data import Dataset
from ..preprocess import training_transform
from ..constant import *

import cv2
import os

class _MyDataset(Dataset):
    def __init__(self, cls_paths : List[str], transform = training_transform, allow_build_label : bool = True):
        super().__init__()

        self.links = []
        self.labels = { }
        self.transform = transform

        for i in range(len(cls_paths)):
            points = os.listdir(cls_paths[i])
            for point in points:
                store = cls_paths[i] + "/" + point
                self.links.append((store, i))
            if allow_build_label:
                self.labels[cls_paths[i].split('/')[3]] = i
                self.labels[i] = cls_paths[i].split('/')[3]
    
    def __len__(self):
        return len(self.links)

    def __getitem__(self, index):
        link, label = self.links[index]
        img = cv2.imread(link)
        img = cv2.resize(img, (WHEIGHT, WWIDTH))
        img = self.transform(img)

        return img, float(label)

class _AutoEncoderDataset(_MyDataset):
    def __init__(self, cls_paths: List[str], transform=training_transform):
        super().__init__(cls_paths, transform, False)
    
    def __getitem__(self, index):
        link, __ = self.links[index]
        img = cv2.imread(link)
        img = cv2.resize(img, (WHEIGHT, WWIDTH))
        img = self.transform(img)
        img = img.reshape(-1)
        
        return img, img