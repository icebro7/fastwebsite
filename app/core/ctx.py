import contextvars

from starlette.background import BackgroundTasks
# 异步上下文中存储和访问当前id，如果没有用户id则返回0
CTX_USER_ID: contextvars.ContextVar[int] = contextvars.ContextVar("user_id", default=0)
# 异步上下文中存储和访问后台任务，如果没有任务被设置则返回None
CTX_BG_TASKS: contextvars.ContextVar[BackgroundTasks] = contextvars.ContextVar("bg_task", default=None)
