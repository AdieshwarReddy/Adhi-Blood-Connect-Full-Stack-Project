from fastapi import APIRouter, Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.schemas.chatbot_schema import ChatQuery
from app.services.chatbot_service import ChatbotService
from app.utils.response_handler import success_response, error_response
from app.core.security import decode_token
from app.middleware.rate_limit import rate_limiter

router = APIRouter(prefix="/chatbot", tags=["AI Chatbot"])

@router.post("", dependencies=[Depends(rate_limiter)])
async def ask_assistant(
    payload: ChatQuery,
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Submits a user query to the AI assistant. Tracks the user anonymously or via token if present.
    """
    # Try to extract user ID from Auth headers safely (chatbot is accessible publicly)
    user_id = "anonymous"
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload_data = decode_token(token)
            if payload_data and payload_data.get("type") == "access":
                user_id = payload_data.get("sub", "anonymous")
        except Exception:
            pass # ignore token issues for public chatbot access

    try:
        reply_data = await ChatbotService.ask_chatbot(
            db=db,
            message=payload.message,
            user_id=user_id
        )
        return success_response(
            data=reply_data,
            message="Response successfully generated."
        )
    except Exception as e:
        from app.core.logger import logger
        logger.exception("AI Chatbot routing exception occurred.")
        return error_response(message="Failed to generate AI response.", errors=str(e))
