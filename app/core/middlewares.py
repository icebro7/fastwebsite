import re
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.dependency import AuthControl
from app.models.admin import AuditLog, User

from .bgtask import BgTasks


# 简单的中间件基类
class SimpleBaseMiddleware:
    # 初始化中间件，传入应用
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # 如果请求类型不是http，直接调应用
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)

        # 请求前执行，返回app
        response = await self.before_request(request) or self.app
        await response(request.scope, request.receive, send)
        # 请求后执行，返回None
        await self.after_request(request)

    async def before_request(self, request: Request):
        return self.app

    async def after_request(self, request: Request):
        return None


# 后台任务中间件
class BackGroundTaskMiddleware(SimpleBaseMiddleware):
    async def before_request(self, request):
        # 请求前，初始化后台任务对象
        await BgTasks.init_bg_tasks_obj()

    async def after_request(self, request):
        # 请求后，执行后台任务
        await BgTasks.execute_tasks()


# HTTP 审计日志中间件
class HttpAuditLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, methods: list, exclude_paths: list):
        super().__init__(app)
        self.methods = methods
        self.exclude_paths = exclude_paths

    async def get_request_log(self, request: Request, response: Response) -> dict:
        """
        根据request和response对象获取对应的日志记录数据
        """
        data: dict = {"path": request.url.path, "status": response.status_code, "method": request.method}
        # 路由信息
        app: FastAPI = request.app
        for route in app.routes:
            if (
                    isinstance(route, APIRoute)
                    and route.path_regex.match(request.url.path)
                    and request.method in route.methods
            ):
                data["module"] = ",".join(route.tags)
                data["summary"] = route.summary
        # 获取用户信息
        token = request.headers.get("token")
        user_obj = None
        if token:
            user_obj: User = await AuthControl.is_authed(token)
        data["user_id"] = user_obj.id if user_obj else 0
        data["username"] = user_obj.username if user_obj else ""
        return data

    # 请求前，空处理
    async def before_request(self, request: Request):
        pass

    # 请求后，记录审计日志
    async def after_request(self, request: Request, response: Response, process_time: int):
        if request.method in self.methods:  # 请求方法为配置的记录方法
            for path in self.exclude_paths:
                if re.search(path, request.url.path, re.I) is not None:
                    return
            data: dict = await self.get_request_log(request=request, response=response)
            data["response_time"] = process_time  # 响应时间
            await AuditLog.create(**data)

    # 记录处理时间
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time: datetime = datetime.now()
        await self.before_request(request)
        response = await call_next(request)
        end_time: datetime = datetime.now()
        process_time = int((end_time.timestamp() - start_time.timestamp()) * 1000)
        await self.after_request(request, response, process_time)
        return response
