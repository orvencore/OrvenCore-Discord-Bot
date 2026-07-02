from dataclasses import dataclass as dc


@dc(slots=True)
class Deployment:
    id: int
    project_slug: str
    status: str
    requested_by_discord_id: int
    message: str
