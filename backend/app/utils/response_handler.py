from typing import Any, Optional
from fastapi.responses import JSONResponse

def success_response(data: Any = None, message: str = "Request completed successfully", status_code: int = 200) -> JSONResponse:
    """
    Returns a unified success response dictionary for client consumption.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data if data is not None else {},
            "errors": None
        }
    )

def error_response(errors: Any = None, message: str = "An error occurred during request execution", status_code: int = 400) -> JSONResponse:
    """
    Returns a unified error response dictionary for client consumption.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": {},
            "errors": errors if errors is not None else message
        }
    )
