import pytest
from unittest.mock import patch
from app.worker import tasks

@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123",
        "new_role": "PROFESSIONAL"
    }

@patch('app.worker.tasks.email_sender.send_verification_email')
def test_send_verification_email_task(mock_send_email, user_data):
    tasks.send_verification_email_task(user_data)
    mock_send_email.assert_called_once_with(user_data)

@patch('app.worker.tasks.email_sender.send_user_locked_email')
def test_send_user_locked_email_task(mock_send_email, user_data):
    tasks.send_user_locked_email_task(user_data)
    mock_send_email.assert_called_once_with(user_data)

@patch('app.worker.tasks.email_sender.send_user_unlocked_email')
def test_send_user_unlocked_email_task(mock_send_email, user_data):
    tasks.send_user_unlocked_email_task(user_data)
    mock_send_email.assert_called_once_with(user_data)

@patch('app.worker.tasks.email_sender.send_role_upgraded_email')
def test_send_role_upgraded_email_task(mock_send_email, user_data):
    tasks.send_role_upgraded_email_task(user_data)
    mock_send_email.assert_called_once_with(user_data)

@patch('app.worker.tasks.email_sender.send_professional_status_email')
def test_send_professional_status_email_task(mock_send_email, user_data):
    tasks.send_professional_status_email_task(user_data)
    mock_send_email.assert_called_once_with(user_data)