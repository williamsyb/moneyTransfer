from fastapi import APIRouter, Depends
from schemas.auth_user import UserIn, UserOut
from db.database import get_db
from db.crud import create_user
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/register', response_model=UserOut, tags=['Auth'])
async def register(*, user: UserIn, db: Session = Depends(get_db)):
    print('-----------------------------------------------------------------')
    print(db)
    user_created = await create_user(user, db)
    return user_created
