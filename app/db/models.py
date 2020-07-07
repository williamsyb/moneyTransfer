from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime as dt
from .database import Base
from app.config.config import config
from sqlalchemy import create_engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(30), nullable=False)
    full_name = Column(String(30))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    is_active = Column(Boolean, default=True)
    balance = relationship("Balance", back_populates="User")


class Balance(Base):
    # __tablename__ = "balance"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="balance")


class TransferAction(Base):
    __tablename__ = 'transfer_action'
    id = Column(Integer, primary_key=True, index=True)
    asset_start_user_id = Column(Integer, ForeignKey('users.id'))
    asset_start_user = relationship('User')
    asset_end_user_id = Column(Integer, ForeignKey('users.id'))
    asset_end_user = relationship('User')
    asset = Column(Float)
    timestamp = Column(DateTime, default=dt.utcnow, index=True)


class Reports(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL  # only sqlite needs "check_same_thread"
)
Base.metadata.create_all(bind=engine)
