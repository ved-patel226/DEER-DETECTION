from ultralytics import YOLO
import cv2

# 1. Load the model
model = YOLO("./deer_ncnn_model")

# Run the model on the image
results = model("deer.png", conf=0.7)

# Plot the detections on the image
plotted_img = results[0].plot()

# Save the image with detections
cv2.imwrite("deer_detections.png", plotted_img)
