from utils.utils import Singleton


class ConfigQA(metaclass=Singleton):
    SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://{}:{}@{}:{}/{}'.format('root', '123456', 'node01', '3306',
                                                                      'MONEYTRANS')
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
