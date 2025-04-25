import os
import torch
import torchvision
from torch.utils.data import random_split
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F

from torchvision.datasets import ImageFolder
import torchvision.transforms.v2 as transforms

import matplotlib.pyplot as plt
from torch.utils.data.dataloader import DataLoader

from torchvision.utils import make_grid

from functions import *


def show_sample(img, label):
    print("Label:", dataset.classes[label], "(Class No: "+ str(label) + ")")
    plt.imshow(img.permute(1, 2, 0))
    plt.show(block="True")

def show_batch(dl):
    for images, labels in dl:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(make_grid(images, nrow = 16).permute(1, 2, 0))
        break
    plt.show(block="True")

def plot_accuracies(history):
    accuracies = [x['val_acc'] for x in history]
    plt.plot(accuracies, '-x')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.title('Accuracy vs. No. of epochs');
    plt.show(block="True")

DEBUG = False
TRAIN = False
VAL_SPLIT = 0.4

BATCH_SIZE = 32
NUM_WORKERS = 0

data_dir  = 'NewModel/justrecycling'
test_dir = 'NewModel/test_recycling'


classes = os.listdir(data_dir)
numFiles = sum([len(files) for r, d, files in os.walk(data_dir)])
valFiles = int(numFiles * VAL_SPLIT)
trainFiles = numFiles - valFiles

if DEBUG:
    print(classes)
    print(numFiles, trainFiles, valFiles)

transformations = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])

dataset = ImageFolder(data_dir, transform = transformations)
test_ds = ImageFolder(test_dir, transform = transformations)

# img, label = dataset[12]
# show_sample(img, label)

random_seed = 42
torch.manual_seed(random_seed)
train_ds, val_ds = random_split(dataset, [trainFiles, valFiles])

train_dl = DataLoader(train_ds, batch_size = BATCH_SIZE, shuffle = True, num_workers = NUM_WORKERS, pin_memory = True)
val_dl = DataLoader(val_ds, batch_size = BATCH_SIZE*2, num_workers = NUM_WORKERS, pin_memory = True)
test_dl = DataLoader(test_ds, batch_size = BATCH_SIZE*2, num_workers = NUM_WORKERS, pin_memory = True)

if DEBUG:
    show_batch(train_dl)

model = ResNet(dataset)
device = get_default_device()
train_dl = DeviceDataLoader(train_dl, device)
val_dl = DeviceDataLoader(val_dl, device)
test_dl = DeviceDataLoader(test_dl, device)
to_device(model, device)

model = to_device(ResNet(dataset), device)
print(evaluate(model, val_dl))
print(evaluate(model, test_dl))

num_epochs = 8
opt_func = torch.optim.Adam
lr = 5.5e-5

history = fit(16, lr, model, train_dl, val_dl, opt_func)
# history += fit(2, lr, model, train_dl, test_dl, opt_func)
# history += fit(2, lr, model, train_dl, val_dl, opt_func)
# history += fit(2, lr, model, train_dl, test_dl, opt_func)
# history += fit(2, lr, model, train_dl, test_dl, opt_func)
# history = fit(num_epochs, lr, model, train_dl, test_dl, opt_func)
plot_accuracies(history)
print(evaluate(model, val_dl))
print(evaluate(model, test_dl))

input_shape = (1, 3, 640, 480)
# torch.onnx.export(model, torch.randn(input_shape), 'model.onnx', opset_version=11)
#  # Load  ONNX model
# onnx_model = onnx.load('model.onnx')
# # Convert ONNX model to TensorFlow format
# tf_model = onnx_tf.backend.prepare(onnx_model)
# # Export  TensorFlow  model 
# tf_model.export_graph("model1.tf")