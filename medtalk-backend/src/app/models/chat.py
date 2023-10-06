from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from .user import User, UserReadPartial
    from .shared_link import SharedLink
    from .message import Message, MessageReadWithFeedback


class ChatBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")
    title: str
    delete_time: datetime | None = None  # None as valid


class Chat(ChatBase, table=True):
    id: int = Field(default=None, primary_key=True)
    create_time: datetime = Field(default_factory=datetime.now)
    update_time: datetime = Field(default_factory=datetime.now)
    user: "User" = Relationship(back_populates="chats")
    messages: list["Message"] = Relationship(back_populates="chat")
    links: list["SharedLink"] = Relationship(back_populates="chat")


class ChatRead(ChatBase):
    id: int
    user_id: int
    update_time: datetime
    create_time: datetime
    user: "UserReadPartial"
    link: Optional["SharedLink"] = None


class ChatReadWithMessages(ChatRead):
    messages: list["MessageReadWithFeedback"]


class ChatCreate(SQLModel):
    user_id: int | None = None
    title: str


class ChatUpdate(SQLModel):
    title: str


__all__ = ["Chat", "ChatRead", "ChatReadWithMessages", "ChatCreate", "ChatUpdate"]

from .message import MessageReadWithFeedback
from .shared_link import SharedLink
from .user import UserReadPartial

ChatRead.update_forward_refs()
ChatReadWithMessages.update_forward_refs()
