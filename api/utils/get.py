"""get.py contains functions to get information about files and directories."""

import os
import base64
from typing import Any, Dict


def get_dir_size(path: str) -> int:
    """get_dir_size returns the size of a directory in bytes."""
    total_size = 0

    for dir_path, _, file_names in os.walk(path):
        for file_name in file_names:
            file_path = os.path.join(dir_path, file_name)
            total_size += os.path.getsize(file_path)

    return total_size


def get_file_tree(root_dir: str) -> Dict[str, Any]:
    """get_file_tree returns a dictionary representing the file tree of a directory."""
    file_tree = {
        "name": os.path.basename(root_dir),
        "type": "directory",
        "children": [],
    }

    for file_name in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file_name)

        if os.path.isdir(file_path):
            file_tree["children"].append(get_file_tree(file_path))
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as _file:
                    file_content = _file.read()
            except UnicodeDecodeError:
                with open(file_path, "rb", encoding=None) as _file:
                    file_content = _file.read()

            file_tree["children"].append(
                {"name": file_name, "type": "file", "content": file_content}
            )

    return file_tree


def get_file_size(path: str) -> int:
    """get_file_size returns the size of a file in bytes."""
    return os.stat(path).st_size


def get_file_type(path: str) -> str:
    """get_file_type returns the extension of a file."""
    return path.split(".")[-1]


def get_file_name(path: str) -> str:
    """get_file_name returns the name of a file."""
    return path.split("/")[-1]


def get_file_path(path: str) -> str:
    """get_file_path returns the path of a file."""
    return "/".join(path.split("/")[:-1])


def get_file_content(path: str) -> str:
    """get_file_content returns the content of a file unicode string decoded"""
    with open(path, "r", encoding="utf-8") as _file:
        return _file.read()


def get_file_content_bytes(path: str) -> bytes:
    """get the raw sequence of bytes of a file"""
    with open(path, "rb") as _file:
        return _file.read()


def get_base64(content: str) -> bytes:
    """get the base64 encoded content of a file"""
    return base64.b64decode(content)
