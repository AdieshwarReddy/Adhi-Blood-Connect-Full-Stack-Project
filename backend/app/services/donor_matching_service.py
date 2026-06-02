from datetime import datetime, timezone
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.services.geo_service import GeoService
from app.utils.blood_compatibility import is_compatible
from app.core.logger import logger

class DonorMatchingService:
    """
    Recommendation engine prioritizing and ranking compatible donors for active emergencies.
    """
    @staticmethod
    async def match_donors_for_request(
        db: AsyncIOMotorDatabase,
        patient_blood_group: str,
        coordinates: List[float], # [longitude, latitude] of the request
        urgency_level: str = "medium",
        max_radius_km: float = 15.0
    ) -> List[Dict[str, Any]]:
        """
        Retrieves compatible, active, and available donors, calculates their fit scores, and ranks them.
        """
        logger.info(f"Initiating Smart Donor Matching for blood group '{patient_blood_group}' at {coordinates} (Urgency: '{urgency_level}').")


        
        # Adjust search radius based on emergency urgency
        radius_multiplier = {
            "low": 1.0,
            "medium": 1.5,
            "high": 2.0,
            "critical": 3.0
        }
        
        adjusted_radius = max_radius_km * radius_multiplier.get(urgency_level.lower(), 1.5)
        logger.info(f"Adjusted search radius for matching: {adjusted_radius} km (Base: {max_radius_km} km).")

        # Fetch nearby eligible active donors
        nearby_donors = await GeoService.find_nearby_donors(
            db=db,
            longitude=coordinates[0],
            latitude=coordinates[1],
            radius_km=adjusted_radius,
            blood_group=patient_blood_group
        )
        
        ranked_donors = []
        now = datetime.now(timezone.utc)
        
        for donor in nearby_donors:
            donor_id = donor["id"]
            
            # Check 90-day donation cooldown
            last_donated_str = donor.get("last_donation_date")
            if last_donated_str:
                try:
                    last_donated = datetime.fromisoformat(last_donated_str)
                    # Force timezone if missing
                    if last_donated.tzinfo is None:
                        last_donated = last_donated.replace(tzinfo=timezone.utc)
                    days_since = (now - last_donated).days
                    if days_since < 90:
                        logger.debug(f"Donor '{donor_id}' skipped: donated {days_since} days ago (90-day cooldown enforced).")
                        continue
                except Exception as ex:
                    logger.warning(f"Error parsing last donation date for donor '{donor_id}': {str(ex)}")

            # 1. Base Compatibility Score (50 Points Max)
            # Exact matches score higher than compatible fallbacks
            donor_bg = donor.get("blood_group", "")
            if donor_bg == patient_blood_group:
                compatibility_score = 50.0
            elif is_compatible(donor_bg, patient_blood_group):
                compatibility_score = 35.0
            else:
                continue # Safety safeguard: completely skip incompatible types

            # 2. Distance Score (35 Points Max)
            # Deduces score as distance increases
            distance = donor.get("distance_km", 0.0)
            distance_score = max(0.0, 35.0 - (distance * 1.5))

            # 3. Reliability Score (15 Points Max)
            reliability = float(donor.get("reliability_score", 100.0))
            reliability_score_boost = (reliability / 100.0) * 15.0

            # 4. Final Aggregated Ranking Score (100 Points Max)
            matching_rank_score = round(compatibility_score + distance_score + reliability_score_boost, 2)
            
            ranked_donors.append({
                "donor_id": donor_id,
                "name": donor.get("name", "Anonymous"),
                "blood_group": donor_bg,
                "phone_number": donor.get("phone_number", ""),
                "availability": donor.get("availability", True),
                "distance_km": distance,
                "compatibility_score": compatibility_score * 2.0, # scale to 100 for display
                "reliability_score": int(reliability),
                "matching_rank_score": matching_rank_score
            })
            
        # Sort donors in descending order of matching_rank_score
        ranked_donors.sort(key=lambda d: d["matching_rank_score"], reverse=True)
        logger.info(f"Smart Matching finished. Successfully ranked {len(ranked_donors)} eligible donors.")
        return ranked_donors
