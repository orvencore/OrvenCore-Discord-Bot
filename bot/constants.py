# COLORS
PRIMARY = 0x2F3136
SUCCESS = 0x43B581
WARNING = 0xFAA61A
ERROR = 0xED4245

# ASSETS
ORVEN_LOGO = "https://assets.orvencore.com/static/img/logos/logo.png"

from bot.config import settings

# API / DEPENDENCIES
API_TARGET = settings.ORVENCORE_API_URL.rstrip("/")
AUTH_TARGET = settings.ORVENCORE_AUTH_URL.rstrip("/")
API_CHECK = f"{API_TARGET}/api/health"

# WEBSITE LINKS
BASE_DOMAIN = "orvencore.com"
HTTPS = "https://"
HTTP = "http://"

HOMEPAGE = f"{HTTPS}www.{BASE_DOMAIN}"
AUTH = AUTH_TARGET

BASE_LINKS = f"{HTTPS}links.{BASE_DOMAIN}"
DISCORD_LINK = AUTH_TARGET
SOCIAL_IG = f"{BASE_LINKS}/instagram"
SOCIAL_X = f"{BASE_LINKS}/twitter-x"
SOCIAL_YT = f"{BASE_LINKS}/youtube"

DEV_BLOG = f"{HTTPS}blog.{BASE_DOMAIN}"
DEV_DOCS = f"{HTTPS}docs.{BASE_DOMAIN}"
