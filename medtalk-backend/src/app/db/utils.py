import asyncio
from typing import Any, Sequence, Type, TypeVar, overload
from sqlmodel import SQLModel
from .session import AsyncSession, AsyncEngine

ModelType = TypeVar("ModelType", bound=SQLModel)
ModelType2 = TypeVar("ModelType2", bound=SQLModel)


@overload
async def from_orm_async(
    db: AsyncSession, model: Type[ModelType], obj: ModelType2, update: dict[str, Any] | None = None
) -> ModelType:
    ...


@overload
async def from_orm_async(
    db: AsyncSession,
    model: Type[ModelType],
    obj: list[ModelType2],
    update: dict[str, Any] | None = None,
) -> list[ModelType]:
    ...


async def from_orm_async(
    db: AsyncSession,
    model: Type[ModelType],
    obj: ModelType2 | list[ModelType2],
    update: dict[str, Any] | None = None,
) -> ModelType | list[ModelType]:
    if isinstance(obj, list):
        return await asyncio.gather(*[from_orm_async(db, model, obj_) for obj_ in obj])
    else:
        return await db.run_sync(lambda _: model.from_orm(obj, update))


@overload
async def fetch_attrs(
    db: AsyncSession, objs: ModelType, attribute_names: list[str] | str
) -> ModelType:
    ...


@overload
async def fetch_attrs(
    db: AsyncSession, objs: list[ModelType], attribute_names: list[str] | str
) -> list[ModelType]:
    ...


async def fetch_attrs(
    db: AsyncSession, objs: ModelType | list[ModelType], attribute_names: list[str] | str
) -> ModelType | list[ModelType]:
    def impl(_):
        for attr in attribute_names if isinstance(attribute_names, list) else (attribute_names,):
            for obj in objs if isinstance(objs, list) else (objs,):
                getattr(obj, attr)

    await db.run_sync(impl)
    return objs


class no_echo:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine
        self.echo = self.engine.echo

    def __enter__(self):
        self.echo = self.engine.echo
        self.engine.echo = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.engine.echo = self.echo
