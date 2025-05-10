import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
from email.mime.image import MIMEImage


def send_email(
    to_email,
    subject="⚠️ DEER DETECTED ⚠️",
    from_email="talk2ved11@gmail.com",
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username="talk2ved11@gmail.com",
    password=os.environ["EMAIL_APP_PASS"] if "EMAIL_APP_PASS" in os.environ else "",
    image_path=None,
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
    if image_path and os.path.isfile(image_path):
        with open(image_path, "rb") as img_file:
            img = MIMEImage(img_file.read())
            img.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(image_path),
            )
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
        "test123",
        "vedhehe292@gmail.com",
    )


if __name__ == "__main__":
    main()
