#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
from typing import List

from fastapi import Form
from tortoise.transactions import in_transaction

from common.response import resp_200, resp_400, resp_200_lis
from models import Users,   Roles
from src.System.schema import *
from src.System.views import router
from src.tools.password import SelfPassWord, md5_password
from starlette.requests import Request


@router.post("/user_list/", summary='用户列表展示',response_model=UsersResp)
async def user_list(
                   phone: str = Form(description='phone', default=""),
                   name: str = Form(description='name', default=""),
                   pageSize: int = Form(description='条数', default=20,le=100),
                   pageNumber: int = Form(description='页码', default=1),
                   ):
    search = {"phone": phone, 'name': name}
    data, total = await Users.query_by_search(search, page_size=pageSize, cur_page=pageNumber)

    res = {'data': data, 'page_size': pageSize, "cur_page": pageNumber, 'total': total}
    return resp_200_lis(data=res, msg='success')


@router.post("/user_add/", description='创建用户', summary='创建用户')
async def user_add(request: Request,
                   name: str = Form(description='姓名'),
                   phone: str = Form(description='电话'),
                   password: str = Form(description='密码', default=''),
                   account: str = Form(description='账号'),
                   ):
    # user = request.app.state.user
    # user_name = user['name']  # 想加上添加人可以用登录信息
    app = await Users.filter(account=account,del_time=None).first()
    if app:
        return resp_400(msg='该账号已存在！')
    if not password:
        password = 'Aa123456'
    pwd = md5_password(password)

    params = {'name': name, 'phone': phone, 'password': pwd, 'account': account,
              }
    async with in_transaction() as connection:
        event = Users(**params)
        await event.save(using_db=connection)
    return resp_200(data=None, msg='success')


@router.post("/user_edit/", description='编辑用户', summary='编辑用户')
async def user_edit(name: str = Form(description='姓名'),
                    id: str = Form(description='id'),
                    phone: str = Form(description='电话'),
                    password: str = Form(description='密码', default=''),
                    account: str = Form(description='账号'),
                    ):
    data = await Users.filter(id=id,del_time=None).first()
    if not data:
        return resp_400(msg='参数异常！')
    if data.account != account:
        check = await Users.exclude(id=id).filter(account=account,del_time=None).first()
        if check:
            return resp_400(msg='该账号已存在！')
    data.name = name
    data.phone = phone
    if password:
        pwd = md5_password(password)
        data.password = pwd
    data.account = account
    await data.save()
    return resp_200(msg='success')


@router.post("/user_del/", summary='删除用户')
async def user_del(request: Request,
                   ids: List[str] = Form(description='ids'),):
    try:
        _ids = ids[0].split(',')
        obj = Users.filter(id__in=_ids)
        await obj.update(del_time=datetime.datetime.now())
        return resp_200(msg='删除成功！')
    except Exception as e:
        return resp_400(msg=str(e))


@router.post("/user_info/", description='获取用户信息', summary='获取用户信息')
async def user_info(request: Request,
                   ):
    user = request.app.state.user
    user = await Users.filter(id=user['id']).values('id', 'phone', 'account')
    return resp_200(data=list(user)[0])
