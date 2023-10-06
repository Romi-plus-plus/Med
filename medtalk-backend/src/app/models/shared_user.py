from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .shared_link import SharedLink
    from .user import User


class SharedUser(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    link_id: str | None = Field(default=None, foreign_key="sharedlink.id", primary_key=True)
    accquire_time: datetime = Field(default_factory=datetime.now)
    access_time: datetime = Field(default_factory=datetime.now)
    valid: bool = True

    user: "User" = Relationship(back_populates="links")
    link: "SharedLink" = Relationship(back_populates="user_links")


__all__ = ["SharedUser"]
