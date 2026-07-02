import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    DISCORD_GUILD_ID: int = int(os.getenv("DISCORD_GUILD_ID", "0"))

settings = Settings()