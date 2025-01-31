import dataclasses
import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pathlib import PurePath
from types import GeneratorType
# SetIntStr, DictIntStrAny,
from fastapi import status

from fastapi.encoders import encoders_by_class_tuples
from fastapi.responses import Response
from typing import Union, Any, Optional, Dict, Callable, List
# 响应数据类型
from pydantic.json import ENCODERS_BY_TYPE
from pydantic.main import BaseModel

from starlette.responses import JSONResponse


def json_encoder(
        obj: Any,
        include: Optional[Any] = None,
        exclude: Optional[Any] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        custom_encoder: Optional[Dict[Any, Callable[[Any], Any]]] = None,
        sqlalchemy_safe: bool = True,
) -> Any:
    custom_encoder = custom_encoder or {}
    if custom_encoder:
        if type(obj) in custom_encoder:
            return custom_encoder[type(obj)](obj)
        else:
            for encoder_type, encoder_instance in custom_encoder.items():
                if isinstance(obj, encoder_type):
                    return encoder_instance(obj)
    if include is not None and not isinstance(include, (set, dict)):
        include = set(include)
    if exclude is not None and not isinstance(exclude, (set, dict)):
        exclude = set(exclude)
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(obj, Decimal):
        return str(obj)
    # return super().default(o)
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, BaseModel):
        encoder = getattr(obj.__config__, "json_encoders", {})
        if custom_encoder:
            encoder.update(custom_encoder)
        obj_dict = obj.dict(
            include=include,  # type: ignore # in Pydantic
            exclude=exclude,  # type: ignore # in Pydantic
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
        )
        if "__root__" in obj_dict:
            obj_dict = obj_dict["__root__"]
        return json_encoder(
            obj_dict,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
            custom_encoder=encoder,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, PurePath):
        return str(obj)
    if isinstance(obj, (str, int, float, type(None))):
        return obj
    if isinstance(obj, dict):
        encoded_dict = {}
        for key, value in obj.items():
            if (
                    (
                            not sqlalchemy_safe
                            or (not isinstance(key, str))
                            or (not key.startswith("_sa"))
                    )
                    and (value is not None or not exclude_none)
                    and ((include and key in include) or not exclude or key not in exclude)
            ):
                encoded_key = json_encoder(
                    key,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_value = json_encoder(
                    value,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_dict[encoded_key] = encoded_value
        return encoded_dict
    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple)):
        encoded_list = []
        for item in obj:
            encoded_list.append(
                json_encoder(
                    item,
                    include=include,
                    exclude=exclude,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
            )
        return encoded_list

    if type(obj) in ENCODERS_BY_TYPE:
        return ENCODERS_BY_TYPE[type(obj)](obj)
    for encoder, classes_tuple in encoders_by_class_tuples.items():
        if isinstance(obj, classes_tuple):
            return encoder(obj)

    errors: List[Exception] = []
    try:
        data = dict(obj)
    except Exception as e:
        errors.append(e)
        try:
            data = vars(obj)
        except Exception as e:
            errors.append(e)
            raise ValueError(errors)
    return json_encoder(
        data,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
        custom_encoder=custom_encoder,
        sqlalchemy_safe=sqlalchemy_safe,
    )


# 注意有个 * 号 不是笔误， 意思是调用的时候要指定参数 e.g.resp_200（data=xxxx)
def resp_200(*, data: Union[list, dict] = None, msg: str = "Success") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 200,
            'msg': msg,
            'data': json_encoder(data) if data else "",
        }
    )


def resp_200_lis(*, data: Union[list, dict] = None, msg: str = "Success") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,

        # {'code': 200, 'result': {'items': res, 'total': total},
        #                              'currentPage': page_number}
        content={
            'code': 200,
            'msg': msg,
            'result': {'items': json_encoder(data['data']), 'total': data['total']},
            'currentPage': data['cur_page'],
        }

    )


def resp_400(*, data: str = None, msg: str = "BAD REQUEST") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 400,
            'msg': msg,
            'data': data,
        }
    )

def resp_405(*, data: str = None, msg: str = "BAD REQUEST") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 405,
            'msg': msg,
            'data': data,
        }
    )

def resp_406(*, data: str = None, msg: str = "BAD REQUEST") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 406,
            'msg': msg,
            'data': data,
        }
    )




def result_200(*, data: Union[list, dict] = None, msg: str = "Success") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 200,
            'msg': msg,
            'result': json_encoder(data) if data else "",
        }
    )