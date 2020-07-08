from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from schemas.auth_user import Token, UserIn, UserOut
from config.config import config
from auth import authenticate_user, create_access_token
from db.database import get_db
from db.crud import create_user
from sqlalchemy.orm import Session

route = APIRouter()


@route.post('/createTransfer')
def create_transfer(start_user, end_user, db: Session = Depends(get_db)):
    pass
