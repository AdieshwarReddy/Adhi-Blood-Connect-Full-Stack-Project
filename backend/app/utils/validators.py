import re
from typing import List

PHONE_REGEX = re.compile(r"^\+?[1-9]\d{1,14}$") # E.164 phone validation

def validate_phone(phone: str) -> bool:
    """
    Validates a phone number matches standard E.164 syntax.
    """
    if not phone:
        return False
    # Strip spaces and dashes
    cleaned = phone.replace(" ", "").replace("-", "")
    return bool(PHONE_REGEX.match(cleaned))

def validate_coordinates(coordinates: List[float]) -> bool:
    """
    Verifies geographic coordinates are valid [-180 to 180] for longitude and [-90 to 90] for latitude.
    """
    if len(coordinates) != 2:
        return False
    longitude, latitude = coordinates[0], coordinates[1]
    return -180.0 <= longitude <= 180.0 and -90.0 <= latitude <= 90.0
