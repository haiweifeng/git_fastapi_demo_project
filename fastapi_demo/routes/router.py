# 这里完成所有路由的注册
from fastapi import APIRouter
from src.Login import views as login_views
from src.System import views as sys_views
router = APIRouter()
router.include_router(login_views.router, tags=["登录相关"], prefix="/login")
router.include_router(sys_views.router, tags=["系统相关接口"], prefix="/sys")




