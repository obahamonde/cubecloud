import os

import base64

import json

import asyncio

from typing import Any, Dict, Optional, AsyncGenerator, Union, List

from aiohttp import ClientSession

from fastapi import APIRouter

from api.config import env

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {env.GITHUB_TOKEN}",
}


async def fetch(url: str) -> Union[str, bytes, Dict[str, Any]]:
    """

    Fetches the content of a URL.


    :param url: The URL to fetch.


    :return: The content of the URL.

    """

    async with ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()

            if response.content_type == "application/json":
                return await response.json()

            if response.content_type.startswith(
                "text/"
            ) or response.content_type.startswith("application/"):
                return await response.text()

            return await response.read()


def build_url(
    owner: str,
    repo: str,
    command: str,
    sha: Optional[str] = None,
    recursive: Optional[str] = None,
) -> str:
    """

    Builds the URL for the GitHub API.


    :param owner: The owner of the repository.

    :param repo: The name of the repository.

    :param command: The command to execute. Options: [commits, git/trees]

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


async def get_latest_commit_sha(owner: str, repo: str) -> str:
    """

    Gets the SHA of the latest commit in the repository.


    :return: The SHA of the latest commit.
    """

    url = build_url(owner, repo, "commits")

    async with ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()

            return (await response.json())[0]["sha"]


app = APIRouter(prefix="/github", tags=["github"])


@app.get("/{owner}/{repo}")
async def get_tree_recursive(owner: str, repo: str):
    """

    Gets the tree of a commit recursively.


    :param sha: The SHA of the commit.

    :return: The tree of the commit.
    """
    sha = await get_latest_commit_sha(owner, repo)

    url = build_url(owner, repo, "git/trees", sha, "1")

    async with ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()

            response = await response.json()

            blobs = await asyncio.gather(
                *[
                    fetch(blob["url"])
                    for blob in response["tree"]
                    if blob["type"] == "blob"
                ]
            )

            responses = []

            for i, blob in enumerate(blobs):
                if "content" in blob:
                    try:
                        blob["content"] = base64.b64decode(blob["content"]).decode(
                            "utf-8"
                        )

                    except:
                        continue

                    try:
                        blob["path"] = response["tree"][i]["path"]
                    except:
                        continue

                    responses.append(
                        {
                            "path": blob["path"],
                            "content": blob["content"],
                            "size": blob["size"],
                        }
                    )

            return responses
