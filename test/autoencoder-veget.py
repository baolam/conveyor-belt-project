import sys
sys.path.append("./")

from torch import load
from torch import nn
from torch.utils.data import DataLoader

from src.train import _AutoEncoderDataset
from src.architecture.autoencoder import AutoEncoder
from src.constant import *

mse_loss = nn.MSELoss()
storage = "auc_veget.pt"
# classification = AutoEncoder()
classification = load(storage)
classification.to(device)
labels = [TOMATO_DS_PẠTH, POTATO_DS_PATH]
dataset = _AutoEncoderDataset(labels)
loader = DataLoader(dataset, 1)
classification.eval()

# from src.train import train
# train(50, classification, storage, 
#     loss=mse_loss, _dataset = _AutoEncoderDataset, 
#     reshape=False, labels=labels
# )

from matplotlib import pyplot as plt

x, y = next(iter(loader))
x = x.to(device)
y = y.to(device)
y_hat = classification.forward(x)

y = y.reshape((CHANNEL, WHEIGHT, WWIDTH))
y_hat = y_hat.reshape((CHANNEL, WHEIGHT, WWIDTH))

import numpy as np
# plt.imshow(np.array(y).transpose(1, 2, 0))
# plt.imshow(np.array(y_hat.cpu().detach()).transpose(1, 2, 0))
# plt.xticks([])
# plt.yticks([])
# plt.show()
loss = mse_loss(y_hat, y)
print(loss.item())

rows, cols = 1, 2
fig = plt.figure(figsize=(10, 7))

fig.add_subplot(rows, cols, 1)
plt.imshow(np.array(y.cpu().detach()).transpose(1, 2, 0))

fig.add_subplot(rows, cols, 2)
plt.imshow(np.array(y_hat.cpu().detach()).transpose(1, 2, 0))

plt.show()