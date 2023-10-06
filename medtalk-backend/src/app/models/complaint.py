from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.utils.sqlutils import time_now

if TYPE_CHECKING:
    from .user import User


class ComplaintBase(SQLModel):
    category: str
    content: str
    reply: str | None = None
    create_time: datetime = Field(default_factory=time_now)
    resolve_time: datetime | None = None  # None as unresolved


class Complaint(ComplaintBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    admin_id: int | None = Field(default=None, foreign_key="user.id")

    user: "User" = Relationship(
        back_populates="posted_complaints",
        sa_relationship_kwargs=dict(primaryjoin="Complaint.user_id==User.id", lazy="joined"),
    )
    admin: "User" = Relationship(
        back_populates="resolved_complaints",
        sa_relationship_kwargs=dict(primaryjoin="Complaint.admin_id==User.id", lazy="joined"),
    )


class ComplaintRead(ComplaintBase):
    id: int
    user_id: int
    admin_id: int | None


class ComplaintReadDetailed(ComplaintRead):
    user: "UserReadPartial"
    admin: Optional["UserReadPartial"]


class ComplaintCreate(SQLModel):
    category: str
    content: str


class ComplaintResolve(SQLModel):
    reply: str


__all__ = [
    "Complaint",
    "ComplaintRead",
    "ComplaintReadDetailed",
    "ComplaintCreate",
    "ComplaintResolve",
]


from .user import UserReadPartial

ComplaintReadDetailed.update_forward_refs()
