from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import Perm, User, UserCreate, UserUpdate
from app.utils.sqlutils import time_now


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()"""

    async def get_by_username(self, db: AsyncSession, *, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return (await db.exec(stmt)).first()  # type: ignore

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User.from_orm(obj_in, {"hashed_password": get_password_hash(obj_in.password)})
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate | dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        db_obj.update_time = time_now()
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, username: str, password: str) -> User | None:
        user = await self.get_by_username(db, username=username)
        if not user:
            return None
        return user if verify_password(password, user.hashed_password) else None

    def is_valid(self, user: User) -> bool:
        return user.valid

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    async def get_perms(self, db: AsyncSession, user: User) -> list[Perm]:
        return await db.run_sync(lambda _: user.role.perms)

    async def count_by_register_date(self, db: AsyncSession):
        return await self.count_by_date(db, User.create_time)

    async def count_by_login_date(self, db: AsyncSession):
        return await self.count_by_date(db, User.login_time)


user = CRUDUser(User)
