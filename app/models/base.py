import asyncio
from datetime import datetime

from tortoise import fields, models

from app.settings import settings


# 定义一个基础模型类
class BaseModel(models.Model):
    id = fields.BigIntField(pk=True, index=True)

    # 将模型实例转换为字典格式
    async def to_dict(self, m2m: bool = False, exclude_fields: list[str] | None = None):
        if exclude_fields is None:
            exclude_fields = []

        d = {}
        # 遍历模型中的所有数据库字段
        for field in self._meta.db_fields:
            if field not in exclude_fields:
                # 获取字段值
                value = getattr(self, field)
                if isinstance(value, datetime):
                    # 格式化日期时间
                    value = value.strftime(settings.DATETIME_FORMAT)
                d[field] = value

        if m2m:
            # 获取所有多对多字段的值
            tasks = [self.__fetch_m2m_field(field) for field in self._meta.m2m_fields if field not in exclude_fields]
            # 并发获取所有多对多字段的值
            results = await asyncio.gather(*tasks)
            for field, values in results:
                d[field] = values
        return d

    # 获取多对多字段的值
    async def __fetch_m2m_field(self, field):
        values = [value for value in await getattr(self, field).all().values()]
        for value in values:
            # 格式化日期时间
            value.update((k, v.strftime(settings.DATETIME_FORMAT)) for k, v in value.items() if isinstance(v, datetime))
        return field, values

    class Meta:
        abstract = True


# 定义一个uuid字段的模型类
class UUIDModel:
    uuid = fields.UUIDField(unique=True, pk=False, index=True)


# 定义一个包含时间戳字段的 Mixin 类
class TimestampMixin:
    # 创建时间字段，自动设置为当前时间，建立索引
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    # 更新时间字段，每次自动设置为当前时间，建立索引
    updated_at = fields.DatetimeField(auto_now=True, index=True)
