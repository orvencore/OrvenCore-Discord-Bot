from bot.api.client import OrvenCoreAPI
from bot.models.deployment import Deployment


class DeploymentService:
    def __init__(self, api: OrvenCoreAPI):
        self.api = api

    async def deploy(self, discord_id: int, project_slug: str) -> Deployment:
        return await self.api.request_deploy(discord_id, project_slug)
