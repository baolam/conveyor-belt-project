from tqdm import tqdm
from torch import nn
from torch.utils.data import Dataset, DataLoader

from ..constant import *

def accuracy(model : nn.Module, dataset : Dataset, threshold : float = 0.5):
    loader = DataLoader(dataset, 1)
    model.to(device)

    total_num = 0
    for x, y in tqdm(loader):
        x = x.to(device)
        y_hat = model.forward(x)

        label = 0
        if y_hat.item() > threshold:
            label = 1
        
        if label == y.item():
            total_num += 1

    return total_num / len(dataset)
