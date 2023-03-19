from typing import Optional, List, Dict, Union, Any

from pydantic import BaseModel, Field


class PortBinding(BaseModel):
    """
    Represents a single port binding configuration for a container.

    Fields:
    - HostIp (Optional[str]): The IP address on the host to bind to. Defaults to None.
    - HostPort (str): The port number on the host to bind to. Must be a valid port number.
    """

    host_ip: Optional[str] = Field(
        None, description="The IP address on the host to bind to."
    )
    host_port: str = Field(
        ...,
        description="The port number on the host to bind to.",
        regex=r"^\d{1,5}$",
        example="8080",
    )


class PortMap(BaseModel):
    """
    Represents the port mapping configuration for a container.

    Fields:
    - container_port (int): The port number inside the container. Must be a valid port number.
    - host_port (int): The port number on the host. Must be a valid port number.
    """

    container_port: int = Field(
        ...,
        description="The port number inside the container.",
        ge=1,
        le=65535,
        example=8000,
    )
    host_port: int = Field(
        ..., description="The port number on the host.", ge=1, le=65535, example=8000
    )


class HostConfig(BaseModel):
    """
    Represents the host configuration for a container.

    Fields:
    - PortBindings (Optional[Dict[str, List[PortBinding]]]): A dictionary that maps container ports to host port bindings.
    """

    port_bindings: Optional[Dict[str, List[PortBinding]]] = Field(
        None,
        description="A dictionary that maps container ports to host port bindings.",
        example={"8000/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8000"}]},
    )


class ContainerConfig(BaseModel):
    """
    Represents the configuration for creating a container.

    Fields:
    - Image (str): The name of the image to use for the container.
    - Cmd (Optional[List[str]]): A list of command arguments to run inside the container.
    - ExposedPorts (Optional[Dict[str, {}]]): A dictionary that maps container ports to empty dictionaries for exposing ports.
    - HostConfig (Optional[HostConfig]): An instance of the HostConfig model for specifying host configurations.
    - Labels (Optional[Dict[str, str]]): A dictionary of key-value pairs to use as labels for the container.
    """

    image: str = Field(
        ...,
        description="The name of the image to use for the container.",
        example="nginx",
    )
    cmd: Optional[List[str]] = Field(
        None,
        description="A list of command arguments to run inside the container.",
        example=["/bin/bash"],
    )
    exposed_ports: Optional[Dict[str, Any]] = Field(
        None,
        description="A dictionary that maps container ports to empty dictionaries for exposing ports.",
        example={"80/tcp": {}},
    )
    host_config: Optional[HostConfig] = Field(
        None,
        description="An instance of the HostConfig model for specifying host configurations.",
    )
    labels: Optional[Dict[str, str]] = Field(
        None,
        description="A dictionary of key-value pairs to use as labels for the container.",
        example={"com.example.description": "Accounting webapp"},
    )


class DNSConfig(BaseModel):
    rrtype: str = Field(default="A")
    subdomain: str = Field(..., example="example.com")
    ip_address: str = Field(..., example="1.1.1.1")
    ttl: int = Field(default=1)
    proxied: bool = Field(default=True)


class ProxyConfig(BaseModel):

    domain: Optional[str] = Field(default="smartpro.solutions")
    subdomain: Optional[str] = Field(default=None)
    container_name: str = Field(...)
    container_port: int = Field(...)

    def __init__(self, **data) -> None:

        super().__init__(**data)

        if self.subdomain is None:

            self.subdomain = self.container_name


class HttpRequest(BaseModel):
    method: str = Field(..., example="GET")
    url: str = Field(..., example="https://api.cloudflare.com/client/v4")
    headers: Optional[Dict[str, str]] = Field(default=None)
    content_type: Optional[str] = Field(default={"Content-Type": "application/json"})
    body: Optional[Union[str, Dict[str, Any], List[Any], bytes]] = Field(default=None)

    def update_headers(self, headers: Dict[str, str]) -> None:
        if self.http_headers is None:
            self.http_headers = headers
        else:
            self.http_headers.update(headers)

    def build_url(self, url: str) -> str:
        return f"{self.url}{url}"

class WSMessage(BaseModel):
    sub: str = Field(..., example="auh0|xfaf|sdf0")
    message: str = Field(..., example="Hello World!")
    event: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    