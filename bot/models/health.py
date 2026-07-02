from dataclasses import dataclass as dc


@dc(slots=True)
class HealthStatus:
    online: bool
    status: str


@dc(slots=True)
class ServiceStatus:
    name: str
    status: str
