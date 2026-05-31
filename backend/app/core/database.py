from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, GEOSPHERE
from app.core.config import settings
from app.core.logger import logger

class DatabaseManager:
    """
    Singleton class managing the state of the Motor async database client and session connections.
    """
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db: AsyncIOMotorDatabase = None

    async def connect_to_database(self):
        """
        Establishes a connection to MongoDB and sets up database references.
        """
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL.split('@')[-1] if '@' in settings.MONGODB_URL else settings.MONGODB_URL}...")
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.db = self.client[settings.DATABASE_NAME]
            # Verify connection
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB.")
            
            # Create indexes asynchronously upon connect
            await self.create_indexes()
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise e

    async def close_database_connection(self):
        """
        Closes all active socket connections in the client.
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

    async def create_indexes(self):
        """
        Configures database indices, including compound filters and spatial coordinates.
        """
        logger.info("Initializing database indices...")
        try:
            # Users Collection Indexes
            users = self.db["users"]
            
            # Unique email constraint
            email_idx = await users.create_index([("email", ASCENDING)], unique=True)
            logger.info(f"Created index: {email_idx}")

            # General role search
            role_idx = await users.create_index([("role", ASCENDING)])
            logger.info(f"Created index: {role_idx}")

            # Blood availability filters
            bg_idx = await users.create_index([("blood_group", ASCENDING)])
            logger.info(f"Created index: {bg_idx}")

            # 2dsphere geospatial index for geo queries
            geo_idx = await users.create_index([("geo_location", GEOSPHERE)])
            logger.info(f"Created index: {geo_idx}")

            # Emergency Requests Indexes
            emergencies = self.db["emergency_requests"]
            status_idx = await emergencies.create_index([("status", ASCENDING)])
            logger.info(f"Created index: {status_idx}")
            
            # Geospatial searches for nearby requests
            req_geo_idx = await emergencies.create_index([("location", GEOSPHERE)])
            logger.info(f"Created index: {req_geo_idx}")

            logger.info("All collection indices successfully initialized.")
        except Exception as e:
            logger.error(f"Error establishing indices: {str(e)}")

# Global Singleton Manager
db_manager = DatabaseManager()

async def get_db() -> AsyncIOMotorDatabase:
    """
    Dependency helper that retrieves the database instance.
    """
    if db_manager.db is None:
        # Fallback if lifecycle hasn't fully started
        await db_manager.connect_to_database()
    return db_manager.db
