import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


def send_email_alert(subject: str, body: str):
    load_dotenv()
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT", "587")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    from_email = os.getenv("FROM_EMAIL") or smtp_user
    to_email = os.getenv("TO_EMAIL")

    if not (smtp_server and smtp_user and smtp_pass and to_email):
        return False, "Missing SMTP configuration in .env"

    try:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        port = int(smtp_port)
        with smtplib.SMTP(smtp_server, port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True, "Email sent"
    except Exception as e:
        return False, str(e)
