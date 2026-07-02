from bot.client import OrvenCoreBot
from bot.config import settings
from bot.logger import logger

bot = OrvenCoreBot()

bot.run(settings.DISCORD_TOKEN)