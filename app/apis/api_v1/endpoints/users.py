from fastapi import APIRouter, Depends
from auth.auth import get_current_active_user
from db.models import User
from db.database import get_db
from schemas.auth_user import AllUser
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/all_users', response_model=AllUser)
def get_all_user(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.is_supervisor and current_user.is_active:
        all_users = db.query(User).all()
        return all_users

