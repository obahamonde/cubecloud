import os

import base64

import json

import asyncio

from typing import Any, Dict, Optional, AsyncGenerator, Union, List

from aiohttp import ClientSession

from fastapi import APIRouter, Request

from api.config import env


class CloudFlareRouter(APIRouter):
    """
    The endpoints for interacting with CloudFlare REST API.
    """

    def __init__(self):
        super().__init__(prefix="/cloudflare", tags=["CloudFlare"])
        self._headers = {
            "X-Auth-Email": env.CF_EMAIL,
            "X-Auth-Key": env.CF_API_KEY,
            "Content-Type": "application/json",
        }
                
        @self.get("/{name}")
        async def create_record(name:str):
            """
            Create a record.
            """
            async with ClientSession() as session:
                json_data = {
                    "type": "A",
                    "name": name,
                    "content": env.DOCKER_IP,
                    "ttl": 1,
                    "proxied": True,
                }
                async with session.post(
                    f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records",
                    headers=self._headers,
                    json=json_data,
                ) as resp:
                    return await resp.json()
                    
                
        @self.get("/")
        async def get_records():
            """
            Get all records.
            """
            async with ClientSession() as session:
                async with session.get(
                    f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records",
                    headers=self._headers,
                ) as resp:
                    return await resp.json()
    
        @self.delete("/{record_id}")
        async def delete_record(record_id:str):
            """
            Delete a record.
            """
            async with ClientSession() as session:
                async with session.delete(
                    f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/dns_records/{record_id}",
                    headers=self._headers,
                ) as resp:
                    return await resp.json()
                
        @self.get("/purge/{name}")
        async def purge_cache(name:str):
            """
            Purge cache.
            """
            async with ClientSession() as session:
                json_data = {
                    "files": [f"https://{name}"]
                }
                async with session.post(
                    f"https://api.cloudflare.com/client/v4/zones/{env.CF_ZONE_ID}/purge_cache",
                    headers=self._headers,
                    json=json_data,
                ) as resp:
                    return await resp.json()
    
app = CloudFlareRouter()