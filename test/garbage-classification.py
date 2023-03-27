import sys
sys.path.append("./")

from torch import load
from torch import nn
from torch.utils.data import DataLoader

from src.train import _MyDataset
from src.preprocess import running_transform
from src.architecture.classify import Classification
from src.constant import *

ds_train = _MyDataset([METAL_DS_PATH, NYLON_DS_PATH], running_transform)
test = DataLoader(ds_train, 1)
storage = "garbage.pt"
# classification : nn.Module = load(storage)
classification = Classification()
classification.to(device)
classification.eval()

x, y = next(iter(test))
x = x.to(device)
y_hat = classification.forward(x)

print("------------------------------------------------------------------")
print("Nhãn tương ứng : ", end = "")
print(ds_train.labels)
print("Dự đoán nhãn : {:.2f}".format(y_hat.item()))
print("Nhãn chuẩn là : {}".format(y.item()))
print("------------------------------------------------------------------")

from src.train import train
train(50, classification, storage, labels=[METAL_DS_PATH, NYLON_DS_PATH])
from src.train import accuracy

per = accuracy(classification, ds_train)
print("Độ chính xác của mô hình dự đoán là {:.2f}%".format(per * 100))