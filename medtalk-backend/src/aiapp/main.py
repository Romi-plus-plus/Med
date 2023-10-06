from fastapi import Body, Depends, FastAPI

from aiapp.config import settings
from aiapp import service
from app.routers import deps
from sqlmodel.ext.asyncio.session import AsyncSession

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json")


@app.get("/api")
def ping():
    return "OK"


@app.post("/api/qa", tags=["ai"])
async def qa(
    db: AsyncSession = Depends(deps.get_db),
    question: str | list[str] = Body(),
):
    return await service.qa(db, question)
