from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import jwt

async def jwt_middleware(request: Request, call_next):
    # Skip auth for docs and openapi.json
    if request.url.path in ["/docs", "/openapi.json"]:
        return await call_next(request)
    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing Authorization header"}
        )

    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401, 
                detail="Invalid authentication scheme"
            )
            
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        request.state.user = payload
    except Exception as e:
        return JSONResponse(
            status_code=401,
            content={"detail": f"Invalid token: {str(e)}"}
        )

    return await call_next(request)