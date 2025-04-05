from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analysis
import uvicorn
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT_DIR)

from common.jwt_middleware import jwt_middleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply JWT middleware
app.middleware("http")(jwt_middleware)

app.include_router(analysis.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)