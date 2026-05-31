from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.core.database import get_db
from app.core.security import decode_token
from app.core.logger import logger
from app.utils.helpers import clean_db_doc

security_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db = Depends(get_db)
) -> dict:
    """
    Decodes the Bearer token, validates it, and fetches the corresponding User doc from MongoDB.
    """
    token = credentials.credentials
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if not user_id or token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from db
    from bson import ObjectId
    try:
        user_obj_id = ObjectId(user_id)
    except Exception:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identification format",
        )
        
    user_doc = await db["users"].find_one({"_id": user_obj_id})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with this token no longer exists",
        )
        
    return clean_db_doc(user_doc)

class RoleChecker:
    """
    Dependency validator that verifies if the current user belongs to the allowed roles list.
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: dict = Depends(get_current_user)) -> dict:
        role = current_user.get("role")
        if role not in self.allowed_roles:
            logger.warning(f"Access Denied: User '{current_user.get('email')}' with role '{role}' tried to access restricted resource (Allowed: {self.allowed_roles}).")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(self.allowed_roles)}",
            )
        return current_user
