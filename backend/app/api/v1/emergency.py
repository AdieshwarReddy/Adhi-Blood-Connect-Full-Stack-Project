from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
from fastapi import APIRouter, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user, RoleChecker
from app.schemas.emergency_schema import EmergencyCreate, EmergencyUpdate
from app.services.donor_matching_service import DonorMatchingService
from app.services.notification_service import NotificationService
from app.utils.response_handler import success_response, error_response
from app.utils.helpers import clean_db_doc, clean_db_docs
from app.core.logger import logger

router = APIRouter(prefix="/emergency", tags=["Emergency Requests"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_emergency_request(
    payload: EmergencyCreate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Creates an emergency request. Computes matched compatible donors, saves records in DB,
    and triggers instant real-time pushes/sms alerts.
    """
    logger.info(f"User '{current_user['email']}' is creating an emergency blood request.")
    
    # Structure MongoDB GeoJSON Point format
    request_doc = {
        "patient_name": payload.patient_name.strip(),
        "blood_group": payload.blood_group,
        "units_needed": payload.units_needed,
        "urgency_level": payload.urgency_level,
        "hospital_name": payload.hospital_name.strip(),
        "hospital_contact": payload.hospital_contact.strip(),
        "location": {
            "type": "Point",
            "coordinates": payload.coordinates # [longitude, latitude]
        },
        "status": "active", # defaults to active
        "created_by": current_user["id"],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }

    try:
        result = await db["emergency_requests"].insert_one(request_doc)
        request_doc["_id"] = result.inserted_id
        cleaned_request = clean_db_doc(request_doc)
        logger.info(f"Emergency request registered in MongoDB. ID: '{result.inserted_id}'")

        # Run Smart Matching Engine asynchronously to get ranked compatible donors
        matched_donors = await DonorMatchingService.match_donors_for_request(
            db=db,
            patient_blood_group=payload.blood_group,
            coordinates=payload.coordinates,
            urgency_level=payload.urgency_level
        )

        # Dispatch background notifications & SMS notifications
        from fastapi import BackgroundTasks
        background_tasks = BackgroundTasks()
        
        # Enforce broadcast asynchronously to avoid blocking the API response
        await NotificationService.broadcast_emergency(
            db=db,
            active_request=cleaned_request,
            matched_donors=matched_donors
        )

        data = {
            "request": cleaned_request,
            "matched_donors": matched_donors
        }
        
        return success_response(
            data=data,
            message="Emergency request created. Matching alerts successfully dispatched.",
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        logger.exception("Error processing emergency request creation.")
        return error_response(message="An error occurred while launching request.", errors=str(e))

@router.get("/active")
async def get_active_requests(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Retrieves all open active emergency requests in the system.
    """
    try:
        cursor = db["emergency_requests"].find({"status": "active"}).sort("created_at", -1)
        raw_requests = await cursor.to_list(length=100)
        return success_response(
            data=clean_db_docs(raw_requests),
            message="Active emergency requests retrieved."
        )
    except Exception as e:
        return error_response(message="Failed to fetch active requests.", errors=str(e))

@router.get("/nearby")
async def get_nearby_requests(
    lat: float = Query(..., description="Target Latitude"),
    lon: float = Query(..., description="Target Longitude"),
    radius: float = Query(15.0, description="Radius limit in km"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Search and find active emergency requests near specific location coordinates.
    """
    max_distance_meters = radius * 1000.0
    query = {
        "status": "active",
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "$maxDistance": max_distance_meters
            }
        }
    }
    
    try:
        cursor = db["emergency_requests"].find(query)
        raw_requests = await cursor.to_list(length=50)
        return success_response(
            data=clean_db_docs(raw_requests),
            message=f"Found {len(raw_requests)} active requests in search radius."
        )
    except Exception as e:
        return error_response(message="Failed to retrieve nearby requests.", errors=str(e))

@router.put("/{request_id}")
async def update_emergency_request(
    request_id: str,
    payload: EmergencyUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Modifies fields or changes status (fulfilled/cancelled) of an active emergency request.
    Verifies that the request belongs to the authenticated user.
    """
    try:
        req_obj_id = ObjectId(request_id)
    except Exception:
        return error_response(message="Invalid Request ID format.", status_code=400)
        
    existing_req = await db["emergency_requests"].find_one({"_id": req_obj_id})
    if not existing_req:
        return error_response(message="Emergency request not found.", status_code=404)
        
    # Security: Verify ownership or admin privileges
    if existing_req.get("created_by") != current_user["id"] and current_user.get("role") != "admin":
        return error_response(message="Access denied. You do not have permission to edit this request.", status_code=403)

    updates = {}
    profile_data = payload.dict(exclude_unset=True)
    
    for key, val in profile_data.items():
        if key == "coordinates" and isinstance(val, list) and len(val) == 2:
            updates["location"] = {
                "type": "Point",
                "coordinates": [float(val[0]), float(val[1])]
            }
        elif key != "coordinates":
            updates[key] = val
            
    updates["updated_at"] = datetime.now(timezone.utc)
    
    try:
        await db["emergency_requests"].update_one(
            {"_id": req_obj_id},
            {"$set": updates}
        )
        updated_doc = await db["emergency_requests"].find_one({"_id": req_obj_id})
        return success_response(
            data=clean_db_doc(updated_doc),
            message="Emergency request details successfully updated."
        )
    except Exception as e:
        return error_response(message="Error executing updates.", errors=str(e))

@router.delete("/{request_id}")
async def delete_emergency_request(
    request_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Deletes an emergency request completely from the database.
    """
    try:
        req_obj_id = ObjectId(request_id)
    except Exception:
        return error_response(message="Invalid Request ID format.", status_code=400)
        
    existing_req = await db["emergency_requests"].find_one({"_id": req_obj_id})
    if not existing_req:
        return error_response(message="Emergency request not found.", status_code=404)
        
    # Security: Verify ownership or admin privileges
    if existing_req.get("created_by") != current_user["id"] and current_user.get("role") != "admin":
        return error_response(message="Access denied.", status_code=403)
        
    try:
        await db["emergency_requests"].delete_one({"_id": req_obj_id})
        logger.info(f"Emergency request '{request_id}' deleted successfully.")
        return success_response(
            message="Emergency request deleted successfully."
        )
    except Exception as e:
        return error_response(message="Error deleting request.", errors=str(e))
