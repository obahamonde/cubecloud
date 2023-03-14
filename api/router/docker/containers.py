from typing import Any, Dict, List

from aiohttp import ClientSession

from fastapi import APIRouter, status

from fastapi.responses import PlainTextResponse, JSONResponse

from jinja2 import Template

from api.config import env

from api.schemas import DBContainer


class ContainerRouter(APIRouter):

    """Docker Service"""

    def __init__(self):
        """Initialize the DockerService"""

        super().__init__(prefix="/containers", tags=["containers"])

        self.base_url = env.DOCKER_URL


app = ContainerRouter()

@app.get("/", response_class=JSONResponse)
async def get_containers() -> List[Dict[str,Any]]:
    """Get containers"""
    async with ClientSession() as session:
        async with session.get(f"{app.base_url}/containers/json") as response:
            if response.status == status.HTTP_200_OK:
                return await response.json()
            return []