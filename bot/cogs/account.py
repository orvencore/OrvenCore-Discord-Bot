import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.embeds import EmbedBuilder


class Account(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def build_link_url(self, user: discord.User | discord.Member) -> str:
        avatar_url = user.display_avatar.url if user.display_avatar else None
        return await self.bot.api.create_discord_link_url(
            discord_id=user.id,
            discord_username=str(user),
            discord_avatar=avatar_url,
        )

    async def send_link_embed(self, interaction: discord.Interaction):
        try:
            link_url = await self.build_link_url(interaction.user)
        except Exception:
            embed = EmbedBuilder.error(
                "Link unavailable",
                "OrvenCore could not create a secure sign-in link. Try again once the API is online.",
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        embed = EmbedBuilder.info(
            "Link OrvenCore",
            f"Sign in with your OrvenCore account here:\n{link_url}",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="account", description="Show your linked OrvenCore account.")
    async def account(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        account = await self.bot.auth_service.resolve_discord_user(interaction.user.id)

        if not account.linked:
            try:
                link_url = await self.build_link_url(interaction.user)
            except Exception:
                embed = EmbedBuilder.error(
                    "Link unavailable",
                    "OrvenCore could not create a secure sign-in link. Try again once the API is online.",
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            embed = EmbedBuilder.warning(
                "Account not linked",
                f"Sign in with your OrvenCore account here:\n{link_url}",
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
        embed.add_field(
            name="Roles",
            value=", ".join(f"`{role}`" for role in account.roles) or "`None`",
            inline=False,
        )
        embed.add_field(
            name="Permissions",
            value=", ".join(f"`{permission}`" for permission in account.permissions) or "`None`",
            inline=False,
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="link", description="Link your Discord account to OrvenCore.")
    async def link(self, interaction: discord.Interaction):
        await self.send_link_embed(interaction)

    @app_commands.command(name="login", description="Open OrvenCore account linking.")
    async def login(self, interaction: discord.Interaction):
        await self.send_link_embed(interaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(Account(bot))
