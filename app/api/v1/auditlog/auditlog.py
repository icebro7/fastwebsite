from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.models.admin import AuditLog

from app.schemas import SuccessExtra
from app.schemas.apis import *
from app.core.dependency import DependPermisson

router = APIRouter()

@router.get('/list', summary="查看操作日志", dependencies=[DependPermisson])
async def get_audit_log_list(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    username: str = Query("", description="操作人名称"),
    module: str = Query("", description="功能模块"),
    summary: str = Query("", description="接口描述"),
    start_time: str = Query("", description="开始时间"),
    end_time: str = Query("", description="结束时间"),
):

    q = Q()
    if username:
        q &= Q(username__icontains=username)
    if module:
        q &= Q(module__icontains=module)
    if summary:
        q &= Q(summary__icontains=summary)
    if start_time and end_time:
        q &= Q(created_at__range=[start_time, end_time])
    elif start_time:
        q &= Q(created_at__gte=start_time)
    elif end_time:
        q &= Q(created_at__lte=end_time)

    # 使用构建好的查询对象和page、page_size完成offset和limit进行分页，并且按照created_at进行排序
    audit_log_objs = await AuditLog.filter(q).offset((page - 1) * page_size).limit(page_size).order_by("-created_at")
    total = await AuditLog.filter(q).count()
    data = [await audit_log.to_dict() for audit_log in audit_log_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)
