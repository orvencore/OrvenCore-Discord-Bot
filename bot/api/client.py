import aiohttp

from bot.api.mock import MOCK_PROJECTS, MOCK_SERVICES, mock_deployment, mock_user_for_discord_id
from bot.config import settings
from bot.constants import API_CHECK, API_TARGET
from bot.logger import logger
from bot.models.deployment import Deployment
from bot.models.health import HealthStatus, ServiceStatus
from bot.models.project import Project
from bot.models.user import User


class OrvenCoreAPI:
    def __init__(self):
        self.base_url = API_TARGET

    @property
    def service_headers(self) -> dict[str, str]:
        if not settings.ORVENCORE_SERVICE_API_KEY:
            return {}
        return {"X-OrvenCore-Service-Key": settings.ORVENCORE_SERVICE_API_KEY}

    @staticmethod
    def unlinked_user(discord_id: int) -> User:
        return User(
            id="",
            username="",
            discord_id=discord_id,
            plan="Free",
            linked=False,
        )
    
    async def health(self) -> HealthStatus:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_CHECK, timeout=5) as response:
                    return HealthStatus(
                        online=response.status == 200,
                        status=str(response.status),
                    )
        except Exception as exc:
            logger.warning(f'API health check failed: {exc}')
            return HealthStatus(
                online=False,
                status="mock",
            )
        

    async def get_account_by_discord_id(self, discord_id: int) -> User:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/discord/users/{discord_id}",
                    headers=self.service_headers,
                    timeout=5,
                ) as response:
                    if response.status == 404:
                        return self.unlinked_user(discord_id)
                    if response.status != 200:
                        raise RuntimeError(f"Unexpected API status: {response.status}")

                    data = await response.json()
                    roles = tuple(data.get("roles", []))
                    permissions = tuple(data.get("permissions", []))
                    return User(
                        id=data["user_id"],
                        username=data["username"],
                        discord_id=int(data["discord"]["discord_user_id"]),
                        plan="Premium" if "Premium" in roles else "User",
                        linked=True,
                        display_name=data.get("display_name"),
                        roles=roles,
                        permissions=permissions,
                    )
        except Exception as exc:
            if settings.ORVENCORE_USE_MOCK_API:
                logger.warning(f"API Discord lookup failed, using mock user: {exc}")
                return mock_user_for_discord_id(discord_id)
            logger.warning(f"API Discord lookup failed: {exc}")
            return self.unlinked_user(discord_id)

    async def create_discord_link_url(
        self,
        *,
        discord_id: int,
        discord_username: str,
        discord_avatar: str | None = None,
    ) -> str:
        params = {
            "discord_id": str(discord_id),
            "discord_username": discord_username,
        }
        if discord_avatar:
            params["discord_avatar"] = discord_avatar
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/auth/discord/start",
                    params=params,
                    timeout=5,
                ) as response:
                    if response.status != 200:
                        raise RuntimeError(f"Unexpected API status: {response.status}")
                    data = await response.json()
                    return data["link_url"]
        except Exception as exc:
            logger.warning(f"Discord link start failed: {exc}")
            raise
    
    async def get_projects_by_discord_id(self, discord_id: int) -> list[Project]:
        return MOCK_PROJECTS

    async def get_project_by_slug(self, discord_id: int, slug: str) -> Project | None:
        normalized_slug = slug.lower()
        for project in MOCK_PROJECTS:
            if project.slug == normalized_slug:
                return project
        return None

    async def request_deploy(self, discord_id: int, project_slug: str) -> Deployment:
        return mock_deployment(project_slug, discord_id)

    async def services(self) -> list[ServiceStatus]:
        return MOCK_SERVICES
