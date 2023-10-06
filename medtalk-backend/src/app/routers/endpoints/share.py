from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.routers import deps
from app.service import chat_service, share_service

router = APIRouter()


@router.post("/", response_model=models.SharedLinkRead)
async def create_share(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.SharedLinkCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Create a shared link with unique URL. The creator must be the chat owner or admin"""
    chat = await chat_service.access_chat(db, data.chat_id, current_user)
    return await share_service.create_share(db, data, chat)


@router.delete("/{id}", response_model=models.SharedLinkRead)
async def delete_share(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    "Delete a existent shared link by link. Current user must be the chat owner or admin."
    share = await crud.share.get_one(db, id)
    assert share.chat_id
    chat = await chat_service.access_chat(db, share.chat_id, current_user)
    share.valid = False
    return await crud.share.add(db, share)


@router.get("/{id}", response_model=models.SharedLinkRead)
async def get_share(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: str,
    user: models.User | None = Depends(deps.get_current_active_user_opt),
):
    "Request, and try consuming a shared link."
    return await share_service.get_share(db, id, user)


@router.put("/{id}", response_model=models.SharedLinkRead)
async def update_share(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: str,
    data: models.SharedLinkUpdate,
    user: models.User | None = Depends(deps.get_current_active_superuser),
):
    "Update a shared link."
    share = await crud.share.get_one(db, id)
    return await crud.share.update(db, db_obj=share, obj_in=data)


@router.get("/", response_model=Page[models.SharedLinkRead])
async def get_links(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: models.PageParams = Depends(),
    user: models.User = Depends(deps.get_current_active_superuser),
):
    "(Admin) Get all shared links"
    return await crud.share.get_page(db, page=q)
