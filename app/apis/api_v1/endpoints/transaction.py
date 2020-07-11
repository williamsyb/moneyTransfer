from fastapi import APIRouter, HTTPException, status, Depends
from schemas.transaction import UserTransfer, TransferRecord, HistoryTransaction
from sqlalchemy.orm import Session
from auth.auth import get_current_active_user
from db.crud import create_transfer_record, get_transaction_records
from db.database import get_db

router = APIRouter()


@router.post('/createTransfer', response_model=TransferRecord, tags=['Transaction'])
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


@router.get('/historyTransaction', response_model=HistoryTransaction, tags=['Transaction'])
async def get_transaction(db: Session = Depends(get_db),
                          current_user: UserTransfer = Depends(get_current_active_user)):
    flag, transactions_or_msg = await get_transaction_records(current_user.id, db)
    if not flag:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=transactions_or_msg,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return transactions_or_msg
