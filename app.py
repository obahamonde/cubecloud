import os
import json
import asyncio
from aiohttp import ClientSession
from typing import Any, Dict
from api.config import env
from typing import *
from rich.console import Console
import base64

print = Console().log

run = asyncio.get_event_loop().run_until_complete

HEADERS = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {env.GITHUB_TOKEN}"
}


async def fetch(url:str)->str:
    
    """
    Fetches the content of a URL.

    :param url: The URL to fetch.

    :return: The content of the URL.

    """
    
    
    async with ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()
            return await response.text()

def build_url(owner:str,repo:str,command:str,sha:Optional[str]=None,recursive:Optional[str]=None)->str:
    
    """
    Builds the URL for the GitHub API.

    :param owner: The owner of the repository.
    :param repo: The name of the repository.
    :param command: The command to execute.
    :param sha: The SHA of the commit.
    :param recursive: Whether to get the tree recursively.

    :return: The URL for the GitHub API.
    
    """
    
    
    url = f"https://api.github.com/repos/{owner}/{repo}/{command}"
    if sha:
        url += f"/{sha}"
    if recursive:
        url += f"?recursive={recursive}"
    return url



async def get_latest_commit_sha(owner:str,repo:str) -> str:
    """
    Gets the SHA of the latest commit in the repository.
    
    :return: The SHA of the latest commit.
    """
    url = build_url(owner,repo,"commits")
    async with ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()
            return (await response.json())[0]["sha"]
            
            
            
           
async def get_tree_recursive(owner:str,repo:str, sha: str) -> Dict[str, Any]:
    """
    Gets the tree of a commit recursively.
    
    :param sha: The SHA of the commit.
    :return: The tree of the commit.
    """
    url = build_url(owner,repo,"git/trees",sha,"1")
    async with ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()
            return (await response.json())["tree"]

async def get_payload(repo:str,owner:str):
    
    """
    Gets the payload of the repository.

    :param repo: The name of the repository.
    :param owner: The owner of the repository.

    :return: The payload of the repository.

    """
    
    
    
    sha = await get_latest_commit_sha(owner,repo)
    tree = await get_tree_recursive(owner,repo,sha)
    for t in tree:
        if t["type"] == "blob":
            url = t["url"]
            payload = await fetch(url)
            payload = json.loads(payload)
            try:
                payload["content"] = base64.b64decode(payload["content"]).decode("utf-8")
            except:
                payload["content"] = payload["content"]
            yield {
                "path": t["path"],
                "content": payload["content"].strip()
            }
        
        
async def git_clone(owner:str,repo:str,dest:str):
    
    """
    
    Clones a repository.
    
    :param owner: The owner of the repository.
    
    :param repo: The name of the repository.
    
    :param dest: The destination to clone the repository to.
    
    """
    
    async for payload in get_payload(repo,owner):
        path = os.path.join(dest,payload["path"])
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,"w") as f:
            f.write(payload["content"])