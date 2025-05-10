from ultralytics import YOLO


def main():
    data_yaml = "deer_database/data.yaml"
    model_cfg = "yolo11n.pt"

    # Initialize YOLO model (using ultralytics package)
    model = YOLO(model_cfg)

    # Train the model with early stopping
    model.train(
        data=data_yaml,
        epochs=100,
        imgsz=640,  # Recommended default image size
        batch=4,
        project="runs/train",
        name="deer_database",
        patience=10,  # Stop if no improvement after 10 epochs
        single_cls=True,  # Treat all classes as one (doe and buck) are the same
    )

    model.export(
        format="ncnn",
        simplify=True,
        half=True,
    )


if __name__ == "__main__":
    main()
