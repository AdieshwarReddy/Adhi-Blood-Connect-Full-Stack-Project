import math
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.utils.blood_compatibility import get_compatible_donors
from app.utils.helpers import clean_db_docs

class GeoService:
    """
    Service for executing geographical query operations, geospatial filtering, and distance computations.
    """
    @staticmethod
    def haversine_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """
        Calculates the great-circle distance between two GPS coordinates in kilometers.
        """
        # Convert decimal degrees to radians
        rad_lon1, rad_lat1, rad_lon2, rad_lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        
        # Haversine formula
        dlon = rad_lon2 - rad_lon1
        dlat = rad_lat2 - rad_lat1
        
        a = math.sin(dlat / 2.0)**2 + math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(dlon / 2.0)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth radius in kilometers
        km = 6371.0 * c
        return round(km, 2)

    @staticmethod
    async def find_nearby_donors(
        db: AsyncIOMotorDatabase,
        longitude: float,
        latitude: float,
        radius_km: float = 10.0,
        blood_group: str = None,
        exclude_user_id: str = None
    ) -> List[Dict[str, Any]]:
        """
        Searches MongoDB for nearby active donors within a radius.
        Uses 2dsphere indexes via $near to perform geospatial sorting.
        """
        # Convert radius to radians (Earth radius is ~6371 km)
        max_distance_meters = radius_km * 1000.0


        
        # Base query for compatible/active donors
        query: Dict[str, Any] = {
            "role": "donor",
            "availability": True
        }
        
        # Exclude self if requested
        if exclude_user_id:
            from bson import ObjectId
            try:
                query["_id"] = {"$ne": ObjectId(exclude_user_id)}
            except Exception:
                pass

        # Apply blood group constraints (only matching compatible blood groups if supplied)
        if blood_group:
            compatible_groups = get_compatible_donors(blood_group)
            query["blood_group"] = {"$in": compatible_groups}
            
        # Geospatial near sphere constraint
        query["geo_location"] = {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": max_distance_meters
            }
        }
        
        cursor = db["users"].find(query)
        # Limit to top 50 nearby donors for scale/performance
        raw_donors = await cursor.to_list(length=50)
        
        donors_list = []
        for donor in raw_donors:
            donor_coords = donor.get("geo_location", {}).get("coordinates", [])
            distance = 0.0
            if len(donor_coords) == 2:
                distance = GeoService.haversine_distance(
                    longitude, latitude,
                    donor_coords[0], donor_coords[1]
                )
            
            # Map donor structure
            from app.utils.helpers import clean_db_doc
            cleaned = clean_db_doc(donor)
            cleaned["distance_km"] = distance
            donors_list.append(cleaned)
            
        # Sort results by distance secondary check
        donors_list.sort(key=lambda d: d["distance_km"])
        return donors_list
