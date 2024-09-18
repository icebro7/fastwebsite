from pydantic import BaseModel, Field

from app.models.enums import MethodType


# 定义 API 的基本结构
class BaseApi(BaseModel):
    path: str = Field(..., description="API路径", example="/api/v1/user/list")
    summary: str = Field("", description="API简介", example="查看用户列表")
    method: MethodType = Field(..., description="API方法", example="GET")
    tags: str = Field(..., description="API标签", example="User")


# 用于创建新的 API 对象
class ApiCreate(BaseApi):
    ...


# 用于更新的 API 对象
class ApiUpdate(BaseApi):
    id: int
