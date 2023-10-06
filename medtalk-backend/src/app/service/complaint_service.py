from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.models.complaint import Complaint, ComplaintCreate
from app.models.page import PageParams
from app.models.user import User
from app.utils.sqlutils import is_today, time_now
from app.utils.statutils import counter_helper


async def get_all_complaints(db: AsyncSession, page: PageParams, resolved: bool | None):
    """Get all complaints or resolved/unresolved"""
    if resolved is None:
        return await crud.complaint.get_page(db, page=page)
    if resolved == True:
        return await crud.complaint.get_page_resolved(db, page=page)
    else:
        return await crud.complaint.get_page_unresolved(db, page=page)


async def create_complaint(db: AsyncSession, data: ComplaintCreate, user: User):
    """Create a new complaint."""
    complaint = Complaint(content=data.content, category=data.category, user=user)
    return await crud.complaint.add(db, complaint)


async def resolve_complaint(db: AsyncSession, complaint: Complaint, admin: User, reply: str):
    """Resolve a given complaint by the given admin and set its `resolve_time`."""
    complaint.admin = admin
    complaint.reply = reply
    complaint.resolve_time = time_now()

    return await crud.complaint.add(db, complaint)


async def get_temporal_stats(db: AsyncSession):
    return await counter_helper(
        db,
        (crud.complaint.count_by_create_date, "creation"),
        (crud.complaint.count_by_resolve_date, "resolution"),
    )


async def get_stats(db: AsyncSession):
    return {
        "total": await crud.complaint.count(db),
        "total_today": await crud.complaint.count_if(db, is_today(Complaint.create_time)),
        "resolved": await crud.complaint.count_if(db, Complaint.resolve_time != None),
        "resolved_today": await crud.complaint.count_if(
            db, Complaint.resolve_time != None, is_today(Complaint.resolve_time)
        ),
        "by_date": await get_temporal_stats(db),
    }
