import json
import datetime
import uuid
from fastapi import APIRouter
from fastapi.params import Body
from starlette.requests import Request
from common.response import resp_400, resp_200
from models import Users
from src.tools.password import SelfPassWord,md5_password

router = APIRouter()


@router.get("/ping", summary="活性测试接口", response_description='Json')
async def ping(
        request: Request,
):

    # await request.app.state.redis.lpush('test', "6666")
    # s1 = '2023-08-09'
    # start_date = '2023-11-09'
    # 测试ck查询！
    # sql = f"SELECT DISTINCT(Mobile)  from zft_project_company.sell_pub_record spr where FbDate>='{s1}' and FbDate<='{start_date}'"
    # result = request.app.state.ck_client.query(sql).result_set
    # b = await request.app.state.redis.sadd('check_set', *[w[0] for w in result])

    # print(await request.app.state.redis.scard('check_set'),'bbbbbb')
    # print(await request.app.state.redis.delete("check_set"))
    # print(await request.app.state.redis.sismember('check_set',"18868286335"))
    # print(b,"bbb",type(b))
    # a = ['fenghaiwei','fenghaiwei1','fenghaiwei2']
    # b = await request.app.state.redis.delete(*a)
    # print(b)
    # if await request.app.state.redis.get('haha'):
    #     await request.app.state.redis.incrby('haha',increment=1)
    # else:
    #     await request.app.state.redis.set('haha',1)
    return {'code': 200, 'msg': 'ok'}


@router.post("/login/", summary="登录接口", response_description='Json')
async def login(request: Request,
                account: str = Body(description='账号'),
                password: str = Body(description='密码'),
                ):
    x_forwarded_for = request.headers.get("x-forwarded-for", "")  # 判断是否使用代理
    if x_forwarded_for:
        print(x_forwarded_for, "ips")
        log_ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip

    else:
        log_ip = ""
    check = await Users.filter(account=account).first()
    if not check:
        return resp_400(msg='账号或密码错误！')
    if check.status == 0:
        return resp_400(msg='账号已被冻结，请联系平台管理员！')
    # e = SelfPassWord()
    # pwd = e.encrypt(password)
    pwd = md5_password(password)
    if pwd == check.password:
        token = str(uuid.uuid4()).replace('-', '')

        target = {
            "name": check.name,
            "id": check.id.__str__(),
            "phone": check.account,
        }
        await request.app.state.redis.setex(token, 60 * 60 * 12 * 1, json.dumps(target))
        check.last_login_ip = log_ip
        check.last_login_time = datetime.datetime.now()
        await check.save()
        target.update({"token": token})
        return resp_200(data=target, msg="登录成功")

    else:
        return resp_400(data=None, msg="账号或密码错误！")
