from fastapi.routing import APIRoute

from app.core.crud import CRUDBase
from app.log import logger
from app.models.admin import Api
from app.schemas.apis import ApiCreate, ApiUpdate


class ApiController(CRUDBase[Api, ApiCreate, ApiUpdate]):
    def __init__(self):
        super().__init__(model=Api)

    async def refresh_api(self):
        from app import app

        # 获取所有 API 路由信息
        all_api_list = []
        for route in app.routes:
            if isinstance(route, APIRoute):
                all_api_list.append((list(route.methods)[0], route.path_format))

        # 找出需要删除的废弃 API 数据
        delete_api = []
        for api in await Api.all():
            if (api.method, api.path) not in all_api_list:
                delete_api.append((api.method, api.path))

        # 删除废弃的 API 数据
        for item in delete_api:
            method, path = item
            logger.debug(f"API Deleted {method} {path}")
            await Api.filter(method=method, path=path).delete()

        # 更新或创建 API 数据
        for route in app.routes:
            if isinstance(route, APIRoute):
                method = list(route.methods)[0]
                path = route.path_format
                summary = route.summary
                tags = list(route.tags)[0]
                api_obj = await Api.filter(method=method, path=path).first()
                if api_obj:
                    # 更新现有的 API 数据
                    await api_obj.update_from_dict(dict(method=method, path=path, summary=summary, tags=tags)).save()
                else:
                    # 创建新的 API 数据
                    logger.debug(f"API Created {method} {path}")
                    await Api.create(**dict(method=method, path=path, summary=summary, tags=tags))


api_controller = ApiController()
