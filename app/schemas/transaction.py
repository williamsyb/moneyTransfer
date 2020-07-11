from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime


class UserTransfer(BaseModel):
    id: int

    class Config:
        orm_mode = True


class TransferRecord(BaseModel):
    asset_start_user: str
    asset: float
    asset_end_user: str
    timestamp: datetime

    class Config:
        orm_mode = True


class HistoryTransaction(BaseModel):
    records: Dict[str, List[TransferRecord]]
