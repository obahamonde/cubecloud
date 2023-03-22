import json
from src.config import env
from src.handlers.fetch import fetch


from src.config import env

CF_HEADERS = {
    "X-Auth-Email": env.CF_EMAIL,
    "X-Auth-Key": env.CF_API_KEY,
    "Content-Type": "application/json",
}


async def update_worker(name: str, script: str):
    """
    Update a worker.
    """
    json_data = json.dumps({"name": name, "script": script})
    return await fetch(
        "PUT",
        f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/workers/scripts/{name}",
        headers=CF_HEADERS,
        body=json_data.encode("utf-8"),
    )


async def invoke_worker(name: str):
    """
    Invoke a worker.
    """
    return await fetch(
        "POST",
        f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/workers/scripts/{name}/subdomain",
        headers=CF_HEADERS,
    )


async def get_workers():
    """
    Get all workers.
    """
    return await fetch(
        "GET",
        f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/workers/scripts",
        headers=CF_HEADERS,
    )


async def create_worker(name: str, script: str):
    """
    Create a worker.
    """
    json_data = json.dumps({"name": name, "script": script})
    return await fetch(
        "POST",
        f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/workers/scripts",
        headers=CF_HEADERS,
        body=json_data.encode("utf-8"),
    )
