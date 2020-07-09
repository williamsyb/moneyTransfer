from pydantic import BaseModel


class UserTransfer(BaseModel):
    id: int

    class Config:
        orm_mode = True


class TransferRecord(BaseModel):
    asset_start_user: str
    asset: float
    asset_end_user: str

    class Config:
        orm_mode = True

