import pytest
from unittest.mock import patch
from app.services.email_sender_service import RealEmailSenderService

@patch('smtplib.SMTP')
def test_send_email_success(mock_smtp):
    sender = RealEmailSenderService()
    sender.send_email('Test Subject', 'test@example.com', 'Test Body')

    mock_smtp.assert_called_once_with(sender.smtp_server, sender.smtp_port)
    instance = mock_smtp.return_value.__enter__.return_value
    instance.starttls.assert_called_once()
    instance.login.assert_called_once_with(sender.smtp_username, sender.smtp_password)
    instance.sendmail.assert_called_once()

@patch('smtplib.SMTP')
def test_send_verification_email(mock_smtp):
    sender = RealEmailSenderService()
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify"
    }
    sender.send_verification_email(user_data)
    instance = mock_smtp.return_value.__enter__.return_value
    instance.sendmail.assert_called_once()

@patch('smtplib.SMTP')
def test_send_user_locked_email(mock_smtp):
    sender = RealEmailSenderService()
    user_data = {"email": "test@example.com", "name": "Test User"}
    sender.send_user_locked_email(user_data)
    instance = mock_smtp.return_value.__enter__.return_value
    instance.sendmail.assert_called_once()

@patch('smtplib.SMTP')
def test_send_user_unlocked_email(mock_smtp):
    sender = RealEmailSenderService()
    user_data = {"email": "test@example.com", "name": "Test User"}
    sender.send_user_unlocked_email(user_data)
    instance = mock_smtp.return_value.__enter__.return_value
    instance.sendmail.assert_called_once()

@patch('smtplib.SMTP')
def test_send_role_upgraded_email(mock_smtp):
    sender = RealEmailSenderService()
    user_data = {"email": "test@example.com", "name": "Test User", "new_role": "PROFESSIONAL"}
    sender.send_role_upgraded_email(user_data)
    instance = mock_smtp.return_value.__enter__.return_value
    instance.sendmail.assert_called_once()

@patch('smtplib.SMTP')
def test_send_professional_status_email(mock_smtp):
    sender = RealEmailSenderService()
    user_data = {"email": "test@example.com", "name": "Test User"}
    sender.send_professional_status_email(user_data)
    instance = mock_smtp.return_value.__enter__.return_value
    instance.sendmail.assert_called_once()