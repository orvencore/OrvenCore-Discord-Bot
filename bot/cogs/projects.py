import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import EmbedBuilder


class Projects(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="projects", description="Show your OrvenCore projects.")
    async def projects(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        projects = await self.bot.project_service.list_for_discord_user(interaction.user.id)

        if not projects:
            embed = EmbedBuilder.warning(
                "No Projects",
                "No OrvenCore projects are currently linked to your account.",
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        embed = EmbedBuilder.info(
            "Your OrvenCore Projects",
            "Projects linked to your account.",
        )

        for project in projects:
            embed.add_field(
                name=project.name,
                value=f"Slug: `{project.slug}`\nStatus: `{project.status}`\nRole: `{project.role}`",
                inline=False,
            )

        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="project", description="Show one OrvenCore project.")
    @app_commands.describe(slug="Project slug, for example flashbackvhs.")
    async def project(self, interaction: discord.Interaction, slug: str):
        await interaction.response.defer(ephemeral=True)

        project = await self.bot.project_service.get_for_discord_user(interaction.user.id, slug)
        if project is None:
            embed = EmbedBuilder.error(
                "Project Not Found",
                "OrvenCore API did not return a project for this Discord account and slug.",
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        embed = EmbedBuilder.info(project.name, "Project access returned by OrvenCore.")
        embed.add_field(name="Slug", value=f"`{project.slug}`", inline=True)
        embed.add_field(name="Status", value=f"`{project.status}`", inline=True)
        embed.add_field(name="Role", value=f"`{project.role}`", inline=True)

        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Projects(bot))
