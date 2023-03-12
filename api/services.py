import json

from typing import List

from httpx import AsyncClient

from jinja2 import Template

from aiogoogle import Aiogoogle

from api.config import env

from api.schemas import DBContainer, User



class DockerService:

    """Docker Service"""


    def __init__(self):

        """Initialize the DockerService"""

        self.base_url = env.DOCKER_URL


    async def get_containers(self) -> List[dict]:

        """Return a list of containers"""

        async with AsyncClient() as client:

            response = await client.get(f"{self.base_url}/containers/json")

            return response.json()


    async def get_container(self, name: str) -> dict:

        """Return a container"""

        async with AsyncClient() as client:

            response = await client.get(f"{self.base_url}/containers/{name}/json")

            return response.json()


    async def logs(self, name: str) -> str:

        """Return a container logs"""

        async with AsyncClient() as client:

            response = await client.get(f"{self.base_url}/containers/{name}/logs")

            return response.text


    async def start_container(self, name: str) -> dict:

        """Start a container"""

        async with AsyncClient() as client:

            response = await client.post(f"{self.base_url}/containers/{name}/start")

            return response.json()


    async def stop_container(self, name: str) -> dict:

        """Stop a container"""

        async with AsyncClient() as client:

            response = await client.post(f"{self.base_url}/containers/{name}/stop")

            return response.json()


    async def remove_container(self, name: str) -> dict:

        """Remove a container"""

        async with AsyncClient() as client:

            response = await client.post(f"{self.base_url}/containers/{name}/remove")

            return response.json()


    async def create_container(self, container: DBContainer) -> dict:

        """Create a container"""

        async with AsyncClient() as client:

            template = Template(open(f"templates/{container.image}.j2").read())

            data = template.render(**container.dict())

            response = await client.post(

                f"{self.base_url}/containers/create", json=data
            )

            return response.json()

    async def pull_image(self, image: str) -> dict:

        """Pull an image"""

        async with AsyncClient() as client:

            response = await client.post(f"{self.base_url}/images/create?fromImage={image}")

            return response.json()

    async def get_images(self) -> List[dict]:
            
            """Return a list of images"""
    
            async with AsyncClient() as client:
    
                response = await client.get(f"{self.base_url}/images/json")
    
                return response.json()

class Auth:


    """Auth0 Service"""


    async def user_info(self, token: str) -> User:

        """Return user info"""

        async with AsyncClient() as client:

            response = await client.get(

                f"https://{env.AUTH0_DOMAIN}/userinfo",

                headers={"Authorization": f"Bearer {token}"},
            )

            user_dict = response.json()

            print(user_dict)

            user = User(**user_dict)

            user.create_user()
            return user

