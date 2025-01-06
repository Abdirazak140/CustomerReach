from fastapi import APIRouter, HTTPException, Header, Request
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(ROOT_DIR)

from common.rabbitmq import request_service_with_response

router = APIRouter(prefix="/api/user")

@router.get("/profile")
def profile(request: Request):
    return request.state.user