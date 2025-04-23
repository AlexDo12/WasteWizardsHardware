import PIL
import torch 
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import sys
import torchvision.transforms.v2 as T
import TransformFunctions


GLASS = 0
PAPER = 1
CARDBOARD = 2
PLASTIC = 3
METAL = 4
TRASH = 5
COMPOST = 6
DIMENSION = 480

img_path = 'C:/Users/Lovelace/Desktop/Waste Wizards/Project/CustomModel/split/test/glass/image-584.png'
orig_img = Image.open(Path(img_path))
orig_img = orig_img.resize((DIMENSION,DIMENSION))

width, height = orig_img.size
left = (width-DIMENSION)/2
top = (height-DIMENSION)/2
right = width-left
bot = height-top
orig_img = orig_img.crop((left,top,right,bot))

orig_imgs = []
for i in range(4):
    orig_imgs.append(orig_img.rotate(90*i))

augmented_imgs = []
for i in range(4):
    augmented_imgs.append(TransformFunctions.augment_image(orig_imgs[i]))



fig, axes = plt.subplots(len(augmented_imgs), len(augmented_imgs[0]), figsize=(10,5))


for i in range(len(augmented_imgs)):
    for j in range(len(augmented_imgs[i])):
        axes[i][j].imshow(augmented_imgs[i][j])
plt.show()
