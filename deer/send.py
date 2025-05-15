import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
from email.mime.image import MIMEImage
import cv2
import numpy as np
import uuid


def send_email(
    to_email,
    subject="⚠️ DEER DETECTED ⚠️",
    from_email="talk2ved11@gmail.com",
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username="talk2ved11@gmail.com",
    password=os.environ.get("EMAIL_APP_PASS", ""),
    image=None,
):
    if isinstance(to_email, str):
        to_email = [to_email]

    user_friendly_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = ", ".join(to_email)
    msg["Subject"] = subject

    msg.attach(MIMEText(f"<h1>DEER DETECTED @ {user_friendly_time}</h1>", "html"))

    # Attach image if provided
    if image is not None:
        # Convert numpy array to image bytes
        if isinstance(image, np.ndarray):
            # Convert to BGR format if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                image_to_send = cv2.imencode(".jpg", image)[1].tobytes()
            else:
                print(
                    "Warning: Image format not recognized, attempting to encode anyway"
                )
                image_to_send = cv2.imencode(".jpg", image)[1].tobytes()

            img = MIMEImage(image_to_send)
            filename = f"deer_detected_{int(time.time())}.jpg"
            img.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(img)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def main() -> None:
    send_email(
        "vedhehe292@gmail.com",
    )


if __name__ == "__main__":
    main()
