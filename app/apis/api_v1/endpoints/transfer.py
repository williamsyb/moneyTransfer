from fastapi import APIRouter, HTTPException, status, Depends
from schemas.transfer import UserTransfer, TransferRecord
from sqlalchemy.orm import Session
from auth.auth import get_current_active_user
from db.crud import create_transfer_record
from db.database import get_db

router = APIRouter()


@router.post('/createTransfer', response_model=TransferRecord)
async def create_transfer(target_user: UserTransfer, amount: float,
                          db: Session = Depends(get_db),
                          current_user: UserTransfer = Depends(get_current_active_user)):
    flag, transfer_record_or_msg = await create_transfer_record(current_user.id, target_user.id, amount, db)
    if not flag:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=transfer_record_or_msg,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return transfer_record_or_msg
