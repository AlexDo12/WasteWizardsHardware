import os
import shutil
import random
from pathlib import Path

def split_dataset(
    input_dir,
    output_dir,
    split_ratio=0.8,
    seed=42
):
    random.seed(seed)
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    train_dir = output_dir / "train"
    val_dir = output_dir / "val"

    if not input_dir.exists():
        raise ValueError(f"Input directory {input_dir} does not exist")

    # Create output directories
    for split in [train_dir, val_dir]:
        split.mkdir(parents=True, exist_ok=True)

    for class_dir in input_dir.iterdir():
        if class_dir.is_dir():
            images = list(class_dir.glob("*.*"))
            random.shuffle(images)
            split_point = int(len(images) * split_ratio)
            train_images = images[:split_point]
            val_images = images[split_point:]

            # Create class subdirectories
            (train_dir / class_dir.name).mkdir(parents=True, exist_ok=True)
            (val_dir / class_dir.name).mkdir(parents=True, exist_ok=True)

            # Copy files
            for img in train_images:
                shutil.copy(img, train_dir / class_dir.name / img.name)
            for img in val_images:
                shutil.copy(img, val_dir / class_dir.name / img.name)

            print(f"Class '{class_dir.name}': {len(train_images)} train, {len(val_images)} val")

if __name__ == "__main__":
    # Example usage:
    split_dataset(
        input_dir="C:/Users/Lovelace/Desktop/Waste Wizards/Project/CustomModel/trashnet+compost",
        output_dir="C:/Users/Lovelace/Desktop/Waste Wizards/Project/CustomModel/output",
        split_ratio=0.8  # Change this as needed
    )
