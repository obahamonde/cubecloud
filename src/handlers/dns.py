import json

import asyncio

from typing import Any, Dict, Optional, AsyncGenerator, Union, List

from aiohttp import ClientSession

from random import choice

from src.config import env

from src.utils.gen import gen_port

from src.handlers.fetch import fetch


CF_HEADERS = {
    "X-Auth-Email": env.CF_EMAIL,
    "X-Auth-Key": env.CF_API_KEY,
    "Content-Type": "application/json",
}

UA_HEADERS = [
    {
        "Mozilla/5.0": " (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0": " (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0": " (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0": " (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0": " (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0": " (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0": " (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    }
]


async def create_dns_record(name: str):
    """
    Create a record.
    """
    json_data = json.dumps(
        {"type": "A", "name": name, "content": env.DOCKER_IP, "ttl": 1, "proxied": True}
    )
    return await fetch(
        "POST",
        f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records",
        headers=CF_HEADERS,
        body=json_data.encode("utf-8"),
    )


async def get_dns_records():
    """
    Get all records.
    """

    return await fetch(
        "GET",
        f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records",
        headers=CF_HEADERS,
    )


async def delete_dns_record(record_id: str):
    """
    Delete a record.
    """
    async with ClientSession() as session:
        async with session.delete(
            f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records/{record_id}",
            headers=CF_HEADERS,
        ) as resp:
            return await resp.json()


async def update_dns_record(record_id: str, name: str):
    """
    Update a record.
    """
    json_data = json.dumps(
        {"type": "A", "name": name, "content": env.DOCKER_IP, "ttl": 1, "proxied": True}
    )
    return await fetch(
        "PUT",
        f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records/{record_id}",
        headers=CF_HEADERS,
        body=json_data.encode("utf-8"),
    )


async def deploy_container_from_repo(
    container: str, image: str, port: int = 8080, env_vars: str = "DOCKER=1"
):
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
    return await fetch(
        "POST",
        f"{env.DOCKER_URL}/containers/create?name={container}",
        headers={"Content-Type": "application/json"},
        body=json.dumps(payload).encode("utf-8"),
    )
