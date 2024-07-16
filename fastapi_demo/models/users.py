import time

import pytz
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import datetime
import uuid
from src.tools.page import make_page


class Roles(models.Model):
    """
    角色role
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, '正常'), (STATUS_DELETE, '删除'))

    id = fields.UUIDField(pk=True, default=uuid.uuid4, editable=False)
    name = fields.CharField(max_length=64, verbose_name='角色名称', default='', null=True, blank=True)
    status = fields.IntField(default=STATUS_NORMAL,
                             choices=STATUS_ITEMS, verbose_name="状态")
    update_time = fields.DatetimeField(auto_now=True, verbose_name='更新时间')
    del_time = fields.DatetimeField(default=None, verbose_name='删除时间', null=True, blank=True)
    created_time = fields.DatetimeField(auto_now_add=True, verbose_name='创建时间', index=True)

    class Meta:
        # 角色表
        table = "waste_roles"

    @staticmethod
    async def query_by_search(search, **kwargs):
        result = Roles.filter(status=1)
        if 'name' in search and search['name']:
            result = result.filter(name__contains=search['name'])
        start = time.time()

        data = await make_page(result.order_by('-created_time'), cur_page=kwargs['cur_page'],
                               page_size=kwargs['page_size']).values()
        t1 = time.time()

        total = await result.count()
        print("查询时间1", t1 - start)
        print("查询时间2", time.time() - t1)
        return data, total


class Users(models.Model):
    """
    The User model
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, '正常'), (STATUS_DELETE, '删除'))
    id = fields.UUIDField(pk=True, default=uuid.uuid4, editable=False)
    number_id = fields.CharField(default="", max_length=64, verbose_name='数字id', null=True, blank=True)
    account = fields.CharField(max_length=128, verbose_name='账号', default='', null=True, blank=True)
    name = fields.CharField(max_length=128, verbose_name='用户姓名', default='', null=True, blank=True)
    head_img = fields.CharField(max_length=128, verbose_name='头像', default='', null=True, blank=True)
    phone = fields.CharField(max_length=16, verbose_name='手机号', default='', null=True, blank=True)
    password = fields.CharField(max_length=64, verbose_name='密码', default='', null=True, blank=True)

    log_ip = fields.CharField(max_length=64, verbose_name='登陆ip', default='', null=True, blank=True)
    log_time = fields.DatetimeField(verbose_name='登陆时间', null=True, blank=True)

    status = fields.IntField(default=STATUS_NORMAL,
                             choices=STATUS_ITEMS, verbose_name="状态")
    del_time = fields.DatetimeField(default=None, verbose_name='删除时间', null=True, blank=True)
    update_time = fields.DatetimeField(auto_now=True, verbose_name='更新时间')
    created_time = fields.DatetimeField(auto_now_add=True, verbose_name='创建时间', index=True)

    class Meta:
        # 管理员表
        table = "waste_users"

    class PydanticMeta:
        # computed = ["full_name"]  # 如果你想跨表搜索或join搜索，在computed里面定义
        exclude = ["password"]

    # def full_name(self) -> str:
    #     """
    #     此方法在序列化解析时每一行都会调用一次
    #     """
    # print(self.name,"sssss")
    # if self.name or self.family_name:
    #     return f"{self.name or ''} {self.family_name or ''}".strip()
    # return self.username

    @staticmethod
    async def query_by_search(search, **kwargs):
        result = Users.filter(del_time=None)
        if 'phone' in search and search['phone']:
            result = result.filter(phone__contains=search['phone'])
        if 'name' in search:
            result = result.filter(name__contains=search['name'])
        data = await make_page(result.order_by('-created_time'), cur_page=kwargs['cur_page'],
                               page_size=kwargs['page_size']).values()

        total = await result.count()
        return data, total


class NumberRoles(models.Model):
    """测试数字id角色表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, '正常'), (STATUS_DELETE, '删除'))
    id = fields.BigIntField(pk=True, editable=False)
    name = fields.CharField(max_length=64, verbose_name='角色名称', default='',null=True,blank=True)
    status = fields.IntField(default=STATUS_NORMAL,
                             choices=STATUS_ITEMS, verbose_name="状态")
    update_time = fields.DatetimeField(auto_now=True, verbose_name='更新时间')
    del_time = fields.DatetimeField(default=None, verbose_name='删除时间', null=True, blank=True)
    created_time = fields.DatetimeField(auto_now_add=True, verbose_name='创建时间',index=True)

    class Meta:
        verbose_name = verbose_name_plural = '测试数字id角色表'
        table = 'number_roles'

    @staticmethod
    async def query_by_search(search, **kwargs):
        result = NumberRoles.filter(status=1)

        if 'name' in search and search['name']:
            result = result.filter(name__contains=search['name'])
        start = time.time()
        data = await make_page(result.order_by('-created_time'), cur_page=kwargs['cur_page'],
                               page_size=kwargs['page_size']).values()
        t1 = time.time()
        total = await result.count()
        print("查询时间1", t1 - start)
        print("查询时间2", time.time() - t1)
        return data, total


