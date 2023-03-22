import os
import io
import json
import tarfile
from typing import Any, Dict, Optional, Union
from aiohttp import ClientSession
from fastapi import APIRouter
from src.config import env
from src.utils.misc import build_file_tree

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {env.GITHUB_TOKEN}",
}


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


async def fetch(method: str, url: str, **kwargs: Any) -> Union[Dict, str, bytes]:
    """
    Generic fetch coroutine. That can be used to make any HTTP request.

    :param method: The HTTP method to use. Options: [GET, POST, PUT, DELETE]
    :param url: The URL to make the request to.
    :param kwargs: Any additional arguments to pass to the request.
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


async def git_clone(owner: str, repo: str):
    """
    Downloads the latest code for the given GitHub repository.
    :param owner: The owner of the repository.
    :param repo: The name of the repository.

    :return: The contents of the downloaded repository as a file tree.
    """
    async with ClientSession() as session:
        sha = await get_latest_commit_sha(owner, repo)
        async with session.get(
            f"https://api.github.com/repos/{owner}/{repo}/tarball", headers=HEADERS
        ) as response:
            response.raise_for_status()
            content = await response.read()
            tarball = tarfile.open(fileobj=io.BytesIO(content), mode="r:gz")
            os.makedirs(f"containers/{sha}", exist_ok=True)
            tarball.extractall(path=f"containers/{sha}")
            return build_file_tree(f"containers/{sha}")


async def git_commit(owner: str, repo: str):
    """
    Downloads the latest code for the given GitHub repository.
    :param owner: The owner of the repository.
    :param repo: The name of the repository.

    :return: The contents of the downloaded repository as a file tree.
    """
    async with ClientSession() as session:
        sha = await get_latest_commit_sha(owner, repo)
        async with session.get(
            f"https://api.github.com/repos/{owner}/{repo}/tarball", headers=HEADERS
        ) as response:
            content = await response.read()
            tarball = tarfile.open(fileobj=io.BytesIO(content), mode="r:gz")
            os.makedirs(f"containers/{sha}", exist_ok=True)
            tarball.extractall(path=f"containers/{sha}")
            return build_file_tree(f"containers/{sha}")


async def git_push_origin_main(owner: str, repo: str):
    """
    Downloads the latest code for the given GitHub repository.
    :param owner: The owner of the repository.
    :param repo: The name of the repository.

    :return: The contents of the downloaded repository as a file tree.
    """
    async with ClientSession() as session:
        sha = await get_latest_commit_sha(owner, repo)
        async with session.get(
            f"https://api.github.com/repos/{owner}/{repo}/tarball", headers=HEADERS
        ) as response:
            content = await response.read()
            tarball = tarfile.open(fileobj=io.BytesIO(content), mode="r:gz")
            os.makedirs(f"containers/{sha}", exist_ok=True)
            tarball.extractall(path=f"containers/{sha}")
            return build_file_tree(f"containers/{sha}")


'''
async def docker_build(owner: str, repo: str):
    """
    Builds a Docker image from the latest code for the given GitHub repository.
    :param owner: The owner of the repository.
    :param repo: The name of the repository.
    :return: The output of the Docker build.
    """
    async with ClientSession() as session:
        sha = await get_latest_commit_sha(owner, repo)
        async with session.get(
            f"https://api.github.com/repos/{owner}/{repo}/tarball", headers=HEADERS
        ) as response:
            response.raise_for_status()
            local_path = f"{owner}-{repo}-{sha[:7]}"
            build_args = json.dumps({"LOCAL_PATH": local_path})
            content = await response.read()
            async with session.post(
                f"{env.DOCKER_URL}/build?dockerfile={local_path}/Dockerfile&buildargs={build_args}",
                data=content,
            ) as response:
                return await response.text()


app = APIRouter(prefix="/build", tags=["build"])


@app.post("/{owner}/{repo}")
async def build(owner: str, repo: str):
    """
    Builds a Docker image from the latest code for the given GitHub repository.
    :param owner: The owner of the repository.
    :param repo: The name of the repository.
    :return: The output of the Docker build.
    """
    return await docker_build(owner, repo)


@app.get("/repos/{owner}/{repo}")
async def git_clone_endpoint(owner: str, repo: str):
    """
    Downloads the latest code for the given GitHub repository.
    :param owner: The owner of the repository.
    :param repo: The name of the repository.
    :return: The contents of the downloaded repository as a file tree.
    """
    return await git_clone(owner, repo)
'''

app = APIRouter(prefix="/build", tags=["build"])
