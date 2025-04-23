import os
from PIL import Image

def find_smallest_image(directory):
    smallest_width = 100000
    smallest_height = 100000

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        # print(dirs)
        for file in files:
            # print(file)
            # Check if the file is an image by extension
            # if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(root, file)
            
            # Open the image and get its dimensions
            with Image.open(file_path) as img:
                width, height = img.size
                
                # Compare dimensions with the smallest one
                if width  < smallest_width:
                    smallest_width = width
                if height < smallest_height:
                    smallest_height = height
    
    return (smallest_width,smallest_height)

# Example usage
directory = 'C:/Users/Lovelace/Downloads/datasets/RealWaste (524x524) (Corrected)'  # Replace with your directory
smallest_image = find_smallest_image(directory)

if smallest_image:
    print(f"The smallest image dimensions are: {smallest_image[0]} x {smallest_image[1]}")
else:
    print("No images found in the directory.")
