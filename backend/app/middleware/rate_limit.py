import time
from typing import Dict, Tuple, Optional
from fastapi import Request, HTTPException, status
from app.core.config import settings
from app.core.logger import logger

# In-memory store for rate limiting if Redis is not configured
# Maps IP/Client_Key -> (list of timestamps)
_in_memory_limits: Dict[str, list] = {}

async def is_rate_limited(request: Request, limit: int = 100, window_seconds: int = 60) -> bool:
    """
    Evaluates if a request is rate-limited based on IP address.
    Supports in-memory or Redis backends dynamically.
    """
    client_ip = request.client.host if request.client else "unknown"
    path = request.url.path
    key = f"rate_limit:{client_ip}:{path}"

    # If Redis is configured and available
    if settings.REDIS_URL:
        try:
            import redis.asyncio as aioredis
            # Lazy initialize Redis client
            r = aioredis.from_url(settings.REDIS_URL)
            current_time = time.time()
            # Clean old records
            async with r.pipeline(transaction=True) as pipe:
                pipe.zremrangebyscore(key, 0, current_time - window_seconds)
                pipe.zcard(key)
                pipe.zadd(key, {str(current_time): current_time})
                pipe.expire(key, window_seconds)
                _, request_count, _, _ = await pipe.execute()
                
            if request_count > limit:
                return True
            return False
        except Exception as e:
            logger.warning(f"Fallback to in-memory rate limiting: Redis connection failed: {str(e)}")

    # In-memory fallback
    now = time.time()
    cutoff = now - window_seconds
    
    if key not in _in_memory_limits:
        _in_memory_limits[key] = []
        
    # Filter timestamps to keep only recent ones
    _in_memory_limits[key] = [t for t in _in_memory_limits[key] if t > cutoff]
    
    if len(_in_memory_limits[key]) >= limit:
        return True
        
    _in_memory_limits[key].append(now)
    return False

async def rate_limiter(request: Request):
    """
    FastAPI dependency wrapper for applying rate limits.
    """
    if await is_rate_limited(request, limit=60, window_seconds=60):
        logger.warning(f"Rate limit exceeded for IP: '{request.client.host if request.client else 'unknown'}' on endpoint '{request.url.path}'")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later."
        )
