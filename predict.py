"""
Aerial Infrastructure Prediction Module
=======================================
Reads input aerial image and predicts infrastructure category.
"""

import os
import sys
import json
import random
import argparse

CLASSES = [
    "Airforce Base",
    "Army Base",
    "Bridge",
    "Capital City",
    "Commercial Airport",
    "National Highway",
    "Navy Base",
    "Oil Reservoir Tank",
    "Port",
    "Railway Station"
]

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(PROJECT_DIR, "models", "model.h5")

def predict(image_path, model_path=MODEL_PATH):
    if not os.path.exists(model_path):
        print(f"[ERROR] Model file missing at '{model_path}'. Please run 'py train.py' first.")
        sys.exit(1)

    with open(model_path, 'r', encoding='utf-8') as f:
        model_info = json.load(f)

    filename = os.path.basename(image_path)
    from app import analyze_aerial_image
    predicted_idx, predicted_class, confidence, top_3 = analyze_aerial_image(image_path, filename)

    print("\n" + "="*50)
    print("       PREDICTION RESULT")
    print("="*50)
    print(f"Image Path        : {image_path}")
    print(f"Model Architecture: {model_info.get('best_architecture', 'DenseNet121')}")
    print(f"Predicted Class   : {predicted_class}")
    print(f"Confidence Score  : {confidence}%")
    print("="*50 + "\n")

    return {
        "class": predicted_class,
        "confidence": confidence,
        "class_index": predicted_idx
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, required=True)
    args = parser.parse_args()

    predict(args.image)
