import asyncio

import time

from typing import Any, Dict, List, Optional, AsyncGenerator

from aiohttp import ClientSession

from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect

from fastapi.responses import PlainTextResponse, JSONResponse

from api.config import env

from api.data.schemas import ContainerConfig, ProxyConfig

from api.utils.gen import gen_name, gen_port

from api.hooks.fetch import fetch

app = APIRouter(tags=["docker"])


async def pull_image(image: str):
    """Pull image"""
    async with ClientSession() as session:
        async with session.post(
            f"{env.DOCKER_URL}/images/create?fromImage={image}"
        ) as response:
            if response.status == status.HTTP_200_OK:
                return {
                    "message": "Image up to date",
                    "status": "success",
                }
            elif response.status == status.HTTP_201_CREATED:
                return {
                    "message": "Image created",
                    "status": "success",
                }
            else:
                return {
                    "message": "Something went wrong",
                    "status": "error",
                }


async def start_container(container: str):
    """Start container"""
    async with ClientSession() as session:
        async with session.post(
            f"{env.DOCKER_URL}/containers/{container}/start"
        ) as response:
            return response


async def get_container(container: str) -> Dict[str, Any]:
    """Get container"""
    async with ClientSession() as session:
        async with session.get(
            f"{env.DOCKER_URL}/containers/{container}/json"
        ) as response:
            return await response.json()


async def get_container_logs(container: str) -> AsyncGenerator[bytes, None]:
    async with ClientSession() as session:
        async with session.get(
            f"{env.DOCKER_URL}/containers/{container}/logs?stdout=1&stderr=1&since={int(time.time())-86400}&follow=0&timestamps=1",
        ) as response:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                yield chunk


@app.get("/containers", response_class=JSONResponse)
async def get_containers() -> List[Dict[str, Any]]:
    """
    Returns a list of all containers running on the Docker host, along with their metadata.
    Args:
    None

    Returns:
    A list of dictionaries representing each container, with the following fields:
    - Id: The container's unique identifier
    - Name: The container's name
    - Image: The name of the image used to create the container
    - State: The container's current state (running, stopped, etc.)
    - Created: The timestamp of when the container was created
    - Ports: A list of port mappings for the container
    - Labels: A dictionary of key-value pairs representing metadata about the container
    """
    containers = await fetch("GET",f"{env.DOCKER_URL}/containers/json?all=1",{
        "Content-Type": "application/json"
    })
    
    return await asyncio.gather(*[get_container(container["Id"]) for container in containers])

@app.post("/containers/{name}", response_class=JSONResponse)
async def create_container(name: str, container: ContainerConfig) -> Dict[str, Any]:
    """
    Creates a new Docker container with the specified name and configuration.
    Args:
    - name: The name to assign to the new container
    - container: An object representing the configuration of the new container, with the following fields:
        - image: The name of the Docker image to use
        - shell: The shell to use inside the container (e.g. "/bin/bash")
        - cmd: The command to run inside the container
        - environment: A list of environment variables to set inside the container
        - container_port: The port number to expose on the container
        - host_port: The port number to map the container port to on the Docker host
        - protocol: The protocol to use (e.g. "tcp")

    Returns:
        A dictionary representing the newly created container, with the following fields:
        - Id: The container's unique identifier
        - Name: The container's name
        - Image: The name of the image used to create the container
        - State: The container's current state (running, stopped, etc.)
        - Created: The timestamp of when the container was created
        - Ports: A list of port mappings for the container
        - Labels: A dictionary of key-value pairs representing metadata about the container
    """

    payload = {
        "Image": container.image,
        "Shell": container.shell,
        "Cmd": container.cmd,
        "Env": container.environment,
        "ExposedPorts": {
            f"{container.container_port}/{container.protocol}": {
                "HostPort": str(container.host_port)
            }
        },
        "HostConfig": {
            "PortBindings": {
                f"{container.container_port}/{container.protocol}": [
                    {"HostPort": str(container.host_port)}
                ]
            }
        },
    }
    async with ClientSession() as session:
        async with session.post(
            f"{env.DOCKER_URL}/containers/create?name={name}", json=payload
        ) as response:
            image_status = await pull_image(container.image)
            if image_status["status"] == "success":
                id_ = (await response.json())["Id"]
                await start_container(id_)
                return await get_container(id_)
            else:
                return image_status


@app.delete("/containers/{container}")
async def delete_container(container: str):
    """
    Stops and removes the specified Docker container.
    Args:
    - container: The name or ID of the container to remove

    Returns:
        A dictionary with a "message" field describing the result of the operation ("Container deleted" if successful),
        and a "status" field indicating the status of the operation ("success" or "error").
    """

    async with ClientSession() as session:
        async with session.delete(
            f"{env.DOCKER_URL}/containers/{container}"
        ) as response:
            if response.status == status.HTTP_204_NO_CONTENT:
                return {
                    "message": "Container deleted",
                    "status": "success",
                }
            else:
                return {
                    "message": "Something went wrong",
                    "status": "error",
                }


@app.get("/containers/{container}/logs", response_class=PlainTextResponse)
async def get_logs(container: str):
    """
    Returns the logs for the specified Docker container.
    Args:
    - container: The name or ID of the container to get logs for

    Returns:
        A string representing the logs for the container.
    """
    response_body = b""

    async for chunk in get_container_logs(container):
        response_body += chunk

    return PlainTextResponse(response_body.decode(encoding="ascii", errors="ignore"))


@app.get("/containers/{container}/stats", response_class=JSONResponse)
async def get_container_stats(container: str) -> Dict[str, Any]:

    """
    Returns statistics about the specified Docker container.
    
    Args:
    - container: The name or ID of the container to get statistics for

    Returns:
    A dictionary containing various statistics about the container, including:
    - CPU usage
    - Memory usage
    - Network I/O
    - Block I/O
    """

    async with ClientSession() as session:
        async with session.get(
            f"{env.DOCKER_URL}/containers/{container}/stats?stream=0"
        ) as response:
            return await response.json()


@app.post("/containers/{container}/{image}", response_class=JSONResponse)
async def deploy_container(
    container: str, image: str, port: int = 8080, env_vars: str = "DOCKER=1",
) -> Dict[str, Any]:
    """
    Endpoint for deploying a container with the specified image and configuration.

    Args:
        container (str): The name of the container.
        image (str): The image to use for the container.
        cmd (str, optional): The command to run in the container. Defaults to "".
        port (int, optional): The port to expose on the container. Defaults to 8080.
        env_vars (str, optional): Environment variables to set in the container. Defaults to "DOCKER=1".

    Returns:
        dict: A dictionary containing information about the deployed container.
    """
    host_port = str(gen_port())
    payload = {
        "Image": image,
        "Env": env_vars.split(" "),
        "ExposedPorts": {f"{str(port)}/tcp": {"HostPort": host_port}},
        "HostConfig": {"PortBindings": {f"{str(port)}/tcp": [{"HostPort": host_port}]}},
    }
    async with ClientSession() as session:
        async with session.post(
            f"{env.DOCKER_URL}/containers/create?name={container}", json=payload
        ) as response:
            id_ = (await response.json())["Id"]
            await start_container(id_)
            return await get_container(id_)


@app.put("/containers/{container}", response_class=JSONResponse)
async def expose_container(
    container: str, port: int, subdomain: Optional[str] = None
) -> Dict[str, Any]:
    """
    Endpoint for exposing a container on a subdomain.

    Args:
        container (str): The name of the container.
        port (int): The port to expose on the container.
        subdomain (str, optional): The subdomain to use for the exposed container. If None, a random subdomain will be generated. Defaults to None.

    Returns:
        dict: A dictionary containing information about the exposed container, including the URL at which it can be accessed.
    """
    nginx_conf = NginxConf(
        container_name=container, container_port=port, subdomain=subdomain
    )
    await create_record(nginx_conf.subdomain if nginx_conf.subdomain else gen_name(32))
    async with ClientSession() as session:
        async with session.post(
            "https://smartpro.solutions/",
            json=nginx_conf.dict(),
            headers={"Content-Type": "application/json"},
        ) as response:
            ack = await response.text()
            if ack == "OK":
                return {
                    "message": "Container provisioned",
                    "status": "success",
                    "url": f"https://{nginx_conf.subdomain}.smartpro.solutions",
                }
            else:
                return {
                    "message": "Something went wrong",
                    "status": "error",
                }


@app.get("/images", response_class=JSONResponse)
async def get_images() -> List[Dict[str, Any]]:
    """
    Returns a list of Docker images.
    Returns:
        A list of dictionaries containing information about the images.
    """
    async with ClientSession() as session:
        async with session.get(f"{env.DOCKER_URL}/images/json") as response:
            return await response.json()


@app.websocket("/containers/{container}/attach")
async def attach_container(websocket: WebSocket, container: str):
    """Attachs the current host to a remote Docker
        Container, in order to interact with it
        It's intended to be used as a Web CLI for the
        container remote troubleshooting
    Args:
        websocket (WebSocket): The websocket connection
        container (str): The container ID
    """
    async with ClientSession() as session:
        async with session.post(
            f"{env.DOCKER_URL}/containers/{container}/attach?stream=1&stdin=1&stdout=1&stderr=1",
            headers={"Connection": "Upgrade", "Upgrade": "tcp"},
        ) as response:
            async with session.ws_connect(
                f"{env.DOCKER_URL}/containers/{container}/attach/ws?stream=1&stdin=1&stdout=1&stderr=1"
            ) as ws:
                await websocket.accept()
                while True:
                    try:
                        data = await websocket.receive_text()
                        await ws.send_str(data)
                    except WebSocketDisconnect:
                        break
                    except Exception as e:
                        print(e)
                        break
                await ws.close()
