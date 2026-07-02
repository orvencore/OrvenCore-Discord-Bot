import platform

import discord
from discord import app_commands
from discord.ext import commands

from bot.constants import AUTH, DEV_DOCS, HOMEPAGE
from bot.utils.embeds import EmbedBuilder


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Show OrvenCore bot stats.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer()

        api_health = await self.bot.health_service.api_health()

        latency_ms = round(self.bot.latency * 1000)
        uptime_seconds = int((discord.utils.utcnow() - self.bot.started_at).total_seconds())

        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        embed = EmbedBuilder.success(
            "OrvenCore Status",
            "Bot is online and responding.",
        )

        embed.add_field(name="Gateway", value=f"`{latency_ms} ms`", inline=True)
        embed.add_field(name="Uptime", value=f"`{hours}h {minutes}m {seconds}s`", inline=True)
        embed.add_field(name="API", value="`online`" if api_health.online else "`mock/offline`", inline=True)
        embed.add_field(name="Python", value=f"`{platform.python_version()}`", inline=True)
        embed.add_field(name="discord.py", value=f"`{discord.__version__}`", inline=True)
        embed.add_field(name="Servers", value=f"`{len(self.bot.guilds)}`", inline=True)

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="about", description="Show OrvenCore links.")
    async def about(self, interaction: discord.Interaction):
        embed = EmbedBuilder.info(
            "About OrvenCore",
            "OrvenCore Discord is the control layer for the future OrvenCore platform.",
        )
        embed.add_field(name="Homepage", value=HOMEPAGE, inline=False)
        embed.add_field(name="Auth", value=AUTH, inline=False)
        embed.add_field(name="Docs", value=DEV_DOCS, inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="version", description="Show bot runtime versions.")
    async def version(self, interaction: discord.Interaction):
        embed = EmbedBuilder.info("OrvenCore Version", "Current bot runtime information.")
        embed.add_field(name="Python", value=f"`{platform.python_version()}`", inline=True)
        embed.add_field(name="discord.py", value=f"`{discord.__version__}`", inline=True)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))
