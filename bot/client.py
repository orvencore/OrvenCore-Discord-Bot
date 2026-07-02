import discord
from discord.ext import commands

from bot.api.client import OrvenCoreAPI
from bot.config import settings
from bot.logger import logger
from bot.services.auth_service import AuthService
from bot.services.deployment_service import DeploymentService
from bot.services.health_service import HealthService
from bot.services.project_service import ProjectService


class OrvenCoreBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

        self.api = OrvenCoreAPI()
        self.auth_service = AuthService(self.api)
        self.project_service = ProjectService(self.api)
        self.deployment_service = DeploymentService(self.api)
        self.health_service = HealthService(self.api)
        self.started_at = discord.utils.utcnow()

    async def setup_hook(self):
        extensions = [
            "bot.cogs.core",
            "bot.cogs.account",
            "bot.cogs.projects",
            "bot.cogs.deployments",
            "bot.cogs.services",
        ]

        for extension in extensions:
            await self.load_extension(extension)
            logger.info(f"Loaded extension: {extension}")

        guild = discord.Object(id=settings.DISCORD_GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

        logger.info("Slash commands synced.")

    async def on_ready(self):
        logger.info(f"OrvenCore online as {self.user}")
