from fastapi import APIRouter
from api.router.containers import app as docker_app
from api.router.auth import app as auth_app
from api.router.build import app as build_app



class API(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "/api"

    def use(self, router: APIRouter):
        self.include_router(router)
        return self


app = API().use(docker_app).use(build_app).use(auth_app)
