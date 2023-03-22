from fastapi import APIRouter
from src.api.containers import app as docker_app
from src.api.auth import app as auth_app
from src.api.build import app as build_app


class API(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "/api"

    def use(self, router: APIRouter):
        self.include_router(router)
        return self


app = API().use(docker_app).use(build_app).use(auth_app)
