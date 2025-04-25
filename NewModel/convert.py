import ai_edge_torch
import numpy
import torch
from functions import ResNet
from torchvision.datasets import ImageFolder
import torchvision.transforms.v2 as transforms

device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
dataset = ImageFolder("justrecycling", transform=transforms.ToTensor())
model = ResNet(dataset)

# for param in model.parameters():
#     param.requires_grad = False


# num_ftrs = model.fc.in_features
# model.fc = nn.Linear(num_ftrs, 3)
# model = model.to(device)


model.load_state_dict(torch.load("model1.pt"))
sample_inputs = (torch.randn(1, 3, 640, 480),)
tfl_model = ai_edge_torch.convert(model.eval(), sample_inputs)

tfl_model.export("model1.tflite")