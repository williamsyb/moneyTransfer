from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str = None
    is_supervisor: bool = False


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str = None

    class Config:
        orm_mode = True


class UserInDB(UserIn):
    hashed_password: str


class AllUser(BaseModel):
    all_user: List[UserOut]