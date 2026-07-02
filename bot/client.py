import discord
from discord.ext import commands

from bot.config import settings
from bot.logger import logger


class OrvenCoreBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self):
        extensions = [
            "bot.cogs.core",
            "bot.cogs.account",
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