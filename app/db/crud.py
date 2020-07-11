from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db
from functools import wraps, reduce
from db.models import User, TransferAction
from schemas.auth_user import UserIn
from schemas.transaction import HistoryTransaction
from schemas.balance import BalanceReport
from fastapi.logger import logger
from auth import get_password_hash
from typing import Tuple, Union
from itertools import groupby
from operator import itemgetter
from datetime import timedelta


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
async def create_user(user: UserIn, db: Session = Depends(get_db)) -> User:
    hashed_pw = get_password_hash(user.password)
    db_user = User(username=user.username, full_name=user.full_name,
                   email=user.email, hashed_password=hashed_pw, is_supervisor=user.is_supervisor)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@db_commit_decorator
async def create_transfer_record(start_user_id: int, end_user_id: int, amount: float,
                                 db: Session = Depends(get_db)) -> Tuple[bool, Union[str, TransferAction]]:
    start_user = db.query(User).filter(User.id == start_user_id).one()
    end_user = db.query(User).filter(User.id == end_user_id).one()
    if start_user and end_user:
        if amount > start_user.wallet:
            return False, 'amount great than the wallet!'
        start_user.wallet -= amount
        end_user.wallet += amount
        record = TransferAction(asset_start_user=start_user.username, asset_start_user_id=start_user.id,
                                asset_end_user=end_user.username, asset_end_user_id=end_user.id, asset=amount
                                )

        db.add(record)
        db.commit()
        db.refresh(record)
        return True, record
    else:
        return False, 'user not found error'


async def get_transaction_records(user_id: int, db: Session) -> Tuple[bool, Union[str, HistoryTransaction]]:
    user_as_payer_records = db.query(TransferAction).filter(TransferAction.asset_start_user_id == user_id).all()
    user_as_payee_records = db.query(TransferAction).filter(TransferAction.asset_end_user_id == user_id).all()

    if not user_as_payer_records and not user_as_payee_records:
        return False, f'user_id:{user_id} not found'

    records = []
    if user_as_payer_records:
        records.extend(user_as_payer_records)
    if user_as_payee_records:
        records.extend(user_as_payee_records)

    records = [item.to_dict() for item in records]
    for record in records:
        record['date'] = (record['timestamp'] + timedelta(hours=8)).strftime('%Y%m%d')
    records.sort(key=itemgetter('date'))
    results = {}
    for date, items in groupby(records, key=itemgetter('date')):
        results[date] = list(items)
    return True, HistoryTransaction(**{'records': results})


async def get_user_balance(user_id: int, db: Session) -> Tuple[bool, Union[str, BalanceReport]]:
    user_as_payer_records = db.query(TransferAction).filter(TransferAction.asset_start_user_id == user_id).all()
    user_as_payee_records = db.query(TransferAction).filter(TransferAction.asset_end_user_id == user_id).all()

    if not user_as_payer_records and not user_as_payee_records:
        return False, f'user_id:{user_id} not found'

    records = []
    if user_as_payer_records:
        records.extend(user_as_payer_records)
    if user_as_payee_records:
        records.extend(user_as_payee_records)

    records = [item.to_dict() for item in records]
    for record in records:
        record['month'] = (record['timestamp'] + timedelta(hours=8)).strftime('%Y%m')
    records.sort(key=itemgetter('month'))
    results = {}
    for date, items in groupby(records, key=itemgetter('month')):
        # results[date] = list(items)
        month_data = list(items)
        as_payer = [item for item in month_data if item['asset_start_user_id'] == user_id]
        as_payee = [item for item in month_data if item['asset_end_user_id'] == user_id]
        payment = reduce(lambda x, y: x.get('asset', 0) + y.get('asset', 0), as_payer) if len(as_payer) else 0
        benefit = reduce(lambda x, y: x.get('asset', 0) + y.get('asset', 0), as_payee) if len(as_payee) else 0
        print('payment:', payment)
        print('benefit:', benefit)
        results[date] = {'payment': payment, 'benefit': benefit, 'net': benefit - payment}
    return True, BalanceReport(**{'records': results})
