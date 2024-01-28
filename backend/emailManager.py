import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

class EmailManager:

    def __init__(self):
        pass

    def sendEmailToCreateNewPassword(self, destination_email, code):
        msg = EmailMessage()

        origin = "cano.investments.tracker@gmail.com"
        msg['Subject'] = 'Investments Tracker - Create new password'
        msg['From'] = origin
        msg['To'] = destination_email

        msg.set_content(f"Go to https://investment-tracker.up.railway.app/new-password and use the code below.\n\n{code}")

        # Use an external SMTP server (e.g., Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create a secure SSL connection
        s = smtplib.SMTP(smtp_server, smtp_port)
        s.starttls()

        # Login to your email account
        username = origin
        password = os.getenv('EMAIL_ACCOUNT_PASSWORD')
        s.login(username, password)

        # Send the message
        s.send_message(msg)

        # Quit the SMTP session
        s.quit()


