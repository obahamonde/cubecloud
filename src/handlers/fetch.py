import aiohttp
from typing import Dict, Optional, Union, Any

async def fetch(    
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
) -> Union[str, bytes, Dict[str, Any]]:
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=method, url=url, headers=headers, data=body,
            json=json
        ) as response:
            if response.content_type.endswith("json"):
                return await response.json()
            if response.content_type.startswith("text/"):
                return await response.text()
            return await response.read()    
