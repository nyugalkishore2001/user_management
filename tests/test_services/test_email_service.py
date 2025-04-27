import pytest
from unittest.mock import patch
from app.services.email_service import EmailService

@pytest.fixture
def email_service_instance():
    return EmailService()

@pytest.mark.asyncio
@patch('app.services.email_service.publish_event')
async def test_send_verification_email(mock_publish_event, email_service_instance):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify"
    }
    await email_service_instance.send_verification_email(user_data)

    mock_publish_event.assert_called_once()
    args, kwargs = mock_publish_event.call_args
    assert kwargs["key"] == "account_verification"
    assert "verification_url" in kwargs["value"]

@pytest.mark.asyncio
@patch('app.services.email_service.publish_event')
async def test_send_user_locked_email(mock_publish_event, email_service_instance):
    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }
    await email_service_instance.send_user_locked_email(user_data)

    mock_publish_event.assert_called_once()
    args, kwargs = mock_publish_event.call_args
    assert kwargs["key"] == "account_locked"

@pytest.mark.asyncio
@patch('app.services.email_service.publish_event')
async def test_send_user_unlocked_email(mock_publish_event, email_service_instance):
    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }
    await email_service_instance.send_user_unlocked_email(user_data)

    mock_publish_event.assert_called_once()
    args, kwargs = mock_publish_event.call_args
    assert kwargs["key"] == "account_unlocked"

@pytest.mark.asyncio
@patch('app.services.email_service.publish_event')
async def test_send_role_upgraded_email(mock_publish_event, email_service_instance):
    user_data = {
        "email": "test@example.com",
        "new_role": "PROFESSIONAL"
    }
    await email_service_instance.send_role_upgraded_email(user_data)

    mock_publish_event.assert_called_once()
    args, kwargs = mock_publish_event.call_args
    assert kwargs["key"] == "role_upgrade"

@pytest.mark.asyncio
@patch('app.services.email_service.publish_event')
async def test_send_professional_status_email(mock_publish_event, email_service_instance):
    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }
    await email_service_instance.send_professional_status_email(user_data)

    mock_publish_event.assert_called_once()
    args, kwargs = mock_publish_event.call_args
    assert kwargs["key"] == "professional_status_upgrade"