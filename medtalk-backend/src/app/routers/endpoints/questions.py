from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app import models
from app.routers import deps
from app.service import question_service

router = APIRouter()


@router.get("/stat", tags=["stat"])
async def get_question_stats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_superuser),
):
    return await question_service.get_counters(db)
