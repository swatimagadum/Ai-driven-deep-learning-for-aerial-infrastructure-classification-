"""
Sample Generator for ALL 10 Infrastructure Classes
===================================================
Generates high-resolution sample test images for all 10 categories
inside sample_test_images/ so the user can test uploading every class.
"""

import os
from PIL import Image, ImageDraw

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DIR = os.path.join(PROJECT_DIR, "sample_test_images")
os.makedirs(SAMPLE_DIR, exist_ok=True)

CLASSES = [
    ("sample_airforce_base.jpg", "Airforce Base", (0, 242, 254), "Fighter Jet Runway Hangar"),
    ("sample_army_base.jpg", "Army Base", (255, 0, 127), "Military Barracks Compound"),
    ("sample_bridge.jpg", "Bridge", (0, 255, 136), "Suspension Highway Bridge River"),
    ("sample_capital_city.jpg", "Capital City", (245, 158, 11), "Urban Skyline Dense Buildings"),
    ("sample_commercial_airport.jpg", "Commercial Airport", (139, 92, 246), "Paved Runway Tarmac Planes"),
    ("sample_national_highway.jpg", "National Highway", (236, 72, 153), "Interstate Expressway Lanes"),
    ("sample_navy_base.jpg", "Navy Base", (59, 130, 246), "Naval Docks Warships Sea"),
    ("sample_oil_reservoir_tank.jpg", "Oil Reservoir Tank", (20, 184, 166), "Circular Petroleum Tanks"),
    ("sample_port.jpg", "Port", (99, 102, 241), "Maritime Container Docks Ships"),
    ("sample_railway_station.jpg", "Railway Station", (244, 63, 94), "Train Tracks Station Platform")
]

def generate_10_samples():
    width, height = 400, 400
    for filename, title, color, desc in CLASSES:
        img = Image.new('RGB', (width, height), color=(13, 19, 35))
        draw = ImageDraw.Draw(img)

        # Draw outer border
        draw.rectangle([10, 10, width-10, height-10], outline=color, width=4)
        
        # Center shapes
        draw.rectangle([40, 40, width-40, height-40], outline=(51, 65, 85), width=2)
        draw.ellipse([100, 100, width-100, height-100], fill=color)

        # Text Overlay
        draw.text((width // 2 - 60, 50), "AERIAL SATELLITE", fill=(148, 163, 184))
        draw.text((width // 2 - 70, height - 70), title.upper(), fill=(255, 255, 255))
        draw.text((width // 2 - 80, height - 45), desc, fill=color)

        out_path = os.path.join(SAMPLE_DIR, filename)
        img.save(out_path, format='JPEG')
        print(f"[SUCCESS] Generated test image: {out_path}")

if __name__ == "__main__":
    generate_10_samples()
