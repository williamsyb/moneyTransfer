from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.api_v1.api import api_router
from auth.auth_http import auth_router

origins = [
    "http://localhost",
    "http://localhost:8080",
]


def make_app():
    app = FastAPI()
    app.include_router(api_router, prefix='/api/v1')
    app.include_router(auth_router)
    add_middleware(app)

    return app


def add_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
