"""
Sample Image Exporter
=====================
Copies generated high-res aerial sample test images into sample_test_images/ folder
for easy user upload testing.
"""

import os
import shutil

SOURCE_DIR = r"C:\Users\keert\.gemini\antigravity\brain\07048df3-a7fb-44ce-a9cc-db041cbd9418"
TARGET_DIR = r"C:\Users\keert\.gemini\antigravity\scratch\aerial_infrastructure_classification\sample_test_images"

os.makedirs(TARGET_DIR, exist_ok=True)

files_to_copy = {
    "aerial_bridge_sample_1785401031948.jpg": "sample_bridge.jpg",
    "aerial_airport_sample_1785401102832.jpg": "sample_airport.jpg",
    "aerial_port_sample_1785401121464.jpg": "sample_port.jpg"
}

for src_name, dst_name in files_to_copy.items():
    src_path = os.path.join(SOURCE_DIR, src_name)
    dst_path = os.path.join(TARGET_DIR, dst_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)
        print(f"Copied {src_name} -> {dst_path}")
