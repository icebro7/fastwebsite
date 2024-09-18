from typing import Optional

import jwt
from fastapi import Depends, Header, HTTPException, Request

from app.core.ctx import CTX_USER_ID
from app.models import Role, User
from app.settings import settings


# 处理用户认证
class AuthControl:
    @classmethod
    async def is_authed(cls, token: str = Header(..., description="token验证")) -> Optional["User"]:
        try:
            # 如果是开发模式下的特殊 token
            if token == "dev":
                user = await User.filter().first()
                user_id = user.id
            else:
                # 解码 JWT token
                decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
                user_id = decode_data.get("user_id")
            # 获取用户对象
            user = await User.filter(id=user_id).first()
            if not user:
                raise HTTPException(status_code=401, detail="Authentication failed")
            # 设置上下文中的用户 ID
            CTX_USER_ID.set(int(user_id))
            return user
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="无效的Token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="登录已过期")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{repr(e)}")


# 处理权限控制
class PermissionControl:
    @classmethod
    async def has_permission(cls, request: Request, current_user: User = Depends(AuthControl.is_authed)) -> None:
        # 超级用户直接返回
        if current_user.is_superuser:
            return

        # 获取请求的方法和路径
        method = request.method
        path = request.url.path

        # 获取用户的角色
        roles: list[Role] = await current_user.roles
        if not roles:
            raise HTTPException(status_code=403, detail="The user is not bound to a role")

        # 获取角色关联的 API
        apis = [await role.apis for role in roles]

        # 去重并生成权限 API 列表
        permission_apis = list(set((api.method, api.path) for api in sum(apis, [])))

        # path = "/api/v1/auth/userinfo"
        # method = "GET"
        # 检查请求的方法和路径是否在权限 API 列表中，不在则抛出异常
        if (method, path) not in permission_apis:
            raise HTTPException(status_code=403, detail=f"Permission denied method:{method} path:{path}")


DependAuth = Depends(AuthControl.is_authed)
DependPermisson = Depends(PermissionControl.has_permission)
