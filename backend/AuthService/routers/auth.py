from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/app/users")

@router.get("/")
def test():
    return "Test"