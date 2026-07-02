from dataclasses import dataclass as dc

@dc(slots=True)
class Project:
    id: int
    name: str
    slug: str
    status: str
    role: str
    