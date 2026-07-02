import platform
import time

import discord
from discord import app_commands
from discord.ext import commands

from bot.api.client import OrvenCoreAPI
from bot.utils.embeds import EmbedBuilder


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.started_at = time.time()
        self.api = OrvenCoreAPI()

    @app_commands.command(name="ping", description="Show OrvenCore bot stats.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer()

        api_health = await self.api.health()

        latency_ms = round(self.bot.latency * 1000)
        uptime_seconds = int(time.time() - self.started_at)

        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = EmbedBuilder.success(
            "OrvenCore Status",
            "Bot is online and responding.",
        )

        embed.add_field(name="Gateway", value=f"`{latency_ms} ms`", inline=True)
        embed.add_field(name="Uptime", value=f"`{hours}h {minutes}m {seconds}s`", inline=True)
        embed.add_field(name="API", value="`online`" if api_health["online"] else "`mock/offline`", inline=True)
        embed.add_field(name="Python", value=f"`{platform.python_version()}`", inline=True)
        embed.add_field(name="discord.py", value=f"`{discord.__version__}`", inline=True)
        embed.add_field(name="Servers", value=f"`{len(self.bot.guilds)}`", inline=True)

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))