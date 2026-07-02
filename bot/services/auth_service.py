from bot.api.client import OrvenCoreAPI
from bot.models.user import User


class AuthService:
    def __init__(self, api: OrvenCoreAPI):
        self.api = api

    async def resolve_discord_user(self, discord_id: int) -> User:
        return await self.api.get_account_by_discord_id(discord_id)
