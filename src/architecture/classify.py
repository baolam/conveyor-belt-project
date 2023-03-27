from torch import nn
from torch import Tensor

class Classification(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.conv1 = nn.Conv2d(3, 16, (2, 2))
        self.conv2 = nn.Conv2d(16, 16, (2, 2))
        
        self.conv3 = nn.Conv2d(16, 16, (2, 2))
        self.conv4 = nn.Conv2d(16, 16, (2, 2))

        self.max = nn.MaxPool2d((3, 3))
        self.activate = nn.ReLU()
        self.probs = nn.Sigmoid()

        self.line1 = nn.Linear(576, 128)
        self.batch1 = nn.BatchNorm1d(128)
        self.line2 = nn.Linear(128, 128)
        self.batch2 = nn.BatchNorm1d(128)
        self.line3 = nn.Linear(128, 1)

    def __feature_extraction(self, x : Tensor):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.activate(x)
        x = self.max(x)

        x = self.conv3(x)
        x = self.conv4(x)
        x = self.activate(x)
        x = self.max(x)

        x = x.reshape((x.size()[0], -1))
        return x

    def __classify(self, x : Tensor):
        x = self.line1(x)
        x = self.batch1(x)
        x = self.activate(x)

        x = self.line2(x)
        x = self.batch2(x)
        x = self.activate(x)

        x = self.line3(x)
        x = self.probs(x)

        return x

    def forward(self, x : Tensor):
        x = self.__feature_extraction(x)
        x = self.__classify(x)
        return x