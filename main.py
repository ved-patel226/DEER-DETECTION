from deer import send
import os
import ast
from ultralytics import YOLO
import time
import picamera2
import cv2
from datetime import datetime
from libcamera import controls


def get_emails():
    return ast.literal_eval(os.environ["EMAILS"])


def save_image(image):
    filename = f"image.jpg"

    cv2.imwrite(filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    print(f"Image saved as {filename}")
    return filename


model = YOLO("./deer_ncnn_model", task="detect", verbose=False)

# Initialize the camera
camera = picamera2.Picamera2()
camera_config = camera.create_preview_configuration(main={"size": (1920, 1080)})
camera.configure(camera_config)

# Enable continuous autofocus
camera.start()

camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

# Give the camera a moment to initialize
time.sleep(2)


# Detection threshold settings
DETECTION_THRESHOLD = 3  # Number of consecutive detections needed
COOLDOWN_PERIOD = 300  # Seconds (5 minutes) before sending another email

consecutive_detections = 0
last_email_time = 0


while True:
    # Capture an image
    image = camera.capture_array()
    results = model(image, verbose=False)

    # Check if anything was detected
    if len(results[0].boxes) > 0:
        consecutive_detections += 1

        current_time = time.time()

        print(
            f"Detection {consecutive_detections}/{DETECTION_THRESHOLD}"
            if (current_time - last_email_time) < COOLDOWN_PERIOD
            else "Detected, but cool-down period active"
        )

        # Check if we've reached the threshold and we're not in cooldown period
        if (
            consecutive_detections >= DETECTION_THRESHOLD
            and (current_time - last_email_time) > COOLDOWN_PERIOD
        ):
            print("Sending email notification!")
            # Save the image with deer detection
            # Get image with detection boxes drawn on it
            annotated_image = results[0].plot()  # Draw detection boxes on the image
            image_path = save_image(annotated_image)

            emails = get_emails()
            send.send_email(emails, image=image)
            last_email_time = current_time
            # Reset counter after sending email
            consecutive_detections = 0
    else:
        print("No detections")
        # Reset counter when no detection occurs
        consecutive_detections = 0

    # Optional: Save periodic frames regardless of detection
    # Uncomment if you want to save all frames
    # if time.time() % 60 < 1:  # Save a frame roughly every minute
    #     save_image(image)

    # Short delay to prevent CPU overload
    time.sleep(2)
