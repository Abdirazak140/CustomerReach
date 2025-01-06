from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException
import jwt

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = request.headers.get("token", None)
 
        if token is None:
            raise HTTPException(402, detail="Token not found.")
        
        try:
            payload = jwt.decode(token, "secret", algorithms="HS256")
            request.state.user = payload
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token.")
        
        response = await call_next(request)
        
        return response