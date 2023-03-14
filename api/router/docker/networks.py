from typing import List
from httpx import AsyncClient
from fastapi import APIRouter
from api.config import env


class NetworksRouter(APIRouter):

    """Docker Service"""

    def __init__(self):
        """Initialize the DockerService"""

        super().__init__(prefix="/networks", tags=["networks"])

        self.base_url = env.DOCKER_URL

        @self.get("/")
        async def get_networks(self) -> List[dict]:
            """Return a list of networks"""

            async with AsyncClient() as client:
                response = await client.get(f"{self.base_url}/networks")

                return response.json()

        @self.get("/{name}")
        async def get_network(self, name: str) -> dict:
            """Return a network"""

            async with AsyncClient() as client:
                response = await client.get(f"{self.base_url}/networks/{name}")

                return response.json()

        @self.post("/")
        async def create_network(self, name: str) -> dict:
            """Create a network"""

            async with AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/networks/create", json={"Name": name}
                )

                return response.json()

        @self.delete("/{name}")
        async def remove_network(self, name: str) -> dict:
            """Remove a network"""

            async with AsyncClient() as client:
                response = await client.delete(f"{self.base_url}/networks/{name}")

                return response.json()

        @self.post("/{name}/connect")
        async def connect_network(self, name: str, container: str) -> dict:
            """Connect a network"""

            async with AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/networks/{name}/connect",
                    json={"Container": container},
                )

                return response.json()

        @self.post("/{name}/disconnect")
        async def disconnect_network(self, name: str, container: str) -> dict:
            """Disconnect a network"""

            async with AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/networks/{name}/disconnect",
                    json={"Container": container},
                )

                return response.json()


app = NetworksRouter()
