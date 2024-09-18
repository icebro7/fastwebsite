# @Time :2024/9/18 14:42
from fastapi import APIRouter
from .video import router

video_router = APIRouter()
video_router.include_router(router, tags=["视频模块"])

__all__ = ["video_router"]