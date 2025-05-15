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


def save_image(image, detection=False):
    # Create images directory if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    detection_status = "deer" if detection else "frame"
    filename = f"images/{detection_status}_{timestamp}.jpg"

    # Save the image
    cv2.imwrite(filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    print(f"Image saved as {filename}")
    return filename


model = YOLO("./deer_ncnn_model", task="detect")

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
    # Save the current frame to image.png
    cv2.imwrite("image.png", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    # Run detection on the image
    results = model(image)

    # Check if anything was detected
    if len(results[0].boxes) > 0:
        consecutive_detections += 1
        print(f"WOAH - Detection {consecutive_detections}/{DETECTION_THRESHOLD}")

        # Check if we've reached the threshold and we're not in cooldown period
        current_time = time.time()
        if (
            consecutive_detections >= DETECTION_THRESHOLD
            and (current_time - last_email_time) > COOLDOWN_PERIOD
        ):
            print("Sending email notification!")
            # Save the image with deer detection
            image_path = save_image(image, detection=True)

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
    time.sleep(0.1)
