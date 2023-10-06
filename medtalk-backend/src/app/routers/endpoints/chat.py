from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi_pagination import Page
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.db.utils import from_orm_async
from app.routers import deps
from app.service import chat_service

router = APIRouter()


@router.get("/stat", tags=["stat"])
async def get_chat_stats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_superuser),
):
    return await chat_service.get_stats(db)


@router.get("/", response_model=Page[models.ChatRead])
async def get_all_chats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: models.PageParams = Depends(),
    user: models.User = Depends(deps.get_current_active_superuser),
):
    """(Admin) Get all chats."""

    return await crud.chat.get_page(db, page=q, transformer=chat_service.to_reads_wrapped(db))


@router.get("/me", response_model=list[models.ChatRead])
async def get_my_chats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_user),
):
    """Get chats of current user."""
    chats = await crud.chat.get_by_user(db, user=user)
    chats2 = await chat_service.get_shared_chats(db, user)  # 还需要获取用户分享得到的
    return await chat_service.to_reads(db, chats + chats2)


@router.post("/", response_model=models.ChatRead)
async def create_chat(
    *,
    db: AsyncSession = Depends(deps.get_db),
    data: models.ChatCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Create a chat of current user."""
    data.user_id = current_user.id
    chat = await crud.chat.create(db, obj_in=data)
    return await chat_service.to_read(db, chat)


@router.delete("/{id}", response_model=str)
async def delete_chat(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Delete a chat. The operator must be the chat owner of superuser."""
    chat = await chat_service.access_chat(db, chat_id=id, user=current_user)
    await chat_service.delete_chat(db, chat)
    return "Successfully deleted the chat."


@router.get("/{chat_id}", response_model=models.ChatReadWithMessages)
async def get_chat(
    *,
    db: AsyncSession = Depends(deps.get_db),
    chat_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """Get chat contents."""
    chat = await chat_service.access_chat(db, chat_id=chat_id, user=current_user)
    return await chat_service.get_chat_with_feedbacks(db, chat=chat, user=current_user)


@router.put("/{chat_id}", response_model=models.ChatRead)
async def update_title(
    *,
    db: AsyncSession = Depends(deps.get_db),
    chat_id: int,
    data: models.ChatUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    chat = await chat_service.access_chat(db, chat_id=chat_id, user=current_user)
    chat = await chat_service.update_title(db, chat=chat, title=data.title)
    return await chat_service.to_read(db, chat)


@router.post("/{chat_id}")
async def send_question(
    *,
    db: AsyncSession = Depends(deps.get_db),
    chat_id: int,
    question: str = Body(),
    hint: str | None = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    chat = await chat_service.access_chat(
        db, chat_id=chat_id, user=current_user, allow_admin=False, update_time=True
    )
    return await chat_service.qa(db, chat=chat, question=question, hint=hint)


@router.post("/{chat_id}/note", response_model=models.MessageRead)
async def post_note(
    *,
    db: AsyncSession = Depends(deps.get_db),
    chat_id: int,
    data: models.NoteCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    chat = await chat_service.access_chat(db, chat_id=chat_id, user=current_user)
    return await chat_service.create_note(db, chat=chat, note_in=data)
