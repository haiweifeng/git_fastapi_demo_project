from typing import Union, Optional
# 这里存放自定义的schema
from fastapi.params import Body
from pydantic import BaseModel, Field


class UserAddReq(BaseModel):
    phone: str = Field(max_length=11, min_length=11)
    name: str
    nickname: str
    account: str
    rolesId: str
    dept_id: str
    power: int
    # rolesName: str
    password: str = Field(max_length=20, min_length=6)

    class Config:
        orm_mode = True


class UserEditReq(BaseModel):
    id: str
    phone: str = Field(max_length=11, min_length=11)
    name: str
    nickname: str
    account: str
    dept_id: str
    power: int
    rolesId: str
    password: str = Field(default=None)

    class Config:
        orm_mode = True


class RoleAddReq(BaseModel):
    name: str

    class Config:
        orm_mode = True


class RoleEditReq(BaseModel):
    id: str
    name: str
    status: int

    class Config:
        orm_mode = True

class BaseReqId(BaseModel):
    id: str

    class Config:
        orm_mode = True


class BaseReqNoneId(BaseModel):
    id: Union[str,None]=None

    class Config:
        orm_mode = True


class UserListReq(BaseModel):
    name: Union[str,None]=None
    date: Union[list,None]=None
    pageNumber: int = 1,
    pageSize: int = 20,
    class Config:
        orm_mode = True


class RolesListReq(BaseModel):
    name: Union[str,None]=None
    pageNumber: int = 1,
    pageSize: int = 20,
    class Config:
        orm_mode = True


class UsersResp(BaseModel):
    """用户返回信息格式"""

    number_id = '数字id'
    account = '账号'
    name = '用户姓名'
    head_img = '头像'
    phone = '手机号'
    log_ip = "登陆ip"
    log_time = "登陆time"
    status = '0不启用 1启用 状态'
    created_time = '创建时间'