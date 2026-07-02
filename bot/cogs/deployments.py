import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import EmbedBuilder


class Deployments(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="deploy", description="Request a deployment through OrvenCore.")
    @app_commands.describe(project_slug="Project slug, for example flashbackvhs.")
    async def deploy(self, interaction: discord.Interaction, project_slug: str):
        await interaction.response.defer(ephemeral=True)

        deployment = await self.bot.deployment_service.deploy(interaction.user.id, project_slug)

        embed = EmbedBuilder.success(
            "Deployment Requested",
            deployment.message,
        )
        embed.add_field(name="Deployment ID", value=f"`{deployment.id}`", inline=True)
        embed.add_field(name="Project", value=f"`{deployment.project_slug}`", inline=True)
        embed.add_field(name="Status", value=f"`{deployment.status}`", inline=True)

        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Deployments(bot))
