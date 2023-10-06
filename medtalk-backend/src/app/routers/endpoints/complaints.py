from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.routers import deps
from app.service import complaint_service

router = APIRouter()


@router.get("/stat", tags=["stat"])
async def get_complaint_stats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """(Admin) Get complaint stats."""
    return await complaint_service.get_stats(db)


@router.get("/", response_model=Page[models.ComplaintReadDetailed])
async def get_complaints(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: models.PageParams = Depends(),
    resolved: bool | None = None,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """(Admin) Get all complaints."""
    return await complaint_service.get_all_complaints(db, q, resolved)


@router.post("/", response_model=models.ComplaintRead)
async def create_complaint(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.ComplaintCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Create complaint."""
    return await complaint_service.create_complaint(db, data, current_user)


@router.post("/{id}", response_model=models.ComplaintRead)
async def resolve_complaint(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    data: models.ComplaintResolve,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """Resolve a complaint."""
    complaint = await crud.complaint.get(db, id)
    if not complaint:
        raise HTTPException(404, "The complaint is not found!")

    return await complaint_service.resolve_complaint(db, complaint, current_user, data.reply)
