from fastapi import APIRouter
from apis.api_v1.endpoints import auth

api_router = APIRouter()

api_router.include_router(auth.router, tags=['auth'])
