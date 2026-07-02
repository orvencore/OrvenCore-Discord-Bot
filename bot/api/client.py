import aiohttp

from bot.api.mock import MOCK_PROJECTS, MOCK_SERVICES, mock_deployment, mock_user_for_discord_id
from bot.constants import API_CHECK, API_TARGET
from bot.logger import logger
from bot.models.deployment import Deployment
from bot.models.health import HealthStatus, ServiceStatus
from bot.models.project import Project
from bot.models.user import User


class OrvenCoreAPI:
    def __init__(self):
        self.base_url = API_TARGET
    
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
        return mock_user_for_discord_id(discord_id)
    
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
