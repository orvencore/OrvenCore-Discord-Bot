from dataclasses import dataclass as dc

@dc(slots=True)
class User:
    id: str
    username: str
    discord_id: int
    plan: str
    linked: bool
    display_name: str | None = None
    roles: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()
