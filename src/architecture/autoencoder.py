from torch import nn
from torch import Tensor
from ..constant import WHEIGHT, WWIDTH, CHANNEL

class AutoEncoder(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activation = nn.ReLU()

        self.linear_1 = nn.Linear(WHEIGHT * WWIDTH * CHANNEL, 512)
        self.batchnorm1 = nn.BatchNorm1d(512)
        self.linear_2 = nn.Linear(512, 512)
        self.batchnorm2 = nn.BatchNorm1d(512)

        self.linear_3 = nn.Linear(512, 256)
        self.batchnorm3 = nn.BatchNorm1d(256)
        self.linear_4 = nn.Linear(256, 512)
        self.batchnorm4 = nn.BatchNorm1d(512)

        self.linear_5 = nn.Linear(512, 512)
        self.batchnorm5 = nn.BatchNorm1d(512)
        self.linear_6 = nn.Linear(512, WHEIGHT * WWIDTH * CHANNEL)
    
    def forward(self, x : Tensor):
        x = self.linear_1(x)
        x = self.batchnorm1(x)
        x = self.activation(x)

        x = self.linear_2(x)
        x = self.batchnorm2(x)
        x = self.activation(x)

        x = self.linear_3(x)
        x = self.batchnorm3(x)
        x = self.activation(x)

        x = self.linear_4(x)
        x = self.batchnorm4(x)
        x = self.activation(x)

        x = self.linear_5(x)
        x = self.batchnorm5(x)
        x = self.activation(x)

        x = self.linear_6(x)
        return x
