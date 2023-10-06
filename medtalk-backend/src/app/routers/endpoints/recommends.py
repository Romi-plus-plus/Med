from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.routers import deps
from app.service import recommend_service

router = APIRouter()


@router.get("/", response_model=list[models.RecommendationRead])
async def get_recommends(
    *,
    db: AsyncSession = Depends(deps.get_db),
):
    """Get all active recommendations."""
    return await recommend_service.get_active_recommends(db)


@router.get("/all", response_model=Page[models.RecommendationReadWithOperator])
async def get_all_recommends(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: models.PageParams = Depends(),
    active: bool | None = None,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """Get all recommendations."""
    return await recommend_service.get_all_recommends(db, page=q, active=active)


@router.post("/", response_model=models.RecommendationReadWithOperator)
async def add_recommend(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.RecommendationCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """Add a recommendation."""
    return await recommend_service.add_recommend(db, obj_in=data, user=current_user)


@router.delete("/{rec_id}", response_model=models.RecommendationReadWithOperator | None)
async def remove_recommend(
    *,
    db: AsyncSession = Depends(deps.get_db),
    rec_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """Remove a recommendation."""
    return await recommend_service.remove_recommend(db, rec_id=rec_id, user=current_user)


@router.put("/{rec_id}", response_model=models.RecommendationReadWithOperator | None)
async def recover_recommend(
    *,
    db: AsyncSession = Depends(deps.get_db),
    rec_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """Recover a recommendation removed before."""
    return await recommend_service.recover_recommend(db, rec_id=rec_id, user=current_user)
