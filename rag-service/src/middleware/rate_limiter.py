from typing import Dict, Any
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp
import time
import asyncio
from ..utils.api_errors import TooManyRequestsException
from ..config.settings import settings

# Assuming a simple in-memory store for rate limiting for now, mimicking Neon
# In a real application, this would be a distributed store like Redis or a database.
_rate_limit_store: Dict[str, Dict[str, Any]] = {} # {session_id: {"count": int, "first_request_time": float}}

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/chat" and request.method == "POST":
            # Extract session_id from the request body
            # This requires reading the request body, which can only be done once.
            # So, we read it, store it, and replace it for the next middleware/route.
            try:
                body = await request.json()
                session_id = body.get("session_id")
                # Re-set the request body so it can be read again by the endpoint
                request._body = asyncio.to_thread(lambda: body)
                request.scope["_body"] = body
            except Exception:
                session_id = None # If body is not JSON or session_id is missing

            if not session_id:
                # If no session_id, we cannot apply per-session rate limiting.
                # Allow the request to proceed, but it won't be rate-limited.
                # A more robust solution might apply a global rate limit or reject.
                print("Warning: No session_id found for rate limiting. Request not rate-limited.")
                return await call_next(request)

            current_time = time.time()
            session_data = _rate_limit_store.get(session_id, {"count": 0, "first_request_time": current_time})

            # Check if the time window has passed
            if current_time - session_data["first_request_time"] >= settings.RATE_LIMIT_TIME_WINDOW_SECONDS:
                # Reset count and time for a new window
                session_data["count"] = 1
                session_data["first_request_time"] = current_time
            else:
                session_data["count"] += 1

            _rate_limit_store[session_id] = session_data

            if session_data["count"] > settings.RATE_LIMIT_MAX_REQUESTS:
                print(f"Rate limit exceeded for session_id: {session_id}")
                raise TooManyRequestsException(
                    message=f"Rate limit exceeded. Max {settings.RATE_LIMIT_MAX_REQUESTS} requests per {settings.RATE_LIMIT_TIME_WINDOW_SECONDS} seconds.",
                    target="session_id"
                )

        return await call_next(request)
