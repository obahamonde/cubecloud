from typing import List
from httpx import AsyncClient
from fastapi import APIRouter
from api.config import env


class ImagesRouter(APIRouter):

    """Docker Service"""

    def __init__(self):
        """Initialize the DockerService"""

        super().__init__(prefix="/images", tags=["images"])

        self.base_url = env.DOCKER_URL

        @self.get("/")
        async def get_images() -> List[dict]:
            """Return a list of images"""

            async with AsyncClient() as client:
                response = await client.get(f"{self.base_url}/images/json")

                return response.json()

        @self.get("/{name}")
        async def get_image(name: str) -> dict:
            """Return an image"""

            async with AsyncClient() as client:
                response = await client.get(f"{self.base_url}/images/{name}/json")

                return response.json()

        @self.post("/{name}")
        async def pull_image(name: str) -> dict:
            """Pull an image"""

            async with AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/images/create?fromImage={name}"
                )

                return response.json()

        @self.delete("/{name}")
        async def remove_image(name: str) -> dict:
            """Remove an image"""

            async with AsyncClient() as client:
                response = await client.delete(f"{self.base_url}/images/{name}")

                return response.json()


app = ImagesRouter()
