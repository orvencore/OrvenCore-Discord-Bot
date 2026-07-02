from bot.client import OrvenCoreBot
from bot.config import settings

bot = OrvenCoreBot()

bot.run(settings.DISCORD_TOKEN)
