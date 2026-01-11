import os
import smtplib
from email.message import EmailMessage


def send_email(subject: str, body: str) -> None:
    sender = os.getenv("HEALTHIT_SENDER_EMAIL", "").strip()
    receiver = os.getenv("HEALTHIT_RECEIVER_EMAIL", "").strip()
    password = os.getenv("HEALTHIT_GMAIL_APP_PASSWORD", "").strip()

    if not sender or not receiver or not password:
        raise RuntimeError(
            "Missing email config. Set HEALTHIT_SENDER_EMAIL, HEALTHIT_RECEIVER_EMAIL, "
            "and HEALTHIT_GMAIL_APP_PASSWORD in your local .env file."
        )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
