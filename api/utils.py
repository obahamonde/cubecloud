"""Utility functions for the API."""
import socket
from uuid import uuid4
from secrets import token_urlsafe
from datetime import datetime
from random import randint, choice
from names import get_first_name, get_last_name
from rich.console import Console

pprint = Console().log


def gen_oid() -> str:
    """Generate a unique object id."""
    return str(uuid4())


def gen_now() -> str:
    """Generate a timestamp."""
    return datetime.now().isoformat()


def gen_ip() -> str:
    """Generate a random ip address."""
    return ".".join([str(randint(0, 255)) for _ in range(4)])


def gen_name() -> str:
    """Generate a random name."""
    return f"{get_first_name()}{get_last_name()}"


def gen_password() -> str:
    """Generate a random password."""
    return "".join(
        [
            choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")
            for _ in range(randint(8, 16))
        ]
    )


def gen_secret() -> str:
    """Generate a random secret."""
    return token_urlsafe(32)


def gen_port() -> int:
    """Generate a random port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port
