from typing import List

from torch import nn
from torch.utils.data import DataLoader
from matplotlib import pyplot as plt

from ..constant import *
from ..preprocess import epoch
from .dataset import _MyDataset

def train(epochs, model : nn.Module, saved : str, 
    labels : List[str] = [TOMATO_DS_PẠTH, POTATO_DS_PATH], 
    batch_size : int = 64):
    from torch import save

    ds_train = _MyDataset(labels)
    train_lo = DataLoader(ds_train, batch_size, shuffle=True)

    losses = []
    min_loss = 1000

    for e in range(epochs):
        l = epoch(train_lo, model)
        print("Epoch = {}. Loss = {}".format(e + 1, l))
        losses.append(l)

        if min_loss > l:
            print("Tiến hành lưu trữ với l = {}".format(l))
            min_loss = l
            save(model, saved)

    # x, y = next(iter(train_lo))
    # print(x.shape)
    # print(y)
    return losses