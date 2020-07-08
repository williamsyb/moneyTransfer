from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import config
from sqlalchemy import create_engine

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL  # only sqlite needs "check_same_thread"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_db_():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
