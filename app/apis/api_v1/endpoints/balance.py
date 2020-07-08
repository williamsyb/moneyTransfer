from fastapi import APIRouter
from fastapi import Depends
from app.db.database import get_db
from app.db import crud
from sqlalchemy.orm import Session
from typing import List
router = APIRouter()


@router.post("/balance/{user}/{year}/{month}", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


