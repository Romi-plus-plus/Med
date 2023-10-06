from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.models import User, Recommendation, RecommendationCreate, PageParams


async def get_active_recommends(db: AsyncSession):
    """Get active recommendations which can be seen by users."""
    return await crud.recommend.get_active_ones(db)


async def get_all_recommends(db: AsyncSession, page: PageParams, active: bool | None):
    """Get all recommendations or active/inactive."""
    if active is None:
        return await crud.recommend.get_page(db, page=page)
    elif active:
        return await crud.recommend.get_page_if(db, Recommendation.remove_time == None, page=page)
    else:
        return await crud.recommend.get_page_if(db, Recommendation.remove_time != None, page=page)


async def add_recommend(db: AsyncSession, obj_in: RecommendationCreate, user: User):
    """Add a new recommendation by the user."""
    return await crud.recommend.add(
        db, Recommendation(title=obj_in.title, content=obj_in.content, creator=user)
    )


async def remove_recommend(db, rec_id: int, user: User):
    """Remove a recommendation by the user."""
    rec = await crud.recommend.get(db, rec_id)
    if not rec:
        return None
    rec.remove_time = datetime.now()
    rec.remover = user
    return await crud.recommend.add(db, rec)


async def recover_recommend(db, rec_id: int, user: User):
    """Recover a removed recommendation by the user."""
    rec = await crud.recommend.get(db, rec_id)
    if not rec:
        return None
    rec.remove_time = None
    rec.remover = None
    return await crud.recommend.add(db, rec)
