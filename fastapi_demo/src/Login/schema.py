# from typing import Union
# # 这里存放自定义的schema
# from pydantic import BaseModel, Field
#
#
# class PointReq(BaseModel):
#     # 'source': 'app',
#     # '': 'pageCate',
#     # '': 'urlOrName',
#     # '': 'lastUrlOrName',
#
#
#     source: str = Field(title='来源')
#     page_cate: str = Field(title='类型')
#     url_or_name: str
#     last_url_or_name: str
#
#     password_hash: str = Field(max_length=20,min_length=6)
#     status: Union[int, None] = 1
#     depart_id: int = Field(gt=0,description='部门id',default=1)
#
#     class Config:
#         orm_mode = True

