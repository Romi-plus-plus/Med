from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import Complaint, ComplaintCreate, PageParams


class CRUDComplaint(CRUDBase[Complaint, ComplaintCreate, SQLModel]):
    async def count_by_create_date(self, db: AsyncSession):
        return await self.count_by_date(db, Complaint.create_time)

    async def count_by_resolve_date(self, db: AsyncSession):
        return await self.count_by_date(db, Complaint.resolve_time)

    async def get_page_resolved(self, db: AsyncSession, page: PageParams):
        return await self.get_page_if(db, Complaint.resolve_time != None, page=page)

    async def get_page_unresolved(self, db: AsyncSession, page: PageParams):
        return await self.get_page_if(db, Complaint.resolve_time == None, page=page)


complaint = CRUDComplaint(Complaint)
