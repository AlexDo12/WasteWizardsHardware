# This script aims to create augmented images from one image to create a larger dataset for our cnn model
# The augmentation this script will perform on each object is 
# orig_img,grayscaled_image,random_rotation_transformation_45_image,random_rotation_transformation_65_image,random_rotation_transformation_85_image,gausian_blurred_image_13_image,gausian_blurred_image_56_image,gausian_image_3,gausian_image_6,gausian_image_9,colour_jitter_image_1,colour_jitter_image_2,colour_jitter_image_3

#call the function creating file with augmented image give path of dataset and path of folder where you want the augmented images to be stored

import PIL
import torch 
from PIL import Image
from pathlib import Path
import torchvision.transforms.v2 as T
from random import sample, randint

NUM_AUGMENTS = 4

DIMENSION = 480

#torch.transforms
def addnoise(input_image, noise_factor = 0.3):
    inputs = T.ToTensor()(input_image)
    noisy = inputs + torch.rand_like(inputs) * noise_factor
    noisy = torch.clip (noisy,0,1.)
    output_image = T.ToPILImage()
    image = output_image(noisy)
    return image

data_transforms = [
    T.Compose([T.RandomRotation((20,75)),T.GaussianBlur(kernel_size = (7,13), sigma = (6 , 9))]),
    T.Compose([T.RandomRotation((20,75)),T.GaussianBlur(kernel_size = (7,13), sigma = (5 , 8))]),
    T.Compose([T.RandomRotation((20,75)),T.ColorJitter(brightness=(0.5,1.5),contrast=(3),saturation=(0.3,1.5),hue=(-0.1,0.1))]),
    T.Compose([T.RandomRotation((20,75)),T.ColorJitter(brightness=(0.7),contrast=(6),saturation=(0.9),hue=(-0.1,0.1))]),
    T.Compose([T.RandomRotation((20,75)),T.ColorJitter(brightness=(0.5,1.5),contrast=(2),saturation=(1.4),hue=(-0.1,0.5))]),
    T.Compose([T.RandomRotation((20,75)),T.Grayscale(3)])   
]




#Random invert
random_invert_transform = T.RandomInvert(1)

#Main function that calls all the above functions to create 11 augmented images from one image

def augment_image(orig_img):
    output = [orig_img]
    for transform in sample(data_transforms,NUM_AUGMENTS-1):
        output.append(transform(orig_img))
    

    random_integer = randint(1, 3)
    if(random_integer == 1):
        output.append(addnoise(orig_img,0.3))
    elif(random_integer == 2):
        output.append(addnoise(orig_img,0.6))
    else:
        output.append(addnoise(orig_img,0.9))
    return (output)