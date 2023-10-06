from logging import Logger
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi_pagination import Page
from app import crud, models
from app.core.security import verify_password
from app.routers import deps
from app.service import user_service
from app.utils.futils import save_file

router = APIRouter()

logger = Logger(__file__)


@router.get("/stat", tags=["stat"])
async def get_user_stats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_superuser),
):
    return await user_service.get_stats(db)


@router.get("/", response_model=Page[models.UserRead])
async def read_users(
    *,
    db: AsyncSession = Depends(deps.get_db),
    q: models.PageParams = Depends(),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    (Admin) Retrieve users.
    """
    return await crud.user.get_page(db, page=q)


@router.post("/", response_model=models.UserRead)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: models.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    (Admin) Create new user.
    """
    user = await crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = await crud.user.create(db, obj_in=user_in)
    """if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )"""
    return user


@router.get("/me", response_model=models.UserReadWithRole)
async def read_user_me(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get current user.
    """
    return await db.run_sync(lambda _: models.UserReadWithRole.from_orm(current_user))


@router.put("/me", response_model=models.UserRead)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    username: str = Form(None),
    email: EmailStr = Form(None),
    phone: str = Form(None),
    name: str = Form(None),
    password: str = Form(),
    password2: str = Form(None),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update own user.
    """
    # check password
    if not password:
        raise HTTPException(403, "You should send password!")
    if not verify_password(password, current_user.hashed_password):
        raise HTTPException(403, "The password is incorrect!")
    if password2 and password != password2:
        raise HTTPException(403, "The passwords are inconsistent!")
    user_in = models.UserUpdate(
        username=username or current_user.username,
        email=email or current_user.email,
        phone=phone or current_user.phone,
        name=name or current_user.name,
        avatar_url=current_user.avatar_url,
        password=password,
    )
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.post("/me/avatar", response_model=models.UserRead)
async def upload_avatar(
    *,
    db: AsyncSession = Depends(deps.get_db),
    file: UploadFile = File(),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    url = await save_file(file)
    current_user.avatar_url = url
    return await crud.user.add(db, current_user)


@router.get("/{user_id}", response_model=models.UserRead | None)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Get a specific user by id.
    """
    user = await crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user


@router.put("/{user_id}", response_model=models.UserRead)
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: models.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    (Admin) Update a user.
    """
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    return await crud.user.update(db, db_obj=user, obj_in=user_in)
