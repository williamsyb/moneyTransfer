from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from datetime import datetime as dt
from .database import Base
from config.config import config
from sqlalchemy import create_engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(20), nullable=False)
    full_name = Column(String(30))
    email = Column(String(120), unique=True, index=True)
    hashed_password = Column(String(128))

    is_active = Column(Boolean, default=True)


class Balance(Base):
    __tablename__ = "balance"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(LONGTEXT)  # save json
    year = Column(Integer)
    month = Column(Integer)
    owner_id = Column(Integer)
    owner = Column(String(30), nullable=False)


class TransferAction(Base):
    __tablename__ = 'transfer_action'
    id = Column(Integer, primary_key=True, index=True)
    asset_start_user_id = Column(Integer, nullable=False)
    asset_start_user = Column(String(30), nullable=False)

    asset_end_user_id = Column(Integer, nullable=False)
    asset_end_user = Column(String(30), nullable=False)

    asset = Column(Float)
    timestamp = Column(DateTime, default=dt.utcnow, index=True)


class Reports(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    year=Column(Integer)
    month = Column(Integer)
    content = Column(LONGTEXT)



engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL  # only sqlite needs "check_same_thread"
)
Base.metadata.create_all(bind=engine)
