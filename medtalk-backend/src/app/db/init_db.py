from datetime import datetime
import os
from pathlib import Path
import random
from typing import Any
from faker import Faker
import pandas as pd
from sqlmodel import SQLModel
from app.core.permission import Permission

from app.core.security import get_password_hash
from app.db.utils import no_echo

from aiapp.models import *
from app.models import *
from app import crud
from app.core.config import settings
from app.db.session import SessionLocal, engine, AsyncSession
from app.service import share_service


class Init:
    def __init__(self) -> None:
        self.superusers = list[User]()
        self.users = list[User]()
        self.chats = list[Chat]()
        self.fake = Faker("zh_CN")

    def get_datetime(self) -> datetime:
        return self.fake.date_time_between_dates(datetime(2023, 8, 21), datetime(2023, 9, 13))

    def get_datetime_pair(self) -> tuple[datetime, datetime]:
        dt1 = self.get_datetime()
        dt2 = self.get_datetime()
        return (dt1, dt2) if dt1 < dt2 else (dt2, dt1)

    async def add_batch(self, db: AsyncSession, batch: list[Any]):
        db.add_all(batch)
        await db.commit()
        # await asyncio.gather(*[db.refresh(db_obj) for db_obj in batch])
        for db_obj in batch:
            await db.refresh(db_obj)
        return batch

    async def init_perms(self, db: AsyncSession):
        perm1 = await crud.perm.create(
            db, PermCreate(name=Permission.ChatAccess.value, desc="聊天访问", route="")
        )
        perm2 = await crud.perm.create(
            db, PermCreate(name=Permission.UserMngr.value, desc="用户管理", route="")
        )
        perm3 = await crud.perm.create(
            db, PermCreate(name=Permission.ChatMngr.value, desc="聊天管理", route="")
        )
        perm4 = await crud.perm.create(
            db, PermCreate(name=Permission.OpMngr.value, desc="运营管理", route="")
        )
        perm5 = await crud.perm.create(
            db, PermCreate(name=Permission.KBMngr.value, desc="知识库管理", route="")
        )
        RoleCreate.update_forward_refs()
        role1 = await crud.role.add(db, Role(name="Normal User", label="普通用户", perms=[perm1]))
        role2 = await crud.role.add(
            db, Role(name="Super User", label="管理员", perms=[perm1, perm2, perm3, perm5])
        )
        role3 = await crud.role.add(
            db,
            Role(name="Super Super User", label="超级管理员", perms=[perm1, perm2, perm3, perm4, perm5]),
        )
        self.role_norm = role1
        self.role_super = role2
        self.role_super2 = role3

    async def init_users(self, db: AsyncSession, num: int):
        all_usernames = Path("../data/nick_name.txt").read_text("utf8").splitlines()
        usernames = random.choices(all_usernames, k=num)
        self.superusers = [
            await crud.user.create(
                db,
                obj_in=UserCreate(
                    username=settings.FIRST_SUPERUSER,
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                    is_superuser=True,
                    role_id=self.role_super2.id,
                ),
            ),
            await crud.user.create(
                db,
                obj_in=UserCreate(
                    username="admin",
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                    is_superuser=True,
                    role_id=self.role_super2.id,
                ),
            ),
            await crud.user.create(
                db,
                obj_in=UserCreate(
                    username="dev",
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                    is_superuser=True,
                    role_id=self.role_super.id,
                ),
            ),
        ]

        def make_user(i: int):
            return User(
                username=usernames[i],
                hashed_password=get_password_hash(self.fake.password()),
                email=self.fake.ascii_email() if random.random() < 0.6 else None,
                phone=self.fake.phone_number() if random.random() < 0.7 else None,
                name=self.fake.name() if random.random() < 0.5 else None,
                role=self.role_norm,
            )

        users = await self.add_batch(db, [make_user(i) for i in range(num)])
        self.users = self.superusers + users

    async def init_chats(self, db: AsyncSession, num: int):
        self.chats = [
            await crud.chat.add(
                db, Chat(user=random.choice(self.users), title=self.fake.sentence())
            )
            for _ in range(num)
        ]

    async def init_messages(self, db: AsyncSession, num: int):
        self.messages = [
            await crud.message.add(
                db,
                Message(
                    chat=random.choice(self.chats),
                    type=random.choice(list(MessageType)),
                    content=self.fake.text(),
                    remark="",
                ),
            )
            for _ in range(num)
        ]

    async def init_chat_messages(self, db: AsyncSession, num_chats: int, num_messages: int):
        from app.service import chat_service

        data = pd.read_csv("../data/data.csv")

        self.messages = list[Message]()

        self.chats = [
            Chat(user=random.choice(self.users), title="", create_time=self.get_datetime())
            for _ in range(num_chats)
        ]
        await self.add_batch(db, self.chats)

        for _ in range(num_messages):
            dt = self.get_datetime()
            chat = random.choice(self.chats)
            question = random.choice(data["title"])
            if not chat.title:
                chat.title = question
            msgs = await chat_service.qa(db, chat, question, "")
            for msg in msgs:
                msg.send_time = dt
            self.messages.extend(msgs)
            # 现在这些都已经存库里了
        await self.add_batch(db, self.chats)

    async def init_feedbacks(self, db: AsyncSession, num: int):
        all_feedbacks = Path("../data/comment.txt").read_text("utf8").splitlines()

        msg_samples = random.sample(self.messages, num)
        self.feedbacks = await self.add_batch(
            db,
            [
                Feedback(
                    user=msg.chat.user,
                    msg=msg,
                    mark_like=random.choices((True, False), (0.5, 0.5))[0],
                    mark_dislike=random.choices((True, False), (0.3, 0.7))[0],
                    content=random.choice(all_feedbacks) if random.random() < 0.2 else "",
                    update_time=self.get_datetime(),
                )
                for msg in msg_samples
            ],
        )

    async def init_recommends(self, db: AsyncSession, num: int):
        all_recs = pd.read_csv("../data/recommend.csv")

        await self.add_batch(
            db,
            [
                Recommendation(
                    title=str(all_recs.iloc[i, 0]),
                    content=str(all_recs.iloc[i, 1]),
                    creator=random.choice(self.superusers),
                    add_time=self.get_datetime(),
                )
                for i in range(num)
            ],
        )

    async def init_complaints(self, db: AsyncSession, num: int):
        all_complaints = Path("../data/report.txt").read_text("utf8").splitlines()
        # self.users = await crud.user.gets(db)
        # self.superusers = [await crud.user.get_one(db, 1), await crud.user.get_one(db, 2),await crud.user.get_one(db, 3)]
        
        def make_complaint():
            c = Complaint(
                category=random.choice(["信息不准确", "信息不完整", "响应时间长", "其他问题", "其他问题", "其他问题"]),
                content=random.choice(all_complaints),
                user=random.choice(self.users),
                create_time=self.get_datetime(),
            )
            if random.random() < 0.4:
                c.admin = random.choice(self.superusers)
                c.create_time, c.resolve_time = self.get_datetime_pair()
            return c

        await self.add_batch(db, [make_complaint() for _ in range(num)])

    async def init_shares(self, db: AsyncSession, num: int):
        for _ in range(num):
            chat = random.choice(self.chats)
            await share_service.create_share(
                db,
                SharedLinkCreate(
                    chat_id=chat.id,
                    expire_days=random.randint(1, 30),
                    max_uses=random.randint(-1, 10),
                    readonly=random.choices([True, False], [0.4, 0.6])[0],
                ),
                chat,
            )

    async def __call__(self, db: AsyncSession):
        await self.init_perms(db)
        await self.init_users(db, 50)
        # await self.init_chats(db, 200)
        # await self.init_messages(db, 1000)
        await self.init_chat_messages(db, 200, 2000)
        await self.init_feedbacks(db, 400)
        await self.init_shares(db, 50)
        await self.init_recommends(db, 18)
        await self.init_complaints(db, 100)


async def init_db():
    """Initialize the database and add a default superuser."""
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    if os.getenv("CREATE_ONLY") == "true":
        return

    print("===Init data===")

    async with SessionLocal() as db:
        user = await crud.user.get_by_username(db, username="root")
        if not user:
            ini = Init()
            with no_echo(engine):
                await ini(db)
        else:
            ini = Init()
            with no_echo(engine):
                await ini.init_complaints(db, 100)
