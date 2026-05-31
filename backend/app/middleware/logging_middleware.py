import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that records HTTP transactions, including response code, method, path, and duration.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        
        logger.info(f"Incoming Request: {method} {path} | Client IP: {client_ip}")
        
        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            
            logger.info(
                f"Outgoing Response: {method} {path} | "
                f"Status: {response.status_code} | "
                f"Time: {process_time:.2f}ms"
            )
            return response
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.exception(
                f"Unhandled Exception occurred: {method} {path} | "
                f"Time: {process_time:.2f}ms | Error: {str(e)}"
            )
            raise e
