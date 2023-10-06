from typing import Any, TypeGuard
from sqlmodel import SQLModel, select

from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.chat import Chat, ChatCreate, ChatRead
from app.models.user import User


class CRUDChat(CRUDBase[Chat, ChatCreate, SQLModel]):
    async def get_by_user(self, db: AsyncSession, *, user: User):
        chats = await db.run_sync(lambda _: user.chats)
        return list(filter(self.is_valid, chats))

    def is_valid(self, chat: Chat | None) -> TypeGuard[Chat]:
        return chat is not None and not chat.delete_time

    async def count_by_date(self, db):
        return await super().count_by_date(db, Chat.create_time)


chat = CRUDChat(Chat)
