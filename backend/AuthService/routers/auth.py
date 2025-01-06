from fastapi import APIRouter, HTTPException
import jwt
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(ROOT_DIR)

from common.rabbitmq import on_response, publish_message, request_service_with_response

router = APIRouter(prefix="/api/user")

def generateJWT(payload):
    encoded = jwt.encode(payload, "secret", algorithm="HS256")
    return encoded

@router.post("/login")
def login(data: dict):
    response = None
    try:
        payload = {
            "request_type": "login",
            "email": data["email"],
            "password": data["password"],
        }
        
        response = request_service_with_response("user_data", payload)
        
        if response["status"] == "error":
            raise HTTPException(status_code=400, detail="Email or password is incorrect")
        
        token = generateJWT({"user_id": response["user_id"]})
        
    except Exception:
        raise HTTPException(status_code=400, detail=str(Exception))

    return token

@router.post("/signup")
def signup(data: dict):
    response = None
    try:
        payload = {
            "request_type": "registration",
            "email": data["email"],
            "password": data["password"],
            "location": data["location"]
        }
        
        response = request_service_with_response("user_data", payload)
        
        if response["status"] == "error":
            raise HTTPException(status_code=400, detail="Email already exists")
        
        token = generateJWT({"user_id": response["user_id"]})

        
    except Exception:
        raise HTTPException(status_code=400, detail=str(Exception))

    return token

