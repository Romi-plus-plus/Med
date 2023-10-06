from typing import Type

from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from aiapp.models import BaseCount


class CRUDCounter:
    async def gets(self, db: AsyncSession, model: Type[BaseCount]) -> list[BaseCount]:
        stmt = select(model)
        return (await db.exec(stmt)).all()  # type: ignore

    async def get_tops(
        self, db: AsyncSession, model: Type[BaseCount], top: int = 100
    ) -> list[BaseCount]:
        stmt = select(model).order_by(desc(model.value)).limit(top)
        return (await db.exec(stmt)).all()  # type: ignore

    async def inc(self, db: AsyncSession, model: Type[BaseCount], key: str):
        obj = await db.get(model, key) or model(key=key)
        obj.value += 1
        db.add(obj)
        await db.commit()


counter = CRUDCounter()
