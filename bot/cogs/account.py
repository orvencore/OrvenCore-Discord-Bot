import discord
from discord import app_commands
from discord.ext import commands

from bot.api.client import OrvenCoreAPI
from bot.utils.embeds import EmbedBuilder


class Account(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api = OrvenCoreAPI()

    @app_commands.command(name="account", description="Show your linked OrvenCore account.")
    async def account(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        account = await self.api.get_account_by_discord_id(interaction.user.id)

        if not account.get("linked"):
            embed = EmbedBuilder.warning(
                "Account not linked",
                f"Connect your Discord account here:\n{account['link_url']}",
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        embed = EmbedBuilder.info(
            "OrvenCore Account",
            "Your Discord account is linked to OrvenCore.",
        )

        embed.add_field(name="Username", value=f"`{account['username']}`", inline=True)
        embed.add_field(name="Plan", value=f"`{account['plan']}`", inline=True)
        embed.add_field(name="Discord ID", value=f"`{account['discord_id']}`", inline=False)

        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="projects", description="Show your OrvenCore projects.")
    async def projects(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        projects = await self.api.get_projects_by_discord_id(interaction.user.id)

        embed = EmbedBuilder.info(
            "Your OrvenCore Projects",
            "Projects linked to your account.",
        )

        for project in projects:
            embed.add_field(
                name=project["name"],
                value=f"Status: `{project['status']}`\nRole: `{project['role']}`",
                inline=False,
            )

        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Account(bot))