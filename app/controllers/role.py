from typing import List

from app.core.crud import CRUDBase
from app.models.admin import Api, Menu, Role
from app.schemas.roles import RoleCreate, RoleUpdate


class RoleController(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def __init__(self):
        super().__init__(model=Role)

    async def is_exist(self, name: str) -> bool:
        return await self.model.filter(name=name).exists()

    async def update_roles(self, role: Role, menu_ids: List[int], api_infos: List[dict]) -> None:
        await role.menus.clear()
        # 遍历传入的菜单 ID 列表，添加新的菜单关联
        for menu_id in menu_ids:
            menu_obj = await Menu.filter(id=menu_id).first()
            await role.menus.add(menu_obj)

        # 清除现有角色的 API 关联
        await role.apis.clear()

        # 遍历传入的菜单 ID 列表，添加新的菜单关联
        for item in api_infos:
            api_obj = await Api.filter(path=item.get("path"), method=item.get("method")).first()
            await role.apis.add(api_obj)


role_controller = RoleController()
