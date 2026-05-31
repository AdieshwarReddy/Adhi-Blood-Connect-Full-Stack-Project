import asyncio
from app.core.logger import logger

async def send_email_notification_task(email: str, subject: str, body: str):
    """
    Background worker simulating SMTP server connection to send HTML email notifications.
    """
    logger.info(f"Background task started: Sending email notification to {email}...")
    try:
        # Simulate network I/O
        await asyncio.sleep(2)
        logger.info(f"Email successfully dispatched to {email}. Subject: '{subject}'")
    except Exception as e:
        logger.error(f"Failed to dispatch email to {email}: {str(e)}")

async def send_sms_alert_task(phone_number: str, message: str):
    """
    Background worker simulating a Twilio/SMS gateway API client request.
    """
    logger.info(f"Background task started: Sending emergency SMS alert to {phone_number}...")
    try:
        # Simulate network I/O
        await asyncio.sleep(1.5)
        logger.info(f"SMS alert successfully broadcasted to {phone_number}.")
    except Exception as e:
        logger.error(f"Failed to transmit SMS alert to {phone_number}: {str(e)}")

async def send_donor_reminder_task(donor_id: str, donor_email: str):
    """
    Background task to notify eligible donors that their 90-day cooldown period has ended.
    """
    logger.info(f"Background task started: Scheduling donor reminder for Donor ID '{donor_id}'...")
    try:
        await asyncio.sleep(1)
        logger.info(f"Donor cooldown completion notice sent to {donor_email}.")
    except Exception as e:
        logger.error(f"Error executing cooldown reminder for {donor_email}: {str(e)}")

async def run_inactive_donor_cleanup_task():
    """
    Mock cron job performing automated batch cleaning of outdated accounts or state logs.
    """
    logger.info("Background task started: Cleaning up inactive database records...")
    try:
        await asyncio.sleep(3)
        logger.info("Inactive database record cleanup complete.")
    except Exception as e:
        logger.error(f"Error running database cleanup: {str(e)}")
