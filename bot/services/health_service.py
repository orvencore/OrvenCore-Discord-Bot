from bot.api.client import OrvenCoreAPI
from bot.models.health import HealthStatus, ServiceStatus


class HealthService:
    def __init__(self, api: OrvenCoreAPI):
        self.api = api

    async def api_health(self) -> HealthStatus:
        return await self.api.health()

    async def services(self) -> list[ServiceStatus]:
        return await self.api.services()
