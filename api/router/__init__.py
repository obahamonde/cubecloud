from fastapi import APIRouter
from api.router.docker import app as docker_app
from api.router.github import app as github_app
from api.router.auth import app as oauth2_app
from api.middleware.notifier import app as notifier_app

app = APIRouter(prefix="/api")

app.include_router(notifier_app)

app.include_router(oauth2_app)

app.include_router(docker_app)

app.include_router(github_app)

