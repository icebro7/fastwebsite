import logging

from fastapi import APIRouter, Query

from app.controllers.menu import menu_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.menus import *

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="查看菜单列表")
async def list_menu(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
):
    # 获取指定menu_id的菜单以及它的所有子菜单
    async def get_menu_with_children(menu_id: int):
        menu = await menu_controller.model.get(id=menu_id)
        menu_dict = await menu.to_dict()
        child_menus = await menu_controller.model.filter(parent_id=menu_id).order_by("order")
        menu_dict["children"] = [await get_menu_with_children(child.id) for child in child_menus]
        return menu_dict
    # 获取所有父菜单
    parent_menus = await menu_controller.model.filter(parent_id=0).order_by("order")
    # 获取每个父菜单的子菜单
    res_menu = [await get_menu_with_children(menu.id) for menu in parent_menus]
    return SuccessExtra(data=res_menu, total=len(res_menu), page=page, page_size=page_size)


@router.get("/get", summary="查看菜单")
async def get_menu(
    menu_id: int = Query(..., description="菜单id"),
):
    # 获取的菜单信息
    result = await menu_controller.get(id=menu_id)
    return Success(data=result)


@router.post("/create", summary="创建菜单")
async def create_menu(
    menu_in: MenuCreate,
):
    await menu_controller.create(obj_in=menu_in)
    return Success(msg="Created Success")


@router.post("/update", summary="更新菜单")
async def update_menu(
    menu_in: MenuUpdate,
):
    await menu_controller.update(id=menu_in.id, obj_in=menu_in)
    return Success(msg="Updated Success")


@router.delete("/delete", summary="删除菜单")
async def delete_menu(
    id: int = Query(..., description="菜单id"),
):
    # 检查是否有子菜单
    child_menu_count = await menu_controller.model.filter(parent_id=id).count()
    if child_menu_count > 0:
        return Fail(msg="不能删除菜单及其子菜单")
    await menu_controller.remove(id=id)
    return Success(msg="Deleted Success")
