from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

engine = AsyncEngine(
    create_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True, echo=True)
)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)