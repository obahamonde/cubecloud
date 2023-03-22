"""gen.py contains functions for generating random data."""

# imports
import os
import socket
from uuid import uuid4
from secrets import token_urlsafe
from datetime import datetime
from random import randint, choice


def gen_oid() -> str:
    """gen_oid generates a UUID (universally unique identifier), which is useful for identifying objects in a system."""
    return str(uuid4())


def gen_now() -> str:
    """gen_now generates a timestamp string in ISO format, which is useful for tracking the time at which an event occurred."""
    return datetime.now().isoformat()


def gen_name(len_: int) -> str:
    """gen_name generates a random name of a specified length, which could be useful for generating usernames or passwords."""
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    name = None
    while not name or len(name) != len_:
        name = "".join(
            [
                choice(consonants) if i % 2 == 0 else choice(vowels)
                for i in range(randint(1, len_))
            ]
        )
    return name.capitalize()


def gen_password() -> str:
    """gen_password generates a random password of a random length, which could be useful for generating passwords."""
    return "".join(
        [
            choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")
            for _ in range(randint(8, 16))
        ]
    )


def gen_secret() -> str:
    """gen_secret generates a random secret key, which could be useful for generating secret keys."""
    return token_urlsafe(32)


def gen_port() -> int:
    """gen_port generates a random port number, which could be useful for generating port numbers."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port
