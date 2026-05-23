"""
API v1 router
"""
from fastapi import APIRouter

from app.api.v1 import repositories, documentation, pull_requests, chat, analysis

api_router = APIRouter()

api_router.include_router(
    repositories.router,
    prefix="/repositories",
    tags=["repositories"]
)

api_router.include_router(
    documentation.router,
    prefix="/documentation",
    tags=["documentation"]
)

api_router.include_router(
    pull_requests.router,
    prefix="/prs",
    tags=["pull-requests"]
)

api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"]
)

api_router.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["analysis"]
)
