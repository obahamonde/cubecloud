from fastapi import APIRouter
from api.router.docker.containers import app as container_app
from api.router.docker.volumes import app as volume_app
from api.router.docker.images import app as image_app
from api.router.docker.networks import app as network_app

app = APIRouter(prefix="/docker", tags=["docker"])

app.include_router(container_app)
