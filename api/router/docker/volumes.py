from typing import List
from httpx import AsyncClient
from fastapi import APIRouter
from api.config import env


class VolumesRouter(APIRouter):

    """Docker Service"""

    def __init__(self):
        """Initialize the DockerService"""

        super().__init__(prefix="/volumes", tags=["volumes"])

        self.base_url = env.DOCKER_URL

        @self.get("/")
        async def get_volumes(self) -> List[dict]:
            """Return a list of volumes"""

            async with AsyncClient() as client:
                response = await client.get(f"{self.base_url}/volumes")

                return response.json()

        @self.get("/{name}")
        async def get_volume(self, name: str) -> dict:
            """Return a volume"""

            async with AsyncClient() as client:
                response = await client.get(f"{self.base_url}/volumes/{name}")

                return response.json()

        @self.post("/")
        async def create_volume(self, name: str) -> dict:
            """Create a volume"""

            async with AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/volumes/create", json={"Name": name}
                )

                return response.json()

        @self.delete("/{name}")
        async def remove_volume(self, name: str) -> dict:
            """Remove a volume"""

            async with AsyncClient() as client:
                response = await client.delete(f"{self.base_url}/volumes/{name}")

                return response.json()


app = VolumesRouter()
