from sqlmodel import SQLModel, select, func, distinct

from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import Message, MessageCreate
from app.models.chat import Chat
from app.models.message import MessageType
from app.utils.sqlutils import is_today


class CRUDMessage(CRUDBase[Message, MessageCreate, SQLModel]):
    async def count_by_date(self, db: AsyncSession):
        return await super().count_by_date(db, Message.send_time)

    async def count_q_by_date(self, db: AsyncSession):
        return await super().count_if_by_date(
            db, Message.send_time, Message.type == MessageType.Question
        )

    async def count_a_by_date(self, db: AsyncSession):
        return await super().count_if_by_date(
            db, Message.send_time, Message.type == MessageType.Answer
        )

    async def count_n_by_date(self, db: AsyncSession):
        return await super().count_if_by_date(
            db, Message.send_time, Message.type == MessageType.Note
        )

    async def count_distinct_sender_today(self, db: AsyncSession):
        stmt = select(func.count(distinct(Chat.user_id))).where(is_today(Chat.update_time))  # type: ignore
        return (await db.exec(stmt)).one()


message = CRUDMessage(Message)
