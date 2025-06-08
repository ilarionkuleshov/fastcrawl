import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastcrawl.models.http_settings import HttpSettings
from fastcrawl.models.log_settings import LogSettings


class AppSettings(BaseSettings):

    workers: int = 15
    log: LogSettings = LogSettings()
    http: HttpSettings = HttpSettings()

    model_config = SettingsConfigDict(
        env_file=dotenv.find_dotenv(),
        env_prefix="fastcrawl_",
        env_nested_delimiter="__",
        extra="ignore",
    )
