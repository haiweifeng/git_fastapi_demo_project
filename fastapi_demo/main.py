import time
import zoneinfo
from typing import Optional

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.params import Header
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
import json
import aioredis
from routes.router import router
from fastapi import FastAPI, Request, Depends,applications
from settings.setting import *
from tortoise.contrib.fastapi import register_tortoise
from fastapi.openapi.docs import get_swagger_ui_html

from src.tools.mq_listen import init_rmq_listen
from src.tools.tools import task1


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='/static/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger-ui.css',
        swagger_favicon_url='/static/favicon.png',
    )


applications.get_swagger_ui_html = swagger_monkey_patch

async def verify_token(
        request: Request,
        token: Optional[str] = Header(None, description='login+point模块可以不传！'),):
    # 全局依赖函数：此处执行在中间件之后，请求之前。。。
    # 这一行让所有api都有了token这个参数，不信你看api文档
    pass
    # if not token:
    #     raise HTTPException(status_code=400, detail="请携带token!")

app = FastAPI(
    debug=DEBUG,
    title=TITLE,
    description=DESCRIPTION,
    docs_url=DOCS_URL,
    openapi_url=OPENAPI_URL,
    redoc_url=REDOC_URL,
    dependencies=[Depends(verify_token), ])

register_tortoise(
    app,
    # db_url=DB_URL,
    # modules={"models": [MODEL_PATH]},
    config=TORTOISE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=False,
)

app.mount('/static', StaticFiles(directory='static'), name='static')
# -------------这是定时任务的配置不需要刻意删除-------------------------------------
zo = zoneinfo.ZoneInfo("Asia/Shanghai")  # America/New_York
job_defaults = {
    'coalesce': True,
    'max_instances': 1,
    'misfire_grace_time': 1000*60*60  # 600秒的任务超时容错
}

JOBSTORES = {"default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URL)}

scheduler = AsyncIOScheduler(timezone=zo, jobstores=JOBSTORES, job_defaults=job_defaults)
# -------------------------------------------------------------------------------------


app.include_router(router)  # , prefix='/api' 加前缀


if not DEBUG:
    # 这里控制是否启动rabbitmq监听
    app.add_event_handler("startup", init_rmq_listen)


@app.on_event("startup")
async def startup():
    app.state.redis = await aioredis.create_redis(
        address=(REDIS_URL, REDIS_PORT), db=REDIS_DB, encoding="utf-8",

    )  # password=REDIS_PASS
    if not DEBUG:
        # 这里可以控制在不同环境下不同任务的启动
        scheduler.remove_all_jobs()
        scheduler.add_job(id="night_1", name="night_1",func=task1, trigger="cron",
                          day_of_week='mon-sun',replace_existing=True,
                          hour='17', minute='00', second='01')
        scheduler.start()
    else:
        # 连接ck的时候写入，可以在request中直接使用
        # import clickhouse_connect
        # app.state.ck_test_logs = clickhouse_connect.get_client(
        #     host='10.10.25.110', port=8123, username="default",
        #     password='feng1991', database="database")
        # app.state.redis = await aioredis.create_redis(
        #     address=(REDIS_URL, REDIS_PORT), db=REDIS_DB, encoding="utf-8",
        # )
        scheduler.remove_all_jobs()
        scheduler.add_job(id="night_1", name="night_1", func=task1, trigger="cron",
                          day_of_week='mon-sun', replace_existing=True,
                          hour='17', minute='00', second='01')
        scheduler.start()





# @app.on_event("startup")  # 应用启动时执行装饰的方法
# @repeat_every(wait_first=True,seconds=60*60*2)  # 1 hour
# async def remove_expired_tokens_task() -> None:
#     # 这里可以在程序启动后周期性执行任务 -->source fastapi-utils
#     pass


@app.on_event("shutdown")
async def shutdown():
    # scheduler.shutdown()

    await app.state.redis.wait_closed()



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    # 进入请求前处理
    if not [1 for w in NO_TOKEN_URL_LIST if w in request.url.__str__()]:
        sts = await check_token(request.headers.get('token',""))
        if not sts:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'code': 1000,
                    'message': 'token异常！',
                    'data': {},
                }
            )
    response = await call_next(request)
    # 请求返回之后的处理
    process_time = time.time() - start_time

    response.headers["X-Use-Time"] = str(process_time)
    print("请求时间：", process_time)
    return response

app.add_middleware(  # 解决跨域问题
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

async def check_token(token):
    if token:
        try:
            data = await app.state.redis.get(token)
            app.state.user = json.loads(data)
            return True
        except:
            return False
    else:
        return False


# 后台任务
# async def sendtxt(email: str, background_tasks: BackgroundTasks):
#     background_tasks.add_task(write_notification, email, message="不关注")
#     return {"message": "在后台读写"}


def get_local_ip():
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# 获取本机IP地址



if __name__ == '__main__':
    import uvicorn
    # 第一次多进程启动的时候可能会去创建一个apscheduler表，导致报错。是因为搞了好几次导致的，不影响。后续就正常了
    local_ip = get_local_ip()
    uvicorn.run('main:app', host=f'{local_ip}', port=8686, workers=3)
    # reload=True,
    # gunicorn main:app -b 0.0.0.0:8000 -w 2 -k uvicorn.workers.UvicornWorker --max-requests 10000 --log-level=info --access-logfile -

