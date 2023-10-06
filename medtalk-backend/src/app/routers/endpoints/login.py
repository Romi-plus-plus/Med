from datetime import datetime, timedelta

from fastapi import APIRouter, Body, Depends, Form, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.routers import deps

# from app.utils import (
#     generate_password_reset_token,
#     send_reset_password_email,
#     verify_password_reset_token,
# )

router = APIRouter()


@router.post("/auth/register", response_model=models.UserRead)
async def register(
    *,
    db: AsyncSession = Depends(deps.get_db),
    username: str = Form(),
    password: str = Form(),
):
    """
    Create new user.
    """
    user_in = models.UserRegister(username=username, password=password)
    user = await crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.user.create(db, obj_in=models.UserCreate.from_orm(user_in, dict(role_id=1)))
    return user


@router.post("/auth/login", response_model=models.Token)
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_valid(user):
        raise HTTPException(status_code=400, detail="Invalid user")

    user.login_time = datetime.now()  # Update login time
    await crud.user.add(db, user)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
    }


@router.post("/auth", response_model=models.UserReadWithRole)
async def test_token(
    db: AsyncSession = Depends(deps.get_db),
    admin: bool | None = Body(None),
    perm: str | None = Body(None),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Test access token
    """
    # Check permissions
    if (admin and not crud.user.is_superuser(current_user)) or (
        perm and (perm not in await crud.user.get_perms(db, current_user))
    ):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return await db.run_sync(lambda _: models.UserReadWithRole.from_orm(current_user))


@router.post("/auth/logout")
async def logout():
    response = Response()
    response.delete_cookie("token")
    return response


'''
@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}

@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
'''
