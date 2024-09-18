from enum import Enum, StrEnum


class EnumBase(Enum):
    @classmethod
    def get_member_values(cls):
        # 枚举所有成员的值
        return [item.value for item in cls._member_map_.values()]

    @classmethod
    def get_member_names(cls):
        # 枚举所有对象的名称
        return [name for name in cls._member_names_]


class MethodType(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
