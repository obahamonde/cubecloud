from typing import Dict, List, AsyncGenerator
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module
from fastapi import WebSocket


class HMRSocketPayload(BaseModel):
    """Payload for HMR WebSocket messages."""

    path: str = Field(...)
    content: str = Field(...)
    sub: str = Field(...)
