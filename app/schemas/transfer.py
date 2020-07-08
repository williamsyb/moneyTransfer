from pydantic import BaseModel


class UserOut(BaseModel):
    username: str
    full_name: str = None

    class Config:
        orm_mode = True