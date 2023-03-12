from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File


from fastapi.responses import JSONResponse, PlainTextResponse,StreamingResponse


from api.services import Auth, DockerService,  AsyncClient


from api.schemas import DBContainer, User


from api.config import env


import base64

from api.google import Storage




class DockerRouter(APIRouter):


    """Docker Router"""



    @property


    def client(self):


        return DockerService()



    @property


    def auth(self):


        return Auth()



    def __init__(self):


        """Initialize the DockerRouter"""


        super().__init__(prefix="/docker", tags=["docker"])



        @self.get("/containers")


        async def get_containers():


            """Return a list of containers"""


            return await self.client.get_containers()



        @self.get("/containers/{name}")


        async def get_container(name: str):


            """Return a container"""


            return await self.client.get_container(name)



        @self.get("/containers/{name}/logs")


        async def get_logs(name: str):


            """Return a container logs"""


            return await self.client.logs(name)



        @self.post("/containers/{name}/start")


        async def start_container(name: str):


            """Start a container"""


            return await self.client.start_container(name)



        @self.post("/containers/{name}/stop")


        async def stop_container(name: str):


            """Stop a container"""


            return await self.client.stop_container(name)



        @self.post("/containers/{name}/remove")


        async def remove_container(name: str):


            """Remove a container"""


            return await self.client.remove_container(name)



        @self.post("/containers/create")


        async def create_container(container: DBContainer):


            """Create a container"""


            return await self.client.create_container(container)

        @self.get("/images/{image}/pull")
        
        async def pull_container(image: str):
            
            """Pull a container"""
            
            return await self.client.pull_image(image)

        @self.get("/images")

        async def get_images():
            
            """Get images"""
            
            return await self.client.get_images()
        

class UserRouter(APIRouter):


    """Router for user authentication with Auth0"""



    def __init__(self):


        super().__init__(prefix="/auth", tags=["user"])


        self.auth = Auth()



        @self.get("/")


        async def get_user_info(token: str):


            """Return user info"""


            return await self.auth.user_info(token)
        
        
        

class GCSRouter(APIRouter):

    """Router for Google Cloud Storage"""

    def __init__(self):

        super().__init__(prefix="/storage", tags=["storage","GCS API","Google Cloud Storage"])
        self.google = Storage()
        
        @self.post("/")
        async def put_object_endpoint(key: str, file: UploadFile = File(...)):

            """Upload a file to Google Cloud Storage"""

            return await self.google.upload_file(
                file.file.read(), key, file.content_type or "application/octet-stream"
            )
        
        @self.get("/buckets")
        async def get_buckets():
            return await self.google.list_storage_buckets()
        
    
        @self.get("/objects")
        async def get_objects():
            return await self.google.get_objects_from_bucket()
        
        @self.post("/objects")
        async def upload_object(key: str, file: UploadFile = File(...)):
            chunks =  await self.google.upload_file(
                file.file, key, file.content_type or "application/octet-stream"
            )
            print(chunks)