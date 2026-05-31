from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user, RoleChecker
from app.schemas.user_schema import UserUpdate
from app.services.geo_service import GeoService
from app.utils.response_handler import success_response, error_response
from app.utils.helpers import clean_db_doc

router = APIRouter(prefix="/donors", tags=["Donors & Users"])

@router.get("")
async def search_donors(
    lat: float = Query(..., description="Latitude coordinate"),
    lon: float = Query(..., description="Longitude coordinate"),
    radius: float = Query(10.0, description="Search radius in kilometers"),
    blood_group: Optional[str] = Query(None, description="Patient blood group compatibility constraint"),
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Search and find compatible, available donors sorted by distance.
    """
    try:
        donors = await GeoService.find_nearby_donors(
            db=db,
            longitude=lon,
            latitude=lat,
            radius_km=radius,
            blood_group=blood_group,
            exclude_user_id=current_user["id"]
        )
        return success_response(
            data=donors,
            message=f"Found {len(donors)} available donors in search radius."
        )
    except Exception as e:
        return error_response(message="Failed to execute donor search.", errors=str(e))

@router.get("/me")
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    Retrieves the authenticated user's profile card.
    """
    return success_response(
        data=current_user,
        message="Profile retrieved successfully."
    )

@router.patch("/me")
async def update_my_profile(
    profile_data: dict, # support direct flexible bodies (like {"available": true} or {"availability": true})
    db: AsyncIOMotorDatabase = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Updates profile variables like geographical location coordinates or donation availability.
    """
    user_id = current_user["id"]
    from bson import ObjectId
    
    # Standardize field mapping for flexible keys
    updates = {}
    
    # Availability can be sent as available or availability
    if "available" in profile_data:
        updates["availability"] = bool(profile_data["available"])
    if "availability" in profile_data:
        updates["availability"] = bool(profile_data["availability"])
        
    if "name" in profile_data:
        updates["name"] = str(profile_data["name"])
    if "blood_group" in profile_data:
        updates["blood_group"] = str(profile_data["blood_group"])
    if "city" in profile_data:
        updates["city"] = str(profile_data["city"])
    if "phone_number" in profile_data:
        updates["phone_number"] = str(profile_data["phone_number"])
        
    if "coordinates" in profile_data:
        coords = profile_data["coordinates"]
        if isinstance(coords, list) and len(coords) == 2:
            updates["geo_location"] = {
                "type": "Point",
                "coordinates": [float(coords[0]), float(coords[1])]
            }

    if not updates:
        return error_response(message="No valid update fields detected in request.", status_code=400)
        
    from datetime import datetime, timezone
    updates["updated_at"] = datetime.now(timezone.utc)
    
    try:
        await db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updates}
        )
        
        # Fetch fresh updated profile
        updated_doc = await db["users"].find_one({"_id": ObjectId(user_id)})
        return success_response(
            data=clean_db_doc(updated_doc),
            message="User profile updated successfully."
        )
    except Exception as e:
        return error_response(message="Error executing profile updates.", errors=str(e))
