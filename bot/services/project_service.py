from bot.api.client import OrvenCoreAPI
from bot.models.project import Project


class ProjectService:
    def __init__(self, api: OrvenCoreAPI):
        self.api = api

    async def list_for_discord_user(self, discord_id: int) -> list[Project]:
        return await self.api.get_projects_by_discord_id(discord_id)

    async def get_for_discord_user(self, discord_id: int, slug: str) -> Project | None:
        return await self.api.get_project_by_slug(discord_id, slug)
