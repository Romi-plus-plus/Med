from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.feedback import Feedback, FeedbackUpdate


class CRUDFeedback(CRUDBase[Feedback, FeedbackUpdate, FeedbackUpdate]):
    async def count_by_update_date(self, db: AsyncSession):
        return await self.count_by_date(db, Feedback.update_time)

    async def count_like_by_update_date(self, db: AsyncSession):
        return await self.count_if_by_date(db, Feedback.update_time, Feedback.mark_like == True)

    async def count_dislike_by_update_date(self, db: AsyncSession):
        return await self.count_if_by_date(db, Feedback.update_time, Feedback.mark_dislike == True)

    async def count_comment_by_update_date(self, db: AsyncSession):
        return await self.count_if_by_date(db, Feedback.update_time, Feedback.content != "")


feedback = CRUDFeedback(Feedback)
