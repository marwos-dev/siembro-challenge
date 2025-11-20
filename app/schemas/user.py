from datetime import datetime

from pydantic import BaseModel


class UserMetadata(BaseModel):
    first_seen_at: datetime | None = None
    last_login_at: datetime | None = None
    notes_count: int


class MeOut(BaseModel):
    sub: str
    email: str | None = None
    name: str | None = None
    metadata: dict
