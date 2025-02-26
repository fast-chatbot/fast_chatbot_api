import random
import smtplib
import ssl

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
    print(receiver_email)
    print(otp)
    settings = get_settings()

    smtp_server = settings['smtp_server']
    smtp_port = settings['smtp_port']
    smtp_username = settings['smtp_username']
    smtp_password = settings['smtp_password']

    sender_email = settings['smtp_username']
    subject = 'Проверочный код'
    body = f'Код для авторизации:\n\n{otp}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    print(000)
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Письмо успешно отправлено.")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")

    # with smtplib.SMTP_SSL(smtp_server, 465) as server:
    #     server.login(smtp_username, smtp_password)
    #     server.sendmail(sender_email, receiver_email, msg.as_string())



# Thank you for waiting.
# For the outgoing configuration, please use:
#
# smtp.dreamhost.com
# Port 587 with SSL or  STARTTLS