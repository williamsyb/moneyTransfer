from fastapi import APIRouter
from apis.api_v1.endpoints import auth
from apis.api_v1.endpoints import transfer
api_router = APIRouter()

api_router.include_router(auth.router, tags=['auth'])
api_router.include_router(transfer.router, tags=['transfer'])
