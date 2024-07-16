#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from tortoise import fields, models
import datetime
import uuid

from tortoise.functions import Count

from src.tools.page import make_page


class AssetInfoTable(models.Model):
    """帖子表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = ((STATUS_NORMAL, '正常'), (STATUS_DELETE, '删除'))
    id = fields.UUIDField(pk=True, default=uuid.uuid4, editable=False)
    title = fields.CharField(max_length=128, verbose_name='帖子标题', default='', null=True, blank=True)
    desc = fields.TextField(verbose_name='帖子描述', default='', null=True, blank=True)
    user_name = fields.TextField(verbose_name='联系人', null=True, blank=True, default="")
    user_phone = fields.TextField(verbose_name='电话', null=True, blank=True, default="")
    source = fields.IntField(default=0, verbose_name='来源类型', null=True, blank=True)
    front_sts = fields.IntField(default=1, verbose_name='前台状态', null=True, blank=True)
    cycle = fields.IntField(default=1, verbose_name='周期', null=True, blank=True)
    source_record_id = fields.CharField(default="", max_length=64, verbose_name='各种来源的记录id', null=True, blank=True)
    accept_man_id = fields.CharField(default="", max_length=64, verbose_name='申领人id', null=True, blank=True)
    accept_man_name = fields.CharField(default="", max_length=64, verbose_name='申领人name', null=True, blank=True)
    accept_time = fields.DatetimeField(default=None,null=True,blank=True, verbose_name='申领时间')
    number_id = fields.CharField(default="",max_length=64, verbose_name='数字id', null=True, blank=True, index=True)
    power_sts = fields.IntField(default=1, verbose_name='状态', null=True, blank=True)
    sheng_id = fields.CharField(default="", max_length=64, verbose_name='省ID', null=True, blank=True, index=True)
    shi_id = fields.CharField(default="", max_length=64, verbose_name='市ID', null=True, blank=True, index=True)
    zone_id = fields.CharField(verbose_name='区id', null=True, blank=True, max_length=64, default="")
    address = fields.CharField(verbose_name='地址', null=True, blank=True, max_length=128, default="")
    week = fields.CharField(verbose_name='周', null=True, blank=True, max_length=64, default="")
    cate_name = fields.CharField(verbose_name='分类全称', null=True, blank=True, max_length=128, default="")
    c1 = fields.CharField(verbose_name='类别1', null=True, blank=True, max_length=64, default="")
    c2 = fields.CharField(verbose_name='类别2', null=True, blank=True, max_length=64, default="")
    c3 = fields.CharField(verbose_name='类别3', null=True, blank=True, max_length=64, default="")
    vol = fields.CharField(max_length=64, verbose_name='处置量', default='', null=True, blank=True)
    unit = fields.CharField(max_length=64, verbose_name='单位', default='', null=True, blank=True)
    images = fields.TextField(verbose_name='图片数组-前端转为json字符串', default='', null=True, blank=True)
    video_url = fields.TextField(verbose_name='视频url', default='', null=True, blank=True)
    key_words = fields.TextField(verbose_name='关键词', default='', null=True, blank=True)
    labels = fields.TextField(verbose_name='标签', default='', null=True, blank=True)
    value = fields.IntField(default=0, verbose_name='价值判定', null=True, blank=True)
    valuation = fields.IntField(default=8, verbose_name='估值', null=True, blank=True)
    company_name = fields.CharField(verbose_name='公司名称', null=True, blank=True, max_length=128, default="")
    com_sheng_id = fields.CharField(default="", max_length=64, verbose_name='省ID', null=True, blank=True)
    com_shi_id = fields.CharField(default="", max_length=64, verbose_name='市ID', null=True, blank=True)
    com_zone_id = fields.CharField(verbose_name='区id', null=True, blank=True, max_length=64, default="")
    com_address = fields.CharField(verbose_name='地址', null=True, blank=True, max_length=64, default="")
    industry = fields.CharField(verbose_name='所属行业', null=True, blank=True, max_length=64, default="")
    industry_id = fields.IntField(default=0, verbose_name='行业id', null=True, blank=True)
    remark = fields.TextField(verbose_name='备注', default='', null=True, blank=True)
    end_date = fields.DateField(default=None,null=True,blank=True, verbose_name='有效截止日期')
    add_time = fields.DateField(default=None,null=True,blank=True, verbose_name='添加时间')
    status = fields.IntField(default=STATUS_NORMAL,
                             choices=STATUS_ITEMS, verbose_name="状态")
    update_time = fields.DatetimeField(auto_now=True, verbose_name='更新时间')
    del_time = fields.DatetimeField(default=None, verbose_name='删除时间', null=True, blank=True)
    created_time = fields.DatetimeField(auto_now_add=True, verbose_name='创建时间',index=True)

    class Meta:
        verbose_name = verbose_name_plural = '帖子表'
        db_table = 'asset_info_table'

    @staticmethod
    async def query_by_search(search, **kwargs):
        # TODO:这个接口我不想写了，参数太多了，有兴趣的可以尝试下，这就是为什么喜欢django的原因
        result = AssetInfoTable.filter(del_time=None).order_by('-created_time')
        contains = ["title","desc", "user_name","user_phone","company_name"]
        for b in contains:
            if b in search and search[b]:
                result = result.filter(**{b+"__contains": search[b]})
        check1 = ["number_id","c1","c2","sheng_id",
                  "front_sts","source","value","accept_man_id",
                  "shi_id","zone_id"
                  ]
        for w in check1:
            if w in search and search[w]:
                result = result.filter(**{w: search[w]})
        if 'start_time' in search and search['start_time']:
            startTime = datetime.datetime.strptime(search['start_time'], '%Y-%m-%d')
            result = result.filter(created_time__gte=startTime)
        if 'end_time' in search and search['end_time']:
            endTime = datetime.datetime.strptime(search['end_time'], '%Y-%m-%d') + datetime.timedelta(days=1)
            result = result.filter(created_time__lt=endTime)
        if "is_next" in search and search['is_next']:  # 获取下一条
            if "power_sts" in search and search["power_sts"]:
                result = result.filter(power_sts=search["power_sts"])
            index = (int(search['pageNumber'])-1)*int(search['pageSize'])+int(search['position'])
            total = await result.count()
            if index >= total:
                return -1,-1, []  # 表示超出限制没有数据
            elif index < 0:
                return -2,-2, []
            else:
                data = await make_page(result, cur_page=index,
                                       page_size=1).values()
                return total,1, data

        else:
            others = result.group_by('power_sts').annotate(nums=Count('id'))

            if "power_sts" in search and search["power_sts"]:
                result = result.filter(power_sts=search["power_sts"])
            total = await result.count()
            data = await make_page(result, cur_page=kwargs['cur_page'],
                                   page_size=kwargs['page_size']).values()

            return total, others, data





