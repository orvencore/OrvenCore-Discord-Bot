from datetime import datetime, timezone

import discord

from bot.constants import PRIMARY, SUCCESS, WARNING, ERROR, ORVEN_LOGO


class EmbedBuilder:
    @staticmethod
    def base(title: str, description: str | None = None, *, color: int = PRIMARY):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.now(timezone.utc),
        )
        embed.set_footer(text="OrvenCore")
        embed.set_thumbnail(url=ORVEN_LOGO)
        return embed

    @staticmethod
    def success(title: str, description: str | None = None):
        return EmbedBuilder.base(title, description, color=SUCCESS)

    @staticmethod
    def warning(title: str, description: str | None = None):
        return EmbedBuilder.base(title, description, color=WARNING)

    @staticmethod
    def error(title: str, description: str | None = None):
        return EmbedBuilder.base(title, description, color=ERROR)

    @staticmethod
    def info(title: str, description: str | None = None):
        return EmbedBuilder.base(title, description, color=PRIMARY)