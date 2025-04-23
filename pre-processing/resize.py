
GLASS = 0
PAPER = 1
CARDBOARD = 2
PLASTIC = 3
METAL = 4
TRASH = 5
COMPOST = 6

WIDTH = 524
HEIGHT = 524



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
			if(width == WIDTH and height == HEIGHT):
				shutil.copyfile(os.path.join(subdir, file), os.path.join(destPath, file))
				continue
			scale = max(WIDTH/width, HEIGHT/height)
			img.thumbnail((width*scale, height*scale))
			width, height = img.size

			left = (width-WIDTH)/2
			top = (height-HEIGHT)/2
			right = width-left
			bot = height-top
			cropped = img.crop((left,top,right,bot))

			# if (file == TEST_FILE):
			# 	print(file)
			# 	print("width: " + str(width) + " height: " + str(height))
			# 	print(left, top, right, bot)
			# 	img.save(os.path.join(destPath, file + "thumbnail.jpg"))

			cropped.save(os.path.join(destPath, file))
		

def main():
	prepath = os.path.join("C:/Users/Lovelace/Downloads/TrashNet (Full Size, Corrected)")
	glassDir = os.path.join(prepath, 'glass')
	paperDir = os.path.join(prepath, 'paper')
	cardboardDir = os.path.join(prepath, 'cardboard')
	plasticDir = os.path.join(prepath, 'plastic')
	metalDir = os.path.join(prepath, 'metal')
	trashDir = os.path.join(prepath, 'trash')
	compostDir = os.path.join(prepath, 'compost')


	destPath = os.path.join(os.getcwd(), 'dataset-resized '+TIMESTAMP)
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