from app.db import Base, engine
from app.routers.auth import router as auth_router
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import conf

CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]
app = FastAPI(title=conf.PROJECT_NAME, version="1.0.0")

# / api
api_router = APIRouter()

# authentication route /auth
api_router.include_router(auth_router, prefix="/auth")

app.include_router(api_router, prefix="/api")

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(engine)
