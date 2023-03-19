from typing import List
from pydantic import BaseConfig, BaseSettings, Field


class Settings(BaseSettings):
    """Settings for the app"""

    class Config(BaseConfig):
        env_file = ".env"
        env_file_encoding = "utf-8"

    FAUNA_SECRET: str = Field(..., env="FAUNA_SECRET")
    AUTH0_DOMAIN: str = Field(..., env="AUTH0_DOMAIN")
    DOCKER_HOST: str = Field(..., env="DOCKER_HOST")
    DOCKER_PORT: str = Field(..., env="DOCKER_PORT")
    DOCKER_PROTOCOL: str = Field(..., env="DOCKER_PROTOCOL")
    DOCKER_IP: str = Field(..., env="DOCKER_IP")
    DOCKER_URL: str = Field(..., env="DOCKER_URL")
    GITHUB_TOKEN: str = Field(..., env="GITHUB_TOKEN")
    GITHUB_USERNAME: str = Field(..., env="GITHUB_USER")
    GOOGLE_APPLICATION_CREDENTIALS: str = Field(
        ..., env="GOOGLE_APPLICATION_CREDENTIALS"
    )
    GOOGLE_SCOPES: List[str] = Field(..., env="GOOGLE_SCOPES")
    BUCKET_NAME: str = Field(..., env="BUCKET_NAME")
    CF_API_KEY: str = Field(..., env="CF_API_KEY")
    CF_EMAIL: str = Field(..., env="CF_EMAIL")
    CF_ZONE_ID: str = Field(..., env="CF_ZONE_ID")
    CF_ACCOUNT_ID: str = Field(..., env="CF_ACCOUNT_ID")


env = Settings()
