import aiohttp

from bot.constants import API_TARGET, API_CHECK, DISCORD_LINK
from bot.api.mock import MOCK_USER, MOCK_PROJECTS
from bot.logger import logger


class OrvenCoreAPI:
    def __init__(self):
        self.base_url = API_TARGET
    
    async def health(self) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_CHECK, timeout=5) as response:
                    return {
                        "online": response.status == 200,
                        "status": response.status,
                    }
        except Exception as exc:
            logger.warning(f'API health check failed: {exc}')
            return {
                "online": False,
                "status": "mock"
            }
        

    async def get_account_by_discord_id(self, discord_id: int) -> dict:
        return MOCK_USER | {
            "discord_id": discord_id,
            "link_url": DISCORD_LINK
        }
    
    async def get_projects_by_discord_id(self, discord_id: int) -> dict:
        return MOCK_PROJECTS