from app.utils.kafka_producer import publish_event
from settings.config import settings
import json

class EmailService:
    def __init__(self):
        self.topic = settings.kafka_topic_email_notifications

    async def send_verification_email(self, user_data: dict):
        event_data = {
            "type": "account_verification",
            "email": user_data["email"],
            "name": user_data.get("name", ""),
            "verification_url": user_data.get("verification_url", "")
        }
        publish_event(self.topic, key="account_verification", value=json.dumps(event_data))

    async def send_user_locked_email(self, user_data: dict):
        event_data = {
            "type": "account_locked",
            "email": user_data["email"],
            "name": user_data.get("name", "")
        }
        publish_event(self.topic, key="account_locked", value=json.dumps(event_data))

    async def send_user_unlocked_email(self, user_data: dict):
        event_data = {
            "type": "account_unlocked",
            "email": user_data["email"],
            "name": user_data.get("name", "")
        }
        publish_event(self.topic, key="account_unlocked", value=json.dumps(event_data))

    async def send_role_upgraded_email(self, user_data: dict):
        event_data = {
            "type": "role_upgrade",
            "email": user_data["email"],
            "new_role": user_data.get("new_role", "")
        }
        publish_event(self.topic, key="role_upgrade", value=json.dumps(event_data))

    async def send_professional_status_email(self, user_data: dict):
        event_data = {
            "type": "professional_status_upgrade",
            "email": user_data["email"],
            "name": user_data.get("name", "")
        }
        publish_event(self.topic, key="professional_status_upgrade", value=json.dumps(event_data))

    async def send_user_email(self, user_data: dict, template_name: str):
        # Just a simple dummy implementation for now
        return