from bot.models.deployment import Deployment
from bot.models.health import ServiceStatus
from bot.models.project import Project
from bot.models.user import User


def mock_user_for_discord_id(discord_id: int) -> User:
    return User(
        id="mock-user",
        username="karlo",
        discord_id=discord_id,
        plan="Founder",
        linked=True,
        display_name="Karlo",
        roles=("Owner",),
        permissions=("auth.me", "discord.link", "admin.users", "admin.discord"),
    )


MOCK_PROJECTS = [
    Project(
        id=1,
        name="FlashbackVHS",
        slug="flashbackvhs",
        status="online",
        role="owner",
    ),
    Project(
        id=2,
        name="OrvenCore Homepage",
        slug="orvencore-homepage",
        status="online",
        role="owner",
    ),
    Project(
        id=3,
        name="OrvenTerminal",
        slug="orventerminal",
        status="development",
        role="developer",
    ),
]


MOCK_SERVICES = [
    ServiceStatus(name="API", status="mock/offline"),
    ServiceStatus(name="Auth", status="mock"),
    ServiceStatus(name="Agent Queue", status="mock"),
]


def mock_deployment(project_slug: str, requested_by_discord_id: int) -> Deployment:
    return Deployment(
        id=1001,
        project_slug=project_slug,
        status="queued",
        requested_by_discord_id=requested_by_discord_id,
        message="Mock deployment queued. Real execution will be handled by OrvenCore API and Agent.",
    )
