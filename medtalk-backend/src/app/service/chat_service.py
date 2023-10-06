from datetime import datetime
import random
from typing import Sequence

import aiohttp
from faker import Faker
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.core.config import settings
from app.db.utils import from_orm_async
from app.models.chat import Chat, ChatRead, ChatReadWithMessages
from app.models.feedback import Feedback, FeedbackRead
from app.models.message import (
    Message,
    MessageCreate,
    MessageReadWithFeedback,
    MessageType,
    NoteCreate,
)
from app.models.user import User
from app.service import share_service
from app.utils.sqlutils import is_today, is_yesterday, time_now
from app.utils.statutils import counter_helper


async def to_read(db: AsyncSession, chat: Chat) -> ChatRead:
    link = await share_service.get_chat_link(db, chat)
    return await db.run_sync(lambda _: ChatRead.from_orm(chat, dict(link=link)))


async def to_reads(db: AsyncSession, chats: Sequence[Chat]) -> list[ChatRead]:
    return [await to_read(db, c) for c in chats]


def to_reads_wrapped(db: AsyncSession):
    async def wrapped(chats: Sequence[Chat]):
        return await to_reads(db, chats)

    return wrapped


async def access_chat(
    db: AsyncSession,
    chat_id: int,
    user: User,
    *,
    allow_admin: bool = True,
    update_time: bool = False
) -> Chat:
    """Try accessing a chat.

    Args:
        db (AsyncSession): _description_
        chat_id (int): _description_
        user (User): The current operating user
        allow_admin (bool, optional): Whether admin can unconditionally access. Defaults to True.
        update_time (bool, optional): Whether to update the chat time. Defaults to False.

    Raises:
        HTTPException

    Returns:
        Chat: The accessed chat
    """
    chat = await crud.chat.get(db, chat_id)
    if not crud.chat.is_valid(chat):  # Non-existent or deleted
        raise HTTPException(404, "The chat is not found!")
    if not (chat.user_id == user.id or allow_admin and crud.user.is_superuser(user)):
        raise HTTPException(403, "You can't access this chat!")
    if update_time:
        await update_chat_time(db, chat)
    return chat


async def get_shared_chats(db: AsyncSession, user: User):
    return await db.run_sync(
        lambda _: [l.link.chat for l in user.links if crud.chat.is_valid(l.link.chat)]
    )


async def update_chat_time(db: AsyncSession, chat: Chat) -> Chat:
    """Update the `update_time` of a chat to now and save it."""
    chat.update_time = time_now()
    return await crud.chat.add(db, chat)


async def delete_chat(db: AsyncSession, chat: Chat) -> Chat:
    """Delete a chat from DB and set its `delete_time` to now."""
    chat.delete_time = datetime.now()
    return await crud.chat.add(db, chat)


async def qa(db: AsyncSession, chat: Chat, question: str, hint: str | None):
    """Perferm Q&A. It saves the question and answer messages to DB."""
    if settings.ENABLE_KGQA:
        async with aiohttp.ClientSession() as session:
            async with session.post(settings.KGQA_API, data=question) as response:
                obj = await response.json()
                que_text = obj["marked_input"]
                ans_txts = (
                    [a["marked_text"] for a in obj["answers"]]
                    if obj["answers"]
                    else [obj["fallback_answer"]]
                )
    else:
        fake = Faker("zh_CN")
        que_text = question
        ans_txts: list[str] = [fake.text() for _ in range(random.randint(1, 3))]

    question_msg = await crud.message.create(
        db,
        MessageCreate(
            chat_id=chat.id, type=MessageType.Question, content=que_text, remark=hint or ""
        ),
    )
    answer_msgs = [
        await crud.message.create(
            db,
            MessageCreate(chat_id=chat.id, type=MessageType.Answer, content=ans_txt, remark=""),
        )
        for ans_txt in ans_txts
    ]
    return [question_msg, *answer_msgs]


async def get_chat_with_feedbacks(db: AsyncSession, chat: Chat, user: User):
    """Get a chat with feedbacks loaded."""

    def feedback_orm(fb: Feedback | None):
        return FeedbackRead.from_orm(fb) if fb else None

    return await from_orm_async(
        db,
        ChatReadWithMessages,
        chat,
        dict(
            messages=[
                MessageReadWithFeedback.from_orm(
                    msg,
                    dict(own_feedback=feedback_orm(await crud.feedback.get(db, (msg.id, user.id)))),
                )
                for msg in await db.run_sync(lambda _: chat.messages)
            ],
            link=await share_service.get_chat_link(db, chat),
        ),
    )


async def update_title(db: AsyncSession, chat: Chat, title: str):
    """Update the title of the chat and update its `update_time` to now."""
    chat.title = title
    chat.update_time = time_now()
    return await crud.chat.add(db, chat)


async def create_note(db: AsyncSession, chat: Chat, note_in: NoteCreate):
    """Create a note in the chat."""
    return await crud.message.create(
        db,
        MessageCreate(
            chat_id=chat.id, type=MessageType.Note, content=note_in.content, remark=note_in.remark
        ),
    )


async def get_temporal_stats(db: AsyncSession):
    return await counter_helper(
        db,
        (crud.chat.count_by_date, "total_chats"),
        (crud.message.count_by_date, "total_messages"),
        (crud.message.count_q_by_date, "questions"),
        (crud.message.count_a_by_date, "answers"),
        (crud.message.count_n_by_date, "notes"),
    )


async def get_stats(db: AsyncSession):
    return {
        "total_chats": await crud.chat.count(db),
        "total_messages": await crud.message.count(db),
        "total_chats_today": await crud.chat.count_if(db, is_today(Chat.create_time)),
        "total_messages_today": await crud.message.count_if(db, is_today(Message.send_time)),
        "total_chats_yesterday": await crud.chat.count_if(db, is_yesterday(Chat.create_time)),
        "total_messages_yesterday": await crud.message.count_if(
            db, is_yesterday(Message.send_time)
        ),
        "by_date": await get_temporal_stats(db),
    }
