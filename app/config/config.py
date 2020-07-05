import os
# https://fastapi.tiangolo.com/advanced/settings/
env = os.environ.get('WORKING_ENV', 'dev')
if env == 'dev':
    from .config_dev import *
    config = ConfigDev
elif env == 'prod':
    from .config_prod import *
    config = ConfigProd


# from fastapi import FastAPI
# from pydantic import BaseSettings
#
#
# class Settings(BaseSettings):
#     app_name: str = "Awesome API"
#     admin_email: str
#     items_per_user: int = 50
#
#
# settings = Settings()
# app = FastAPI()
#
#
# @app.get("/info")
# async def info():
#     return {
#         "app_name": settings.app_name,
#         "admin_email": settings.admin_email,
#         "items_per_user": settings.items_per_user,
#     }
