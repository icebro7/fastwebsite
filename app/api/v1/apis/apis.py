from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.api import api_controller
from app.schemas import Success, SuccessExtra
from app.schemas.apis import *

router = APIRouter()


@router.get("/list", summary="查看API列表")
async def list_api(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    path: str = Query(None, description="API路径"),
    summary: str = Query(None, description="API简介"),
    tags: str = Query(None, description="API模块"),
):
    # Q对象用于构建查询条件
    q = Q()
    if path:
        q &= Q(path__contains=path)
    if summary:
        q &= Q(summary__contains=summary)
    if tags:
        q &= Q(tags__contains=tags)

    # 查询API列表
    total, api_objs = await api_controller.list(page=page, page_size=page_size, search=q, order=["tags", "id"])
    # 转换为字典列表，json序列化
    data = [await obj.to_dict() for obj in api_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看Api")
async def get_api(
    # 查询参数id，用于指定要获取的Api的ID
    id: int = Query(..., description="Api"),
):
    # 通过api_controller获取对应id的api对象
    api_obj = await api_controller.get(id=id)
    data = await api_obj.to_dict()
    return Success(data=data)


@router.post("/create", summary="创建Api")
async def create_api(
    api_in: ApiCreate,
):
    await api_controller.create(obj_in=api_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新Api")
async def update_api(
    api_in: ApiUpdate,
):
    await api_controller.update(id=api_in.id, obj_in=api_in)
    return Success(msg="Update Successfully")


@router.delete("/delete", summary="删除Api")
async def delete_api(
    # 指定要删除的Api的ID
    api_id: int = Query(..., description="ApiID"),
):
    await api_controller.remove(id=api_id)
    return Success(msg="Deleted Success")


@router.post("/refresh", summary="刷新API列表")
async def refresh_api():
    await api_controller.refresh_api()
    return Success(msg="OK")
