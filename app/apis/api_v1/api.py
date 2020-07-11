from fastapi import APIRouter
from apis.api_v1.endpoints import auth
from apis.api_v1.endpoints import transaction
from apis.api_v1.endpoints import balance
api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(transaction.router)
api_router.include_router(balance.router)

