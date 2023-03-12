

import functions_framework

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.middleware.wsgi import WSGIMiddleware

from flask import Flask, Request, Response, jsonify

from api.router import UserRouter, DockerRouter, GCSRouter

from mangum import Mangum
from api.google  import Storage


def create_app():

    app = FastAPI()
    app.add_middleware(

        CORSMiddleware,

        allow_origins=["*"],

        allow_credentials=True,

        allow_methods=["*"],

        allow_headers=["*"],
    )

    app.include_router(UserRouter(), prefix="/api")
   

    app.include_router(DockerRouter(), prefix="/api")


    app.include_router(GCSRouter(), prefix="/api")


    @app.get("/api")

    async def root():

        return {"message": "Cube Cloud"}

    return app



