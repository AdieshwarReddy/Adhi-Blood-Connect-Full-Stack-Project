import asyncio
from datetime import datetime, timezone

# Load application settings (includes .env)
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
DATABASE_NAME = settings.DATABASE_NAME
db = client[DATABASE_NAME]

# Sample donor documents
DONORS = [
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "hashed_password": "placeholder",  # you can replace with a real hash later
        "blood_group": "O+",
        "role": "donor",
        "city": "Bangalore",
        "phone_number": "1234567890",
        "geo_location": {"type": "Point", "coordinates": [77.5946, 12.9716]},
        "availability": True,
        "last_donation_date": None,
        "reliability_score": 100,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "hashed_password": "placeholder",
        "blood_group": "A-",
        "role": "donor",
        "city": "Mumbai",
        "phone_number": "9876543210",
        "geo_location": {"type": "Point", "coordinates": [72.8777, 19.0760]},
        "availability": True,
        "last_donation_date": None,
        "reliability_score": 100,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
]

async def seed():
    # Clear existing collections (optional)
    await db["donors"].delete_many({})
    await db["donors"].insert_many(DONORS)
    print("✅ Seeded donors collection with sample data.")
    # You can add more collections like 'blood_requests' similarly.

if __name__ == "__main__":
    asyncio.run(seed())
