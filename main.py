from api import create_app
from api.config import env
from uvicorn import run
from starlette.types import ASGIApp, Receive, Scope, Send
from aiohttp import ClientSession
from fastapi import FastAPI, status, Response

app = create_app()

@app.get("/")
async def compose() -> Response:
    """Compose a docker image"""
    async with ClientSession() as session:
        async with session.get(f"{env.DOCKER_URL}/images/json") as response:
            if response.status == status.HTTP_200_OK:
                return Response(status_code=status.HTTP_200_OK)
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        