from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from schemas.balance import BalanceReport, UserBalance
from auth.auth import get_current_active_user
from db.crud import get_user_balance
from db.database import get_db

router = APIRouter()


@router.get("/balance", response_model=BalanceReport, tags=['Balance'])
async def get_balance(db: Session = Depends(get_db),
                      current_user: UserBalance = Depends(get_current_active_user)):
    flag, balance_or_msg = await get_user_balance(current_user.id, db)
    if not flag:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=balance_or_msg,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return balance_or_msg
