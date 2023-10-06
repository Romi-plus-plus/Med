from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid1

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .chat import Chat
    from .shared_user import SharedUser


class SharedLinkBase(SQLModel):
    create_time: datetime
    expire_time: datetime
    max_uses: int  # -1 representing infinite
    use_times: int = 0
    readonly: bool
    valid: bool = True


class SharedLink(SharedLinkBase, table=True):
    id: str | None = Field(default_factory=lambda: str(uuid1()).replace("-", ""), primary_key=True)
    chat_id: int | None = Field(default=None, foreign_key="chat.id")
    create_time: datetime | None = Field(default_factory=datetime.now)

    chat: "Chat" = Relationship(back_populates="links")

    user_links: list["SharedUser"] = Relationship(back_populates="link")


class SharedLinkRead(SharedLinkBase):
    id: str
    chat_id: int
    create_time: datetime


class SharedLinkCreate(SQLModel):
    chat_id: int
    expire_days: int = Field(ge=1)
    max_uses: int
    readonly: bool


class SharedLinkUpdate(SQLModel):
    max_uses: int
    readonly: bool
    valid: bool


__all__ = ["SharedLink", "SharedLinkCreate", "SharedLinkRead", "SharedLinkUpdate"]
