from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.models.user import User
from app.utils.sqlutils import is_today
from app.utils.statutils import counter_helper


async def get_temporal_stats(db: AsyncSession):
    return await counter_helper(
        db,
        (crud.user.count_by_register_date, "register"),
        (crud.user.count_by_login_date, "login"), # This is no use, since it's variable
    )


async def get_stats(db: AsyncSession):
    return {
        "total": await crud.user.count(db),
        "register_today": await crud.user.count_if(db, is_today(User.create_time)),
        "login_today": await crud.user.count_if(db, is_today(User.login_time)),
        "active_today": await crud.message.count_distinct_sender_today(db),
        "by_date": await get_temporal_stats(db),
    }
