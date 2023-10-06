from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .message import Message
    from .user import User


class FeedbackBase(SQLModel):
    msg_id: int
    mark_like: bool
    mark_dislike: bool
    content: str


class Feedback(SQLModel, table=True):
    msg_id: int | None = Field(default=None, foreign_key="message.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    mark_like: bool = False
    mark_dislike: bool = False
    content: str = ""
    update_time: datetime = Field(default_factory=datetime.now)

    msg: "Message" = Relationship()
    user: "User" = Relationship()
    # msg: "Message" = Relationship(back_populates="user_links")
    # user: "User" = Relationship(back_populates="msg_links")


class FeedbackRead(FeedbackBase):
    user_id: int
    update_time: datetime


class FeedbackReadWithMsgUser(FeedbackRead):
    msg: "MessageRead"
    user: "UserReadPartial"


class FeedbackUpdate(SQLModel):
    msg_id: int
    mark_like: bool | None = None
    mark_dislike: bool | None = None
    content: str | None = None


__all__ = ["Feedback", "FeedbackRead", "FeedbackReadWithMsgUser", "FeedbackUpdate"]


from .message import MessageRead
from .user import UserReadPartial

FeedbackReadWithMsgUser.update_forward_refs()
