from functools import cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.enums import Stage


def assign_config_dict(prefix: str = "") -> SettingsConfigDict:
    return SettingsConfigDict(
        env_prefix=prefix,
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


class NgrokConfig(BaseSettings):
    URL: SecretStr
    USER: SecretStr
    PASS: SecretStr

    model_config = assign_config_dict(prefix="NGROK_")


class Settings(BaseSettings):
    ngrok: NgrokConfig = Field(default_factory=NgrokConfig)
    stage = Stage

    model_config = assign_config_dict()


@cache
def get_settings() -> Settings:
    return Settings()
