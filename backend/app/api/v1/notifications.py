from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.services.notification_service import NotificationService
from app.utils.response_handler import success_response, error_response

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("")
async def get_my_notifications(
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieves all notifications for the authenticated user, sorted newest first.
    """
    try:
        notifications = await NotificationService.get_user_notifications(db, current_user["id"])
        return success_response(
            data=notifications,
            message="User notifications retrieved successfully."
        )
    except Exception as e:
        return error_response(message="Failed to fetch notifications.", errors=str(e))

@router.patch("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Marks a user's notification as read.
    """
    try:
        success = await NotificationService.mark_as_read(db, notification_id, current_user["id"])
        if success:
            return success_response(
                message="Notification marked as read."
            )
        return error_response(
            message="Notification not found or access denied.",
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return error_response(message="Failed to update notification.", errors=str(e))
