from functools import cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

from src.enums import Stage
from src.helpers import assign_config_dict


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
