from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from app.core.exceptions import SettingNotFound
from app.core.init_app import (
    init_menus,
    init_superuser,
    make_middlewares,
    register_exceptions,
    register_routers,
)

try:
    from app.settings.config import settings
except ImportError:
    raise SettingNotFound("Can not import settings")


# 异步上下文管理器，用于处理应用程序的生命周期事件。
@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await Tortoise.generate_schemas()
    await init_superuser()
    await init_menus()
    yield
    await Tortoise.close_connections()


# 创建并配置 FastAPI 应用程序。
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.VERSION,
        openapi_url="/openapi.json",
        middleware=make_middlewares(),
        lifespan=lifespan,
    )
    register_exceptions(app)
    register_routers(app, prefix="/api")
    return app


app = create_app()
