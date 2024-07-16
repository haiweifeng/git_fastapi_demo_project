#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import json

from fastapi.params import Header, Form, Body
from starlette.requests import Request

from src.System.views import router
from typing import List, Union
from common.response import resp_200, resp_400, resp_200_lis, result_200
from models import Users, Roles
from src.System.schema import *
from src.tools.page import make_page


@router.post("/roles_list/", summary='角色列表展示')
async def roles_list(
        name: str = Form(description='name', default=""),
        pageSize: int = Form(description='条数', default=20, le=100),
        pageNumber: int = Form(description='页码', default=1),
):
    search = {'name': name}
    data, total = await Roles.query_by_search(search, page_size=pageSize, cur_page=pageNumber)

    res = {'data': data, 'page_size': pageSize, "cur_page": pageNumber, 'total': total}
    return resp_200_lis(data=res, msg='success')


@router.post("/role_add/", summary='添加角色')
async def role_add(request: Request,
                   roles_add: RoleAddReq,
                   ):
    # 尝试下不同的写法
    params = roles_add.dict(exclude_unset=True)
    # user = request.app.state.user
    await Roles.create(**params)
    return resp_200(data=None, msg='success')


@router.post("/role_edit/", summary='编辑角色')
async def role_edit(role: RoleEditReq,
                    ):
    params = role.dict(exclude_unset=True)
    role_id = params.get('id')
    del params['id']
    await Roles.filter(id=role_id).update(**params)
    return resp_200(data=None, msg='success')


@router.post("/role_del/", summary='删除角色')
async def role_del(role: BaseReqId,
                   ):
    role_id = role.dict().get('id', "")
    data = await Roles.filter(id=role_id, del_time=None).first()

    if not data:
        return resp_400(data=None, msg='参数异常!')
    else:
        data.del_time = datetime.datetime.now()
        await data.save()
        return resp_200(data=None, msg='success')
