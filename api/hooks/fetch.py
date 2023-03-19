import aiohttp
from typing import Dict, Optional, Union, Any

async def fetch(
    method: str,
    url : str,
    headers: Dict[str, str],
    body: Optional[bytes] = None,
)->Union[str, bytes, Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=method, url=url, headers=headers, data=body
        ) as response:
            if response.content_type.endswith("json"):
                return await response.json()
            if response.content_type.startswith("text/"):
                return await response.text()
            return await response.read()