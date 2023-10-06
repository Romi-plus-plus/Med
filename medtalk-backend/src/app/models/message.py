from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from .chat import Chat
    from .feedback import FeedbackRead


class MessageType(Enum):
    Question = 0
    Answer = 1
    Note = 2


class MessageBase(SQLModel):
    chat_id: int | None = Field(default=None, foreign_key="chat.id")
    type: MessageType
    content: str
    remark: str


class Message(MessageBase, table=True):
    id: int = Field(default=None, primary_key=True)
    send_time: datetime = Field(default_factory=datetime.now)

    chat: "Chat" = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    id: int
    send_time: datetime
    chat_id: int


class MessageReadWithFeedback(MessageRead):
    own_feedback: Optional["FeedbackRead"]


class MessageCreate(MessageBase):
    chat_id: int


class NoteCreate(SQLModel):
    content: str
    remark: str


__all__ = [
    "MessageType",
    "Message",
    "MessageRead",
    "MessageReadWithFeedback",
    "MessageCreate",
    "NoteCreate",
]

from .feedback import FeedbackRead


MessageReadWithFeedback.update_forward_refs()
