from dataclasses import dataclass as dc

@dc(slots=True)
class User:
    id: int
    username: str
    discord_id: int
    plan: str
    linked: bool