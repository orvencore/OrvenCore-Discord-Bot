import discord
from discord import app_commands
from discord.ext import commands

from bot.constants import DISCORD_LINK
from bot.utils.embeds import EmbedBuilder


class Account(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def send_link_embed(self, interaction: discord.Interaction):
        embed = EmbedBuilder.info(
            "Link OrvenCore",
            f"Start the account linking flow here:\n{DISCORD_LINK}",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="account", description="Show your linked OrvenCore account.")
    async def account(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        account = await self.bot.auth_service.resolve_discord_user(interaction.user.id)

        if not account.linked:
            embed = EmbedBuilder.warning(
                "Account not linked",
                f"Connect your Discord account here:\n{DISCORD_LINK}",
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        embed = EmbedBuilder.info(
            "OrvenCore Account",
            "Your Discord account is linked to OrvenCore.",
        )

        embed.add_field(name="Username", value=f"`{account.username}`", inline=True)
        embed.add_field(name="Plan", value=f"`{account.plan}`", inline=True)
        embed.add_field(name="Discord ID", value=f"`{account.discord_id}`", inline=False)

        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="link", description="Link your Discord account to OrvenCore.")
    async def link(self, interaction: discord.Interaction):
        await self.send_link_embed(interaction)

    @app_commands.command(name="login", description="Open OrvenCore account linking.")
    async def login(self, interaction: discord.Interaction):
        await self.send_link_embed(interaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(Account(bot))
