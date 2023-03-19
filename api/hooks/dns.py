import json

from typing import Any, Dict, Optional, AsyncGenerator, Union, List

from aiohttp import ClientSession

from api.config import env

from api.hooks import fetch


CF_HEADERS = {
            "X-Auth-Email": env.CF_EMAIL,
            "X-Auth-Key": env.CF_API_KEY,
            "Content-Type": "application/json",
        }

async def create_record(name: str):
    """
    Create a record.
    """
    json_data = json.dumps({
        "type": "A",
        "name": name,
        "content": env.DOCKER_IP,
        "ttl": 1,
        "proxied": True
    })
    return await fetch("POST", f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records", headers=CF_HEADERS, body=json_data.encode("utf-8"))
async def get_records():
    """
    Get all records.
        """
        
    return await fetch("GET", f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records", headers=CF_HEADERS)
async def delete_record(record_id: str):
    """
    Delete a record.
    """
    async with ClientSession() as session:
        async with session.delete(
            f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records/{record_id}",
            headers=CF_HEADERS,
        ) as resp:
            return await resp.json()



