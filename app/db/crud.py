from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from functools import wraps
from db.models import User
from schemas.auth_user import UserIn
from fastapi.logger import logger
from auth import get_password_hash


def db_commit_decorator(func):
    @wraps(func)
    async def session_commit(*args, **kwargs):
        db: Session = kwargs.get('db')
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error('db operation error，here are details{}'.format(e))
            logger.warning('transaction rollbacks')
            db.rollback()
    return session_commit


@db_commit_decorator
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()


@db_commit_decorator
async def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


@db_commit_decorator
async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


@db_commit_decorator
async def create_user(user: UserIn, db: Session = Depends(get_db)):
    hashed_pw = get_password_hash(user.password)
    db_user = User(username=user.username, full_name=user.full_name,
                   email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
