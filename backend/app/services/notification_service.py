from datetime import datetime, timezone
from bson import ObjectId
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.websocket.connection_manager import manager
from app.core.logger import logger
from app.utils.helpers import clean_db_doc, clean_db_docs

class NotificationService:
    """
    Service responsible for storing and broadcasting alert messages to users.
    Integrates DB persistence with active WebSocket channels.
    """
    @staticmethod
    async def create_notification(
        db: AsyncIOMotorDatabase,
        user_id: str,
        title: str,
        message: str,
        notification_type: str = "emergency"
    ) -> dict:
        """
        Saves a notification to MongoDB and attempts real-time WebSocket delivery if the user is active.
        """
        notification_doc = {
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "is_read": False,
            "created_at": datetime.now(timezone.utc)
        }
        
        try:
            result = await db["notifications"].insert_one(notification_doc)
            notification_doc["_id"] = result.inserted_id
            logger.info(f"Notification cached for user '{user_id}' with ID '{result.inserted_id}'.")
            
            # Formulate payload for WebSocket delivery
            cleaned_payload = clean_db_doc(notification_doc)
            
            # Attempt to push to active socket
            delivered_live = await manager.send_personal_message(cleaned_payload, user_id)
            if delivered_live:
                logger.info(f"Notification delivered instantly via active WebSocket channel to user '{user_id}'.")
            else:
                logger.debug(f"User '{user_id}' is offline. Alert saved to database.")
                
            return cleaned_payload
        except Exception as e:
            logger.error(f"Error handling notification creation: {str(e)}")
            raise e

    @staticmethod
    async def get_user_notifications(db: AsyncIOMotorDatabase, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves all notifications for a specific user, sorted newest first.
        """
        cursor = db["notifications"].find({"user_id": user_id}).sort("created_at", -1)
        raw_notifications = await cursor.to_list(length=100)
        return clean_db_docs(raw_notifications)

    @staticmethod
    async def mark_as_read(db: AsyncIOMotorDatabase, notification_id: str, user_id: str) -> bool:
        """
        Marks a specific notification as read after verification of ownership.
        """
        try:
            notification_obj_id = ObjectId(notification_id)
        except Exception:
            logger.warning(f"Invalid notification ObjectId: '{notification_id}'")
            return False
            
        result = await db["notifications"].update_one(
            {"_id": notification_obj_id, "user_id": user_id},
            {"$set": {"is_read": True}}
        )
        
        if result.modified_count > 0:
            logger.info(f"Notification '{notification_id}' marked as read by user '{user_id}'.")
            return True
        return False

    @staticmethod
    async def broadcast_emergency(db: AsyncIOMotorDatabase, active_request: dict, matched_donors: List[dict]):
        """
        Broadcasts emergency details to matched compatible donors.
        Creates persistent DB logs + triggers live socket notifications.
        """
        request_id = active_request.get("id")
        blood_group = active_request.get("blood_group")
        urgency = active_request.get("urgency_level").upper()
        hospital = active_request.get("hospital_name")
        units = active_request.get("units_needed")
        
        title = f"🔴 {urgency} Emergency Blood Request!"
        message = f"Hospital '{hospital}' urgently needs {units} units of '{blood_group}' blood. You are a compatible match!"
        
        logger.info(f"Broadcasting emergency request '{request_id}' to {len(matched_donors)} matched donors...")
        
        for donor in matched_donors:
            donor_id = donor.get("donor_id")
            if donor_id:
                try:
                    await NotificationService.create_notification(
                        db=db,
                        user_id=donor_id,
                        title=title,
                        message=message,
                        notification_type="emergency"
                    )
                except Exception as ex:
                    logger.error(f"Failed to create emergency broadcast for donor '{donor_id}': {str(ex)}")
