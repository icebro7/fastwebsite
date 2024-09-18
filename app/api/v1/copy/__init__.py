# @Time :2024/9/8 16:54
from fastapi import APIRouter
from .copy import router

copy_router = APIRouter()
copy_router.include_router(router, tags=["爬虫模块"])

__all__ = ["copy_router"]