from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Sequence, Type, TypedDict, TypeVar
from fastapi import HTTPException

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination.types import AsyncItemsTransformer
from pydantic import BaseModel
from sqlalchemy import DATE
from sqlmodel import SQLModel, cast, desc, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

if TYPE_CHECKING:
    from app.models import PageParams

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class DateCount(TypedDict):
    date: str
    count: int


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> ModelType | None:
        return await db.get(self.model, id)
    
    async def get_one(self, db: AsyncSession, id: Any) -> ModelType:
        ret = await self.get(db, id)
        if not ret:
            raise HTTPException(404)
        return ret

    async def gets(self, db: AsyncSession, *, offset: int = 0, limit: int = 100) -> list[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)
        return (await db.exec(stmt)).all()  # type: ignore

    async def get_page(
        self,
        db: AsyncSession,
        *,
        page: PageParams,
        transformer: AsyncItemsTransformer | None = None,
    ) -> Page:
        stmt = select(self.model)
        if page.sort_by:
            key = getattr(self.model, page.sort_by)
            key = desc(key) if page.desc else key
            stmt = stmt.order_by(key)
        return await paginate(db, stmt, transformer=transformer)

    async def get_page_if(
        self,
        db: AsyncSession,
        *where_clause,
        page: PageParams,
        transformer: AsyncItemsTransformer | None = None,
    ) -> Page:
        stmt = select(self.model).where(*where_clause)
        if page.sort_by:
            key = getattr(self.model, page.sort_by)
            key = desc(key) if page.desc else key
            stmt = stmt.order_by(key)
        return await paginate(db, stmt, transformer=transformer)

    async def add(self, db: AsyncSession, db_obj: ModelType):
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def adds(self, db: AsyncSession, db_objs: Sequence[ModelType]):
        db.add_all(db_objs)
        await db.commit()
        for db_obj in db_objs:
            await db.refresh(db_obj)
        return db_objs

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        return await self.add(db, db_obj)

    async def update(
        self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return await self.add(db, db_obj)

    async def delete(self, db: AsyncSession, db_obj: ModelType):
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    async def remove(self, db: AsyncSession, *, id: Any) -> ModelType:
        obj = await db.get(self.model, id)
        assert obj
        return await self.delete(db, obj)

    async def count(self, db: AsyncSession) -> int:
        stmt = select([func.count()]).select_from(self.model)
        return (await db.exec(stmt)).one()  # type: ignore

    async def count_if(self, db: AsyncSession, *where_clause) -> int:
        stmt = select([func.count()]).select_from(self.model).where(*where_clause)
        return (await db.exec(stmt)).one()  # type: ignore

    async def count_by_date(self, db: AsyncSession, field: Any) -> list[DateCount]:
        stmt = (
            select(
                [
                    func.to_char(field, "YYYY-MM-DD").label("date"),
                    func.count().label("count"),
                ]
            )
            .select_from(self.model)
            .group_by("date")
            .select()
        )
        return (await db.exec(stmt)).all()  # type: ignore

    async def count_if_by_date(
        self, db: AsyncSession, field: Any, *where_clause
    ) -> list[DateCount]:
        stmt = (
            select(
                [
                    func.to_char(field, "YYYY-MM-DD").label("date"),
                    func.count().label("count"),
                ]
            )
            .select_from(self.model)
            .where(*where_clause)
            .group_by("date")
            .select()
        )
        return (await db.exec(stmt)).all()  # type: ignore
