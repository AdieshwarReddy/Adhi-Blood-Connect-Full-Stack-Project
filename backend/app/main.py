from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import db_manager, get_db
from app.core.logger import logger
from app.middleware.logging_middleware import LoggingMiddleware
from app.utils.response_handler import success_response, error_response
from app.utils.helpers import clean_db_doc, clean_db_docs
# Import all controllers from v1
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.emergency import router as emergency_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.chatbot import router as chatbot_router
from app.api.v1.websocket_routes import router as ws_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for external connections like MongoDB.
    """
    logger.info("Starting up FastAPI application...")
    try:
        await db_manager.connect_to_database()
    except Exception as e:
        logger.critical(f"Database connection failed at startup: {str(e)}")
    
    yield
    
    logger.info("Shutting down FastAPI application...")
    await db_manager.close_database_connection()

app = FastAPI(
    title="Adhi Blood Connect API",
    description="Production-grade, fully async backend for AI-powered blood donation matching platform.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. Register Logging Middleware
app.add_middleware(LoggingMiddleware)

# 2. Register CORS Middleware
# Restricts access based on configurable environment settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Health Check System GET /health
@app.get("/health", tags=["System Health"])
async def health_check():
    """
    Evaluates API running status, active MongoDB ping, WebSocket counts, and AI services.
    """
    status_data = {
        "api": "healthy",
        "mongodb": "disconnected",
        "websocket": "inactive",
        "ai_service": "not_configured"
    }
    
    # Check MongoDB
    if db_manager.client:
        try:
            await db_manager.client.admin.command('ping')
            status_data["mongodb"] = "connected"
        except Exception:
            pass
            
    # Check WebSocket channels count
    from app.websocket.connection_manager import manager
    channel_count = len(manager.active_connections)
    status_data["websocket"] = f"active ({channel_count} client channels)"
    
    # Check AI Keys
    if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
        status_data["ai_service"] = "configured (Gemini prioritised)"
    elif settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
        status_data["ai_service"] = "configured (OpenAI fallback)"
        
    return success_response(
        data=status_data,
        message="System status evaluated successfully."
    )

# 4. Include clean modular API v1 routers
# Supports standard route prefixes /api/v1/
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(emergency_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(chatbot_router, prefix="/api/v1")
app.include_router(ws_router, prefix="/api/v1")

# Also mount under /api prefix for out-of-the-box frontend compatibility
# The React client uses relative calls (e.g. baseURL: "/api")
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(emergency_router, prefix="/api")
app.include_router(notifications_router, prefix="/api")
app.include_router(chatbot_router, prefix="/api")
app.include_router(ws_router, prefix="/api")

# 5. Direct Frontend Integration Aliases
# Bridges gap between React services and Clean Architecture endpoints without touching React code.
@app.post("/api/chat", tags=["Frontend Integration Fallbacks"])
async def react_chat_compatibility(payload: dict, db=Depends(get_db)):
    """
    Fallback alias mapping POST /api/chat -> POST /api/v1/chatbot
    """
    message = payload.get("message", "")
    from app.services.chatbot_service import ChatbotService
    reply_data = await ChatbotService.ask_chatbot(db, message, "anonymous")
    return success_response(data=reply_data)

@app.get("/api/requests", tags=["Frontend Integration Fallbacks"])
async def react_requests_list_compatibility(db=Depends(get_db)):
    """
    Fallback alias mapping GET /api/requests -> GET /api/v1/emergency/active
    """
    cursor = db["emergency_requests"].find({"status": "active"}).sort("created_at", -1)
    raw_requests = await cursor.to_list(length=100)
    return success_response(data=clean_db_docs(raw_requests))

@app.post("/api/requests", tags=["Frontend Integration Fallbacks"])
async def react_requests_create_compatibility(payload: dict, db=Depends(get_db)):
    """
    Fallback alias mapping POST /api/requests -> POST /api/v1/emergency/create
    """
    # Map React's payload fields to our standard schema formats
    from app.schemas.emergency_schema import EmergencyCreate
    from app.services.donor_matching_service import DonorMatchingService
    from app.services.notification_service import NotificationService
    
    # Safe parse with fallbacks
    patient_name = payload.get("patientName", payload.get("patient_name", "Anonymous Patient"))
    blood_group = payload.get("bloodGroup", payload.get("blood_group", "O+"))
    units_needed = int(payload.get("unitsNeeded", payload.get("units_needed", 1)))
    urgency_level = payload.get("urgency", payload.get("urgency_level", "medium")).lower()
    if urgency_level not in ["low", "medium", "high", "critical"]:
        urgency_level = "medium"
        
    hospital_name = payload.get("hospitalName", payload.get("hospital_name", "Local Hospital"))
    hospital_contact = payload.get("contact", payload.get("hospital_contact", "+919876543210"))
    
    # Extract coordinates, fallback to default Bangalore location if missing
    coords = payload.get("coordinates", [77.5946, 12.9716])
    
    from datetime import datetime, timezone
    request_doc = {
        "patient_name": patient_name,
        "blood_group": blood_group,
        "units_needed": units_needed,
        "urgency_level": urgency_level,
        "hospital_name": hospital_name,
        "hospital_contact": hospital_contact,
        "location": {
            "type": "Point",
            "coordinates": coords
        },
        "status": "active",
        "created_by": "anonymous_patient",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    result = await db["emergency_requests"].insert_one(request_doc)
    request_doc["_id"] = result.inserted_id
    cleaned_request = clean_db_doc(request_doc)
    
    # Fetch ranked compatible donors
    matched_donors = await DonorMatchingService.match_donors_for_request(


        db=db,
        patient_blood_group=blood_group,
        coordinates=coords,
        urgency_level=urgency_level
    )
    
    # Dispatch notifications
    await NotificationService.broadcast_emergency(
        db=db,
        active_request=cleaned_request,
        matched_donors=matched_donors
    )
    
    return success_response(
        data={
            "request": cleaned_request,
            "matched_donors": matched_donors
        },
        message="Emergency request created and broadcasts sent."
    )

