import os
import pandas as pd
from PIL import Image
from io import BytesIO

classes = ["compost", "cardboard", "glass", "metal", "paper", "plastic", "trash"]

WIDTH = 512
HEIGHT = 384

# Directories
input_dir = 'C:/Users/Lovelace/Downloads/trashnet_enhanced/data'
output_dir = 'C:/Users/Lovelace/Downloads/trashnet_enhanced/images'

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

# Process Parquet files
for filename in os.listdir(input_dir):
    if filename.endswith('.parquet'):
        file_path = os.path.join(input_dir, filename)
        df = pd.read_parquet(file_path)
        # print(df)
        # break

        # Assuming columns: 'image_data' (bytes) and 'classification' (string)
        for index, row in df.iterrows():
            image_data = row['image.bytes']
            classification = classes[row['label']]
            img_filename = row["image.path"].split('_')[0]
            img_filename = img_filename.replace("biodegradable","compost")

            # Ensure classification folder exists
            class_dir = os.path.join(output_dir, classification)
            os.makedirs(class_dir, exist_ok=True)

            # Convert image data to JPG
            image = Image.open(BytesIO(image_data))
            image_path = os.path.join(class_dir, img_filename+".jpg")
            image.save(image_path, 'JPEG')

            print(f"Saved: {image_path}")

print("All images have been exported.")
