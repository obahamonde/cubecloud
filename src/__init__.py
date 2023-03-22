__version__ = "0.1.0"

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from src.api import app as api_router

from src.handlers.fetch import fetch

def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app
