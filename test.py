from ultralytics import YOLO
import cv2
import os
from pathlib import Path
import time

# 1. Load the model
model = YOLO("./deer_ncnn_model", verbose=False)

INPUT_PATH = Path("./images")
OUTPUT_PATH = Path("./images_detected")

input_files = os.listdir(INPUT_PATH)
os.makedirs(OUTPUT_PATH, exist_ok=True)

for file in input_files:
    try:
        # Run the model on the image using string path instead of Path object
        input_path = str(INPUT_PATH / file)
        output_path = str(OUTPUT_PATH / file)

        # Run the model on the image
        results = model(input_path, conf=0.7, verbose=False)

        # Plot the detections on the image
        plotted_img = results[0].plot()

        # Save the image with detections
        cv2.imwrite(output_path, plotted_img)
    except:
        print("Failed to save file")
