from tqdm import tqdm
from torch.utils.data import DataLoader
from torch import nn
from torch import optim
from torch import float32

from ..constant import *

def epoch(train : DataLoader, model : nn.Module, loss_func, 
        reshape : bool):
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    model.to(device)

    loss = 0
    c = 0
    for x, y in tqdm(train):
        x = x.to(device)
        y = y.to(dtype=float32, device=device)
        y_hat = model.forward(x)
        if reshape:
            y_hat = y_hat.reshape(-1)

        optimizer.zero_grad()

        l = loss_func(y_hat, y)
        l.backward()

        optimizer.step()

        loss += l.item()
        c += 1

    return loss / c 