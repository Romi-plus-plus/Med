from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud, models
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_STR}/auth/login", auto_error=False)


async def get_db():
    """Get AsyncSession"""
    async with SessionLocal() as session:
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str | None = Depends(reusable_oauth2)
) -> models.User:
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = models.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_valid(current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")
    return current_user


async def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return current_user


async def get_current_user_opt(
    *, db: AsyncSession = Depends(get_db), token: str | None = Depends(reusable_oauth2)
) -> models.User | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = models.TokenPayload(**payload)
    except (JWTError, ValidationError):
        return None
    user = await crud.user.get(db, id=token_data.sub)
    return user


async def get_current_active_user_opt(
    current_user: models.User | None = Depends(get_current_user_opt),
) -> models.User | None:
    return current_user
