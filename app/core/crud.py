from typing import Any, Dict, Generic, List, NewType, Tuple, Type, TypeVar, Union

from pydantic import BaseModel
from tortoise.expressions import Q
from tortoise.models import Model

# 定义一个新类型 Total，表示总数
Total = NewType("Total", int)
# 定义类型变量 ModelType，约束为 Tortoise ORM 的 Model 类型
ModelType = TypeVar("ModelType", bound=Model)
# 定义类型变量 CreateSchemaType，约束为 Pydantic 的 BaseModel 类型
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# 定义类型变量 UpdateSchemaType，约束为 Pydantic 的 BaseModel 类型
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    # 定义异步方法 get，用于通过 ID 获取模型实例
    async def get(self, id: int) -> ModelType:
        return await self.model.get(id=id)

    # 定义异步方法 list，用于分页查询模型实例
    async def list(self, page: int, page_size: int, search: Q = Q(), order: list = []) -> Tuple[Total, List[ModelType]]:
        query = self.model.filter(search)
        return await query.count(), await query.offset((page - 1) * page_size).limit(page_size).order_by(*order)

    # 定义异步方法 create，用于创建模型实例
    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        if isinstance(obj_in, Dict):
            obj_dict = obj_in
        else:
            obj_dict = obj_in.model_dump()
        obj = self.model(**obj_dict)
        await obj.save()
        return obj

    # 定义异步方法 update，用于更新模型实例
    async def update(self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        if isinstance(obj_in, Dict):
            obj_dict = obj_in
        else:
            obj_dict = obj_in.model_dump(exclude_unset=True, exclude={"id"})
        obj = await self.get(id=id)
        obj = obj.update_from_dict(obj_dict)
        await obj.save()
        return obj

    # 定义异步方法 remove，用于删除模型实例
    async def remove(self, id: int) -> None:
        obj = await self.get(id=id)
        await obj.delete()
