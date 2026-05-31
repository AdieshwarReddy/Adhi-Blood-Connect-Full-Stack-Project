from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.logger import logger
from app.schemas.auth_schema import UserSignup, UserLogin
from app.utils.helpers import clean_db_doc

class AuthService:
    """
    Service encapsulating user registration, session authentication, and token cycles.
    """
    @staticmethod
    async def register_user(db: AsyncIOMotorDatabase, signup_data: UserSignup) -> dict:
        """
        Creates a new user record in MongoDB. Performs security hashes and index checks.
        """
        email = signup_data.email.lower().strip()
        
        # Check if user already exists
        existing_user = await db["users"].find_one({"email": email})
        if existing_user:
            logger.warning(f"Registration failed: User with email '{email}' already exists.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address is already registered."
            )
            
        hashed_pwd = hash_password(signup_data.password)
        
        # Structure MongoDB GeoJSON Point format
        user_doc = {
            "name": signup_data.name.strip(),
            "email": email,
            "hashed_password": hashed_pwd,
            "blood_group": signup_data.blood_group,
            "role": signup_data.role,
            "city": signup_data.city.strip(),
            "phone_number": signup_data.phone_number.strip(),
            "geo_location": {
                "type": "Point",
                "coordinates": signup_data.coordinates # [longitude, latitude]
            },
            "availability": signup_data.availability,
            "last_donation_date": None,
            "reliability_score": 100,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        try:
            result = await db["users"].insert_one(user_doc)
            user_doc["_id"] = result.inserted_id
            logger.info(f"User successfully registered: '{email}' with ID '{result.inserted_id}'.")
            return clean_db_doc(user_doc)
        except Exception as e:
            logger.error(f"MongoDB write failed during registration: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user profile in database."
            )

    @staticmethod
    async def authenticate_user(db: AsyncIOMotorDatabase, login_data: UserLogin) -> dict:
        """
        Validates credentials and constructs access and refresh token pairs.
        """
        email = login_data.email.lower().strip()
        user_doc = await db["users"].find_one({"email": email})
        
        if not user_doc or not verify_password(login_data.password, user_doc.get("hashed_password", "")):
            logger.warning(f"Authentication failed for user '{email}'. Invalid credentials.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password."
            )
            
        user_id = str(user_doc["_id"])
        
        # Build token payloads
        access_token = create_access_token(subject=user_id)
        refresh_token = create_refresh_token(subject=user_id)
        
        logger.info(f"User '{email}' successfully authenticated.")
        
        return {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user": clean_db_doc(user_doc)
        }

    @staticmethod
    async def refresh_tokens(db: AsyncIOMotorDatabase, refresh_token: str) -> dict:
        """
        Decodes a refresh token and generates a fresh pair of tokens.
        """
        try:
            payload = decode_token(refresh_token)
            user_id = payload.get("sub")
            token_type = payload.get("type")
            
            if not user_id or token_type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh credentials"
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token refresh failed or token expired."
            )
            
        user_doc = await db["users"].find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User associated with token does not exist."
            )
            
        access_token = create_access_token(subject=user_id)
        new_refresh_token = create_refresh_token(subject=user_id)
        
        return {
            "accessToken": access_token,
            "refreshToken": new_refresh_token,
            "user": clean_db_doc(user_doc)
        }

    @staticmethod
    async def oauth_google_login(db: AsyncIOMotorDatabase, google_token: str, role: str = "donor") -> dict:
        """
        OAuth template validating external Google credentials, creating a profile if needed.
        """
        logger.info(f"OAuth login requested using token signature '{google_token[:15]}...' for role '{role}'.")
        
        # In production, call verify_oauth2_token(google_token, requests.Request(), CLIENT_ID)
        # We simulate a valid Google profile callback:
        email = f"google.{google_token[:8].lower()}@gmail.com"
        name = "Google User"
        
        user_doc = await db["users"].find_one({"email": email})
        
        if not user_doc:
            # First time logging in, register profile
            user_doc = {
                "name": name,
                "email": email,
                "hashed_password": hash_password(ObjectId().__str__()), # Secure generated hash
                "blood_group": "O+",
                "role": role,
                "city": "Bangalore",
                "phone_number": "+919876543210",
                "geo_location": {
                    "type": "Point",
                    "coordinates": [77.5946, 12.9716] # default Bangalore coordinates
                },
                "availability": True,
                "last_donation_date": None,
                "reliability_score": 100,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
            result = await db["users"].insert_one(user_doc)
            user_doc["_id"] = result.inserted_id
            logger.info(f"Created new user via Google Sign-In: '{email}' with ID '{result.inserted_id}'.")
            
        user_id = str(user_doc["_id"])
        access_token = create_access_token(subject=user_id)
        refresh_token = create_refresh_token(subject=user_id)
        
        return {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user": clean_db_doc(user_doc)
        }
