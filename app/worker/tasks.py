from app.services.email_sender_service import RealEmailSenderService
from app.worker.celery_app import celery_app
from celery.utils.log import get_task_logger

email_sender = RealEmailSenderService()
logger = get_task_logger(__name__)

@celery_app.task(
    name="send_verification_email_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5},
)
def send_verification_email_task(self, user_data: dict):
    try:
        email_sender.send_verification_email(user_data)
    except Exception as e:
        logger.error(f"Failed to send verification email: {e}")
        raise

@celery_app.task(
    name="send_user_locked_email_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5},
)
def send_user_locked_email_task(self, user_data: dict):
    try:
        email_sender.send_user_locked_email(user_data)
    except Exception as e:
        logger.error(f"Failed to send locked email: {e}")
        raise

@celery_app.task(
    name="send_user_unlocked_email_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5},
)
def send_user_unlocked_email_task(self, user_data: dict):
    try:
        email_sender.send_user_unlocked_email(user_data)
    except Exception as e:
        logger.error(f"Failed to send unlocked email: {e}")
        raise

@celery_app.task(
    name="send_role_upgraded_email_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5},
)
def send_role_upgraded_email_task(self, user_data: dict):
    try:
        email_sender.send_role_upgraded_email(user_data)
    except Exception as e:
        logger.error(f"Failed to send role upgraded email: {e}")
        raise

@celery_app.task(
    name="send_professional_status_email_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5},
)
def send_professional_status_email_task(self, user_data: dict):
    try:
        email_sender.send_professional_status_email(user_data)
    except Exception as e:
        logger.error(f"Failed to send professional status email: {e}")
        raise
