from datetime import datetime

from fastapi import HTTPException
from sqlmodel import func
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.models.feedback import Feedback, FeedbackUpdate
from app.models.user import User
from app.utils.sqlutils import is_today, is_yesterday
from app.utils.statutils import counter_helper


async def update_feedback(
    db: AsyncSession,
    data: FeedbackUpdate,
    user: User,
):
    """Update feedback of the user. Create feedback if necessary."""
    if data.mark_like and data.mark_dislike:
        data.mark_like = False  # Exclusive
    fb = await crud.feedback.get(db, (data.msg_id, user.id))
    if fb:
        fb.update_time = datetime.now()
        return await crud.feedback.update(db, db_obj=fb, obj_in=data)
        # 暂时不做互斥了……
    else:
        msg = await crud.message.get(db, data.msg_id)
        if not msg:
            raise HTTPException(404, "The message is not found!")
        return await crud.feedback.add(db, Feedback(user=user, **data.dict()))


async def get_temporal_stats(db: AsyncSession):
    return await counter_helper(
        db,
        (crud.feedback.count_by_update_date, "total"),
        (crud.feedback.count_like_by_update_date, "like"),
        (crud.feedback.count_dislike_by_update_date, "dislike"),
        (crud.feedback.count_comment_by_update_date, "comments"),
    )


async def get_stats(db: AsyncSession):
    return {
        "total": await crud.feedback.count(db),
        "total_like": await crud.feedback.count_if(db, Feedback.mark_like),
        "total_dislike": await crud.feedback.count_if(db, Feedback.mark_dislike),
        "total_comment": await crud.feedback.count_if(db, func.length(Feedback.content) > 0),
        "total_today": await crud.feedback.count_if(db, is_today(Feedback.update_time)),
        "total_like_today": await crud.feedback.count_if(
            db, Feedback.mark_like, is_today(Feedback.update_time)
        ),
        "total_dislike_today": await crud.feedback.count_if(
            db, Feedback.mark_dislike, is_today(Feedback.update_time)
        ),
        "total_comment_today": await crud.feedback.count_if(
            db, func.length(Feedback.content) > 0, is_today(Feedback.update_time)
        ),
        "total_yesterday": await crud.feedback.count_if(db, is_yesterday(Feedback.update_time)),
        "total_like_yesterday": await crud.feedback.count_if(
            db, Feedback.mark_like, is_yesterday(Feedback.update_time)
        ),
        "total_dislike_yesterday": await crud.feedback.count_if(
            db, Feedback.mark_dislike, is_yesterday(Feedback.update_time)
        ),
        "by_date": await get_temporal_stats(db),
    }
    # TODO 这里统计点击量是有问题的，应该在单独的表里计数
