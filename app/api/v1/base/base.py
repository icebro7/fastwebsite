from datetime import datetime, timedelta, timezone

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.controllers.user import user_controller
from app.core.ctx import CTX_USER_ID
from app.core.dependency import DependAuth
from app.models.admin import Api, Menu, Role, User
from app.schemas.base import Fail, Success
from app.schemas.login import *
from app.schemas.users import UpdatePassword
from app.settings import settings
from app.utils.jwt import create_access_token
from app.utils.password import get_password_hash, verify_password

router = APIRouter()


@router.post("/access_token", summary="获取token")
async def login_access_token(credentials: CredentialsSchema):
    # 通过用户名和密码验证用户
    user: User = await user_controller.authenticate(credentials)
    # 验证用户凭证并更新最后登录时间
    await user_controller.update_last_login(user.id)
    # 定义访问令牌的过期时间
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    # 计算访问令牌的过期时间：当前时间 + 过期时间间隔
    expire = datetime.now(timezone.utc) + access_token_expires
    # 生成访问令牌和用户名
    data = JWTOut(
        access_token=create_access_token(
            data=JWTPayload(
                user_id=user.id,
                username=user.username,
                is_superuser=user.is_superuser,
                exp=expire,
            )
        ),
        username=user.username,
    )
    return Success(data=data.model_dump())





@router.get("/userinfo", summary="查看用户信息", dependencies=[DependAuth])
async def get_userinfo():
    user_id = CTX_USER_ID.get()
    user_obj = await user_controller.get(id=user_id)
    # 排除密码字段
    data = await user_obj.to_dict(exclude_fields=["password"])
    data["avatar"] = 'https://avatars.githubusercontent.com/u/105137585?s=400&u=520fe343af10e1c4a2024c391eec1beed985c341&v=4'
    return Success(data=data)


@router.get("/usermenu", summary="查看用户菜单", dependencies=[DependAuth])
async def get_user_menu():
    user_id = CTX_USER_ID.get()
    user_obj = await User.filter(id=user_id).first()
    # 初始化一个空列表，用于存储用户的菜单
    menus: list[Menu] = []
    # 验证用户是否是超级用户
    if user_obj.is_superuser:
        menus = await Menu.all()
    else:
        # 从用户的角色中获取菜单
        role_objs: list[Role] = await user_obj.roles
        for role_obj in role_objs:
            # 获取角色的菜单对象
            menu = await role_obj.menus
            # 将角色的菜单添加到用户的菜单列表中
            menus.extend(menu)
        # 去重
        menus = list(set(menus))
    parent_menus: list[Menu] = []
    # 遍历用户的菜单
    for menu in menus:
        # 如果菜单的父id是0，则为父菜单，添加到父菜单列表中
        if menu.parent_id == 0:
            parent_menus.append(menu)
    res = []
    for parent_menu in parent_menus:
        parent_menu_dict = await parent_menu.to_dict()
        parent_menu_dict["children"] = []
        for menu in menus:
            # 如果菜单的父ID等于当前父菜单的ID，则是当前父菜单的子菜单
            if menu.parent_id == parent_menu.id:
                parent_menu_dict["children"].append(await menu.to_dict())
        res.append(parent_menu_dict)
    return Success(data=res)


@router.get("/userapi", summary="查看用户API", dependencies=[DependAuth])
async def get_user_api():
    user_id = CTX_USER_ID.get()
    user_obj = await User.filter(id=user_id).first()
    if user_obj.is_superuser:
        api_objs: list[Api] = await Api.all()
        # 将API对象转换为字符串列表
        apis = [api.method.lower() + api.path for api in api_objs]
        return Success(data=apis)
    # 从数据库中获取用户的所有角色对象
    role_objs: list[Role] = await user_obj.roles
    apis = []
    # 构建一个包含用户所有API权限的列表
    for role_obj in role_objs:
        api_objs: list[Api] = await role_obj.apis
        apis.extend([api.method.lower() + api.path for api in api_objs])
    apis = list(set(apis))
    return Success(data=apis)


@router.post("/update_password", summary="修改密码", dependencies=[DependAuth])
async def update_user_password(req_in: UpdatePassword):
    user_id = CTX_USER_ID.get()
    user = await user_controller.get(user_id)
    # 验证旧密码是否和数据库的用户密码相匹配
    verified = verify_password(req_in.old_password, user.password)
    if not verified:
        return Fail(msg="旧密码验证错误！")
    # 计算新密码的哈希值，并更新字段
    user.password = get_password_hash(req_in.new_password)
    await user.save()
    return Success(msg="修改成功")
