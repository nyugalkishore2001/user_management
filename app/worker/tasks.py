from app.services.email_sender_service import RealEmailSenderService
from app.worker.celery_app import celery_app

email_sender = RealEmailSenderService()

@celery_app.task(name="send_verification_email_task", bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def send_verification_email_task(self, user_data: dict):
    email_sender.send_verification_email(user_data)

@celery_app.task(name="send_user_locked_email_task", bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def send_user_locked_email_task(self, user_data: dict):
    email_sender.send_user_locked_email(user_data)

@celery_app.task(name="send_user_unlocked_email_task", bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def send_user_unlocked_email_task(self, user_data: dict):
    email_sender.send_user_unlocked_email(user_data)

@celery_app.task(name="send_role_upgraded_email_task", bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def send_role_upgraded_email_task(self, user_data: dict):
    email_sender.send_role_upgraded_email(user_data)

@celery_app.task(name="send_professional_status_email_task", bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def send_professional_status_email_task(self, user_data: dict):
    email_sender.send_professional_status_email(user_data)