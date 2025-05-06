from app.services.email_sender_service import RealEmailSenderService
from app.worker.celery_app import celery_app
from celery.utils.log import get_task_logger
from app.models.user_model import User
from app.database import Database
import asyncio

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
        email_sender = RealEmailSenderService()
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
        email_sender = RealEmailSenderService()
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
        email_sender = RealEmailSenderService()
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
        email_sender = RealEmailSenderService()
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
    async def _handle_email():
        session_factory = Database.get_session_factory()
        async with session_factory() as session:
            try:
                user = await session.get(User, user_data.get("user_id"))
                if not user:
                    logger.error("User not found. Skipping email.")
                    return

                if user.professional_status_updated_at is None:
                    logger.info(f"Skipping duplicate email for user {user.id}")
                    return

                user.professional_status_updated_at = None
                await session.commit()

                email_sender = RealEmailSenderService()
                email_sender.send_professional_status_email(user_data)

            except Exception as e:
                logger.error(f"Failed to send professional status email: {e}")
                raise

    asyncio.run(_handle_email())

__all__ = ["email_sender"]