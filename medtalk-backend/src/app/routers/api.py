from fastapi import APIRouter

from app.routers.endpoints import (
    chat,
    complaints,
    feedbacks,
    login,
    questions,
    recommends,
    share,
    users,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(share.router, prefix="/share", tags=["share"])
api_router.include_router(feedbacks.router, prefix="/feedbacks", tags=["feedbacks"])
api_router.include_router(complaints.router, prefix="/complaints", tags=["complaints"])
api_router.include_router(recommends.router, prefix="/recommends", tags=["recommends"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])


@api_router.get("/")
def ping():
    return "OK"
