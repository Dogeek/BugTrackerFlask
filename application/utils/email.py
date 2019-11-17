import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .. import app


def send_email(to, subject, content):
    if app.config["DEBUG"]:
        print(f"To : {to}\nSubject: {subject}\n\n{content}")
        return
    port = 465  # For SSL
    smtp_server = app.config["SMTP_EMAIL_SERVER"]
    sender_email = app.config["SMTP_EMAIL_SENDER"]
    password = app.config["SMTP_EMAIL_PASSWORD"]

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to
    content = MIMEText(content, "html")
    message.attach(content)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to, message.as_string())
