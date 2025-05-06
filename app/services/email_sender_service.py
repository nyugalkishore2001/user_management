import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings.config import settings

logger = logging.getLogger(__name__)

class RealEmailSenderService:
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password

    def send_email(self, subject, recipient_email, body):
        message = MIMEMultipart()
        message["From"] = self.smtp_username
        message["To"] = recipient_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(
                    self.smtp_username,
                    recipient_email,
                    message.as_string()
                )
            logger.info(f"✅ Email sent successfully to {recipient_email} with subject '{subject}'")
        except Exception as e:
            logger.error(f"❌ Failed to send email to {recipient_email} with subject '{subject}': {e}")
            raise

    def send_verification_email(self, user_data):
        subject = "Verify Your Account"
        body = f"Hello {user_data['name']},\n\nPlease verify your email: {user_data['verification_url']}"
        self.send_email(subject, user_data['email'], body)

    def send_user_locked_email(self, user_data):
        subject = "Account Locked"
        body = f"Hello {user_data['name']},\n\nYour account has been locked due to multiple failed login attempts."
        self.send_email(subject, user_data['email'], body)

    def send_user_unlocked_email(self, user_data):
        subject = "Account Unlocked"
        body = f"Hello {user_data['name']},\n\nYour account has been unlocked. You can now log in again."
        self.send_email(subject, user_data['email'], body)

    def send_role_upgraded_email(self, user_data):
        subject = "Role Upgraded"
        body = f"Congratulations!\n\nYour role has been upgraded to {user_data.get('new_role')}."
        self.send_email(subject, user_data['email'], body)

    def send_professional_status_email(self, user_data):
        subject = "Professional Status Granted"
        body = f"Hello {user_data['name']},\n\nYou have been upgraded to professional status. Enjoy new features!"
        self.send_email(subject, user_data['email'], body)
