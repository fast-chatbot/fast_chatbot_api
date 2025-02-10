import random
import smtplib

from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import get_settings

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    settings = get_settings()
    encode_jwt = jwt.encode(to_encode, settings['secret_key'], algorithm=settings['algorithm'])

    return encode_jwt


def generate_otp() -> str:
    otp = random.randint(100000, 999999)

    return str(otp)


def send_email(receiver_email: str, otp: str):
    settings = get_settings()

    smtp_server = settings['smtp_server']
    smtp_port = settings['smtp_port']
    smtp_username = settings['smtp_username']
    smtp_password = settings['smtp_password']

    sender_email = settings['smtp_username']
    receiver_email = receiver_email
    subject = 'Проверочный код'
    body = f'Код для авторизации:\n\n{otp}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

