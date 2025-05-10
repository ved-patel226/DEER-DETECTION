from deer import send
import os
import ast
from ultralytics import YOLO
import time
import picamera2


def get_emails():
    return ast.literal_eval(os.environ["EMAILS"])


model = YOLO("runs/train/deer_database3/weights/best_ncnn_model", task="detect")

# Initialize the camera
camera = picamera2.Picamera2()
camera_config = camera.create_preview_configuration(main={"size": (1920, 1080)})
camera.configure(camera_config)
camera.start()

# Give the camera a moment to initialize
time.sleep(2)

while True:
    # Capture an image
    image = camera.capture_array()

    # Run detection on the image
    results = model(image)

    # Check if anything was detected
    if len(results[0].boxes) > 0:
        print("WOAH")

    # Small delay to avoid high CPU usage
    time.sleep(5)
