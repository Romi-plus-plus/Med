from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.utils.sqlutils import time_now

if TYPE_CHECKING:
    from .user import User, UserReadPartial


class RecommendationBase(SQLModel):
    title: str
    content: str


class Recommendation(RecommendationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    creator_id: int | None = Field(default=None, foreign_key="user.id")
    remover_id: int | None = Field(default=None, foreign_key="user.id")
    add_time: datetime = Field(default_factory=time_now)
    remove_time: datetime | None = None

    creator: "User" = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="Recommendation.creator_id==User.id", lazy="joined")
    )
    remover: Optional["User"] = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="Recommendation.remover_id==User.id", lazy="joined")
    )


class RecommendationRead(RecommendationBase):
    id: int
    add_time: datetime


class RecommendationReadWithOperator(RecommendationRead):
    remove_time: datetime | None
    creator: "UserReadPartial"
    remover: Optional["UserReadPartial"]


class RecommendationCreate(RecommendationBase):
    ...


__all__ = [
    "Recommendation",
    "RecommendationRead",
    "RecommendationReadWithOperator",
    "RecommendationCreate",
]

from .user import UserReadPartial

RecommendationReadWithOperator.update_forward_refs()
