import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from celery import Celery

from database.databases import get_emails, create_table_email

celery = Celery(
    'main',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


@celery.task
def send_email():
    emails = get_emails()
    for email in emails:
        print(email[3])
        # Email configuration
        sender_email = 'ruslanovrahmet@gmail.com'
        receiver_email = email[3]
        subject = email[1]
        message = email[2]

        # SMTP server configuration for gmail
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'ruslanovrahmet@gmail.com'
        smtp_password = 'cvkhnrmxfgaeqlwu'

        # Create a multipart message and set headers
        email_message = MIMEMultipart()
        email_message['From'] = sender_email
        email_message['To'] = receiver_email
        email_message['Subject'] = subject

        email_message.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            server.send_message(email_message)

        print('Success')


celery.conf.beat_schedule = {
    'send_email': {
        'task': 'celery_app.send_email',
        'schedule': 20.0
    }
}