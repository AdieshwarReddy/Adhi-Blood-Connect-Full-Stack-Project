from fastapi import APIRouter, Depends, status, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db
from app.core.logger import logger
from app.schemas.auth_schema import UserSignup, UserLogin, GoogleLoginRequest
from app.services.auth_service import AuthService
from app.utils.response_handler import success_response, error_response
from app.middleware.rate_limit import rate_limiter

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", dependencies=[Depends(rate_limiter)])
async def signup(signup_data: UserSignup, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Registers a new user (donor, patient, hospital, admin) in the system.
    """
    try:
        user_profile = await AuthService.register_user(db, signup_data)
        
        # To make it extra frontend-friendly, auto-generate login tokens immediately
        from app.core.security import create_access_token, create_refresh_token
        user_id = user_profile["id"]
        access_token = create_access_token(subject=user_id)
        refresh_token = create_refresh_token(subject=user_id)
        
        data = {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user": user_profile
        }
        
        return success_response(
            data=data,
            message="User successfully registered.",
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        from fastapi import HTTPException
        if isinstance(e, HTTPException):
            return error_response(message=e.detail, status_code=e.status_code)
        logger.exception("Unexpected exception occurred during registration.")
        return error_response(message=f"An error occurred during account creation: {str(e)}", status_code=500)


@router.post("/login", dependencies=[Depends(rate_limiter)])
async def login(login_data: UserLogin, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Authenticates a user and returns JWT credentials and profile details.
    """
    try:
        auth_data = await AuthService.authenticate_user(db, login_data)
        return success_response(
            data=auth_data,
            message="User successfully authenticated."
        )
    except Exception as e:
        from fastapi import HTTPException
        if isinstance(e, HTTPException):
            return error_response(message=e.detail, status_code=e.status_code)
        logger.exception("Unexpected exception occurred during login.")
        return error_response(message="Authentication failed.", status_code=500)

@router.post("/refresh")
async def refresh(refresh_data: dict, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Refreshes an expired JWT access token using a valid refresh token.
    Expects body format: {"refreshToken": "..."}
    """
    token_str = refresh_data.get("refreshToken")
    if not token_str:
        return error_response(message="Refresh token is missing from payload.", status_code=status.HTTP_400_BAD_REQUEST)
        
    try:
        refreshed_data = await AuthService.refresh_tokens(db, token_str)
        return success_response(
            data=refreshed_data,
            message="Token successfully refreshed."
        )
    except Exception as e:
        from fastapi import HTTPException
        if isinstance(e, HTTPException):
            return error_response(message=e.detail, status_code=e.status_code)
        return error_response(message="Refresh failed.", status_code=401)

@router.post("/google", dependencies=[Depends(rate_limiter)])
async def google_login(payload: GoogleLoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Authenticates or registers a user via Google OAuth2.
    """
    try:
        auth_data = await AuthService.oauth_google_login(db, payload.token)
        return success_response(
            data=auth_data,
            message="OAuth authentication successful."
        )
    except Exception as e:
        logger.exception("Google login failed")
        return error_response(message=f"Google authentication failed: {str(e)}", status_code=400)

