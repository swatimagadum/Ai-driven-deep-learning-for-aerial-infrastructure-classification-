"""
Dataset Generator Utility Script
=================================
Generates real .jpg image files inside dataset/ subfolders for all 10 classes
so you can view actual JPG images in your Windows File Explorer and VS Code.
"""

import os
from PIL import Image, ImageDraw

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")

CLASSES = [
    ("Airforce Base", (0, 242, 254), "Fighter Hangar"),
    ("Army Base", (255, 0, 127), "Barracks Compound"),
    ("Bridge", (0, 255, 136), "River Suspension Bridge"),
    ("Capital City", (245, 158, 11), "Urban Skyline"),
    ("Commercial Airport", (139, 92, 246), "Paved Runway Tarmac"),
    ("National Highway", (236, 72, 153), "Interstate Expressway"),
    ("Navy Base", (59, 130, 246), "Naval Warship Dock"),
    ("Oil Reservoir Tank", (20, 184, 166), "Petroleum Tanks"),
    ("Port", (99, 102, 241), "Container Shipping Port"),
    ("Railway Station", (244, 63, 94), "Train Station Tracks")
]

def create_dataset_jpg_images(num_samples_per_class=15):
    print(f"[INFO] Setting up dataset directories at: {DATASET_DIR}")
    os.makedirs(DATASET_DIR, exist_ok=True)
    
    total_images = 0
    width, height = 224, 224

    for class_name, color, label_text in CLASSES:
        class_folder = os.path.join(DATASET_DIR, class_name)
        os.makedirs(class_folder, exist_ok=True)

        for i in range(num_samples_per_class):
            img = Image.new('RGB', (width, height), color=(13, 19, 35))
            draw = ImageDraw.Draw(img)

            # Draw outer border & distinct shapes
            draw.rectangle([10, 10, width-10, height-10], outline=color, width=3)
            draw.ellipse([60, 60, width-60, height-60], fill=color)

            # Text labels
            draw.text((20, 25), f"{class_name}", fill=(255, 255, 255))
            draw.text((20, height - 35), f"Sample #{i+1}", fill=(148, 163, 184))

            img_path = os.path.join(class_folder, f"sample_{i+1}.jpg")
            img.save(img_path, format='JPEG')
            total_images += 1

    print(f"\n[SUCCESS] Generated {total_images} real .jpg images across all 10 classes in dataset/\n")

if __name__ == "__main__":
    create_dataset_jpg_images(15)
