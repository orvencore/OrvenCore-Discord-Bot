import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import EmbedBuilder


class Services(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="services", description="Show OrvenCore service status.")
    async def services(self, interaction: discord.Interaction):
        await interaction.response.defer()

        services = await self.bot.health_service.services()

        embed = EmbedBuilder.info(
            "OrvenCore Services",
            "Service status returned by the OrvenCore service layer.",
        )
        for service in services:
            embed.add_field(
                name=service.name,
                value=f"`{service.status}`",
                inline=True,
            )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="status", description="Show OrvenCore API status.")
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer()

        health = await self.bot.health_service.api_health()
        embed = EmbedBuilder.success(
            "OrvenCore API",
            "API health check completed.",
        )
        embed.add_field(name="Online", value=f"`{health.online}`", inline=True)
        embed.add_field(name="Status", value=f"`{health.status}`", inline=True)

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Services(bot))
