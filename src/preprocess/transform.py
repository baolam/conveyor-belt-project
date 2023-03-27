from ..constant import *
from torchvision import transforms

mean, std = (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)
training_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((WHEIGHT, WWIDTH)),
    transforms.AutoAugment(),
    transforms.ToTensor(),
    transforms.Normalize(mean, std),
    transforms.RandomAutocontrast(0.3),
    transforms.RandomVerticalFlip(0.2),
    transforms.RandomHorizontalFlip(0.2)
])

running_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((WHEIGHT, WWIDTH)),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])