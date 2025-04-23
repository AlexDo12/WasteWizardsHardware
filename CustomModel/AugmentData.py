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



import os
from PIL import Image
import shutil
from time import strftime, localtime

TIMESTAMP = strftime('%m-%d-%Y %H•%M•%S', localtime())
TEST_FILE = "glass6.jpg.jpg"


def fileWalk(directory, destPath):
    try: 
        os.makedirs(destPath)
    except OSError:
        if not os.path.isdir(destPath):
            raise

    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file[-4:] != '.jpg':
                continue
            # print(file)
            img = Image.open(os.path.join(subdir, file))
            width, height = img.size
            left = (width - DIMENSION) / 2
            top = (height - DIMENSION) / 2
            right = width - left
            bot = height - top
            orig_img = img.crop((left, top, right, bot))
            orig_imgs = []
            for i in range(1):
                orig_imgs.append(orig_img.rotate(90 * i))

            augmented_imgs = TransformFunctions.augment_image(orig_img)
            # print(augmented_imgs)

            for i in range(len(augmented_imgs)):
                    augmented_imgs[i].save(os.path.join(destPath, file[:-4] + str(i) +".jpg"))

def main():
	prepath = os.path.join("C:/Users/Lovelace/Desktop/Waste Wizards/Project/CustomModel/split/unaugmented-train")
	glassDir = os.path.join(prepath, 'glass')
	paperDir = os.path.join(prepath, 'paper')
	cardboardDir = os.path.join(prepath, 'cardboard')
	plasticDir = os.path.join(prepath, 'plastic')
	metalDir = os.path.join(prepath, 'metal')
	trashDir = os.path.join(prepath, 'trash')
	compostDir = os.path.join(prepath, 'compost')


	destPath = os.path.join(os.getcwd(), 'dataset-augmented '+ TIMESTAMP)
	try: 
		os.makedirs(destPath)
	except OSError:
		if not os.path.isdir(destPath):
			raise

	#GLASS
	fileWalk(glassDir, os.path.join(destPath, 'glass'))

	#PAPER
	fileWalk(paperDir, os.path.join(destPath, 'paper'))

	#CARDBOARDs
	fileWalk(cardboardDir, os.path.join(destPath, 'cardboard'))

	#PLASTIC
	fileWalk(plasticDir, os.path.join(destPath, 'plastic'))

	#METAL
	fileWalk(metalDir, os.path.join(destPath, 'metal'))

	#TRASH
	fileWalk(trashDir, os.path.join(destPath, 'trash'))

	#COMPOST
	fileWalk(compostDir, os.path.join(destPath, 'compost'))  

if __name__ == '__main__':
    main()