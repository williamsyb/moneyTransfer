from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from schemas.auth_user import Token, UserIn, UserOut
from config.config import config
from auth import authenticate_user, create_access_token
from db.database import get_db
from db.crud import create_user
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/register', response_model=UserOut)
async def register(*, user: UserIn, db: Session = Depends(get_db)):
    # username: str
    # password: str
    # email: EmailStr
    # full_name: str = None

    user_created = create_user(user, db)
    return user_created
