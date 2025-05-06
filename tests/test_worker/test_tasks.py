import pytest
from unittest.mock import patch
from app.worker import tasks


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123",
        "new_role": "PROFESSIONAL",
        "user_id": "11111111-1111-1111-1111-111111111111"
    }


@patch("app.worker.tasks.RealEmailSenderService.send_verification_email")
def test_send_verification_email_task(mock_send, user_data):
    tasks.send_verification_email_task(user_data)
    mock_send.assert_called_once()


@patch("app.worker.tasks.RealEmailSenderService.send_user_locked_email")
def test_send_user_locked_email_task(mock_send, user_data):
    tasks.send_user_locked_email_task(user_data)
    mock_send.assert_called_once()


@patch("app.worker.tasks.RealEmailSenderService.send_user_unlocked_email")
def test_send_user_unlocked_email_task(mock_send, user_data):
    tasks.send_user_unlocked_email_task(user_data)
    mock_send.assert_called_once()


@patch("app.worker.tasks.RealEmailSenderService.send_role_upgraded_email")
def test_send_role_upgraded_email_task(mock_send, user_data):
    tasks.send_role_upgraded_email_task(user_data)
    mock_send.assert_called_once()


@patch("app.worker.tasks.RealEmailSenderService.send_professional_status_email")
@patch("app.worker.tasks.Database.get_session_factory")
def test_send_professional_status_email_task(mock_factory, mock_send, user_data):
    class FakeUser:
        id = user_data["user_id"]
        professional_status_updated_at = "2025-05-05T00:00:00Z"

    class FakeSession:
        async def __aenter__(self): return self
        async def __aexit__(self, *a): pass
        async def get(self, model, uid): return FakeUser()
        async def commit(self): pass

    mock_factory.return_value = lambda: FakeSession()
    tasks.send_professional_status_email_task(user_data)
    mock_send.assert_called_once()