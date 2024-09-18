from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.controllers.user import UserCreate, user_controller
from app.core.exceptions import (
    DoesNotExist,
    DoesNotExistHandle,
    HTTPException,
    HttpExcHandle,
    IntegrityError,
    IntegrityHandle,
    RequestValidationError,
    RequestValidationHandle,
    ResponseValidationError,
    ResponseValidationHandle,
)
from app.models.admin import Menu
from app.schemas.menus import MenuType
from app.settings.config import settings

from .middlewares import BackGroundTaskMiddleware, HttpAuditLogMiddleware


# 创建中间件列表
def make_middlewares():
    middleware = [
        Middleware(
            CORSMiddleware,
            # 允许的源
            allow_origins=settings.CORS_ORIGINS,
            # 是否允许发送cookie
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            # 允许的HTTP方法
            allow_methods=settings.CORS_ALLOW_METHODS,
            # 允许的HTTP请求头
            allow_headers=settings.CORS_ALLOW_HEADERS,
        ),
        # 处理后台任务
        Middleware(BackGroundTaskMiddleware),
        # 记录HTTP请求的日志
        Middleware(
            HttpAuditLogMiddleware,
            methods=["GET", "POST", "PUT", "DELETE"],
            # 自动生成的规范，不需要记录
            exclude_paths=[
                "/docs",
                "/openapi.json",
            ],
        ),
    ]
    return middleware


# 注册异常处理函数，此处注册为全局异常处理器
def register_exceptions(app: FastAPI):
    app.add_exception_handler(DoesNotExist, DoesNotExistHandle)
    app.add_exception_handler(HTTPException, HttpExcHandle)
    app.add_exception_handler(IntegrityError, IntegrityHandle)
    app.add_exception_handler(RequestValidationError, RequestValidationHandle)
    app.add_exception_handler(ResponseValidationError, ResponseValidationHandle)


# 注册路由
def register_routers(app: FastAPI, prefix: str = "/api"):
    app.include_router(api_router, prefix=prefix)


# 初始化超级用户
async def init_superuser():
    user = await user_controller.model.exists()
    if not user:
        await user_controller.create_user(
            UserCreate(
                username="admin",
                email="admin@admin.com",
                password="123456",
                is_active=True,
                is_superuser=True,
            )
        )


# 初始化菜单
async def init_menus():
    menus = await Menu.exists()
    if not menus:
        parent_menu = await Menu.create(
            menu_type=MenuType.CATALOG,
            name="系统管理",
            path="/system",
            order=1,
            parent_id=0,
            icon="carbon:gui-management",
            is_hidden=False,
            component="Layout",
            keepalive=False,
            redirect="/system/user",
        )
        children_menu = [
            Menu(
                menu_type=MenuType.MENU,
                name="用户管理",
                path="user",
                order=1,
                parent_id=parent_menu.id,
                icon="material-symbols:person-outline-rounded",
                is_hidden=False,
                component="/system/user",
                keepalive=False,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="角色管理",
                path="role",
                order=2,
                parent_id=parent_menu.id,
                icon="carbon:user-role",
                is_hidden=False,
                component="/system/role",
                keepalive=False,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="菜单管理",
                path="menu",
                order=3,
                parent_id=parent_menu.id,
                icon="material-symbols:list-alt-outline",
                is_hidden=False,
                component="/system/menu",
                keepalive=False,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="API管理",
                path="api",
                order=4,
                parent_id=parent_menu.id,
                icon="ant-design:api-outlined",
                is_hidden=False,
                component="/system/api",
                keepalive=False,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="部门管理",
                path="dept",
                order=5,
                parent_id=parent_menu.id,
                icon="mingcute:department-line",
                is_hidden=False,
                component="/system/dept",
                keepalive=False,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="审计日志",
                path="auditlog",
                order=6,
                parent_id=parent_menu.id,
                icon="ph:clipboard-text-bold",
                is_hidden=False,
                component="/system/auditlog",
                keepalive=False,
            )
        ]
        await Menu.bulk_create(children_menu)
        parent_menu = await Menu.create(
            menu_type=MenuType.CATALOG,
            name="功能模块",
            path="/",
            order=2,
            parent_id=0,
            icon="mdi-fan-speed-1",
            is_hidden=False,
            component="Layout",
            keepalive=False,
            redirect="",
        )
        await Menu.create(
            menu_type=MenuType.MENU,
            name="页面生成",
            path="top-menu",
            order=1,
            parent_id=parent_menu.id,
            icon="mdi-fan-speed-1",
            is_hidden=False,
            component="/top-menu",
            keepalive=False,
        )

# 新建页面相关
