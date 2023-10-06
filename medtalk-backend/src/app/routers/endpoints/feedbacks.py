from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.routers import deps
from app.service import feedback_service

router = APIRouter()


@router.get("/stat", tags=["stat"])
async def get_feedback_stats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_superuser),
):
    return await feedback_service.get_stats(db)


@router.get("/", response_model=Page[models.FeedbackReadWithMsgUser])
async def get_feedbacks(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: models.PageParams = Depends(),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """(Admin) Get all feedbacks."""
    return await crud.feedback.get_page(db, page=q)


@router.put("/", response_model=models.FeedbackRead)
async def update_feedback(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.FeedbackUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Update feedback of the user. Create feedback if necessary."""
    return await feedback_service.update_feedback(db,data,current_user)

