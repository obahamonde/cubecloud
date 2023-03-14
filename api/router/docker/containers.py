from typing import Any, Dict, List

from aiohttp import ClientSession

from fastapi import APIRouter, status

from fastapi.responses import PlainTextResponse, JSONResponse

from jinja2 import Template

from api.config import env




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
        
@app.post("/", response_class=JSONResponse)
async def create_container() -> Dict[str,Any]:
    """Create a container"""
    async with ClientSession() as session:
        async with session.post(f"{app.base_url}/containers/create") as response:
            if response.status == status.HTTP_200_OK:
                return await response.json()
            return {}
        
@app.get("version", response_class=JSONResponse)
async def get_version() -> Dict[str,Any]:
    """Get version"""
    async with ClientSession() as session:
        async with session.get(f"{app.base_url}/version") as response:
            if response.status == status.HTTP_200_OK:
                return await response.json()
            return {}