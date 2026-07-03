import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    DISCORD_GUILD_ID: int = int(os.getenv("DISCORD_GUILD_ID", "0"))
    APP_ENV: str = os.getenv("APP_ENV", os.getenv("ORVENCORE_APP_ENV", "development"))
    ORVENCORE_API_URL: str = os.getenv("ORVENCORE_API_URL", "http://127.0.0.1:8000")
    ORVENCORE_AUTH_URL: str = os.getenv("ORVENCORE_AUTH_URL", "http://127.0.0.1:8000")
    ORVENCORE_SERVICE_API_KEY: str = os.getenv("ORVENCORE_SERVICE_API_KEY", "")
    ORVENCORE_USE_MOCK_API: bool = env_bool("ORVENCORE_USE_MOCK_API", False)

    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() in {"production", "prod"}

settings = Settings()

if settings.is_production and not settings.ORVENCORE_SERVICE_API_KEY:
    raise RuntimeError("ORVENCORE_SERVICE_API_KEY is required in production.")
