from pydantic import BaseModel
from typing import Dict, List


class UserBalance(BaseModel):
    id: int

    class Config:
        orm_mode = True


class BalanceReport(BaseModel):
    records: Dict[str, Dict[str, float]]

    class Config:
        orm_mode = True
