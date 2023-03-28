import sys
sys.path.append("./")

from torch import load
from torch import nn
from torch.utils.data import DataLoader

from src.train import _AutoEncoderDataset
from src.architecture.autoencoder import AutoEncoder
from src.constant import *

mse_loss = nn.MSELoss()
storage = "auc_garbage.pt"
classification = AutoEncoder()
classification.to(device)

from src.train import train
train(100, classification, storage, 
    loss=mse_loss, _dataset = _AutoEncoderDataset, 
    reshape=False, labels=[METAL_DS_PATH, NYLON_DS_PATH]
)