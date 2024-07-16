# -*- coding:utf-8 -*-
import asyncio
import random
import re
import string
import redis
from settings.setting import *


async def task1():
    await asyncio.sleep(round(random.randint(50, 150) / random.randint(100, 180), 2))
    if not DEBUG:
        conn = redis.Redis(host=REDIS_URL, port=REDIS_PORT, db=REDIS_DB,password=REDIS_PASS,
                           decode_responses=True)
    else:
        conn = redis.Redis(host=REDIS_URL, port=REDIS_PORT, db=REDIS_DB,
                           decode_responses=True)

    lock_key = f'task1_lock'
    val = conn.get(lock_key)

    if not val:
        conn.setex(lock_key, 60, 1)
        logger.info('开始执行task1')
    else:
        print('没进去...')


def ret_equip_type(txt):
    if re.search("Android", txt):
        return 'Android'
    elif re.search("iPhone|iPad|iPod",txt):
        return 'iOS'
    elif re.search("Windows",txt):
        return 'PC'
    else:
        return 'Unknown'


def get_unique_code():
    str1 = string.ascii_letters + string.digits
    res = ""
    for i in range(5):
        res += random.choice(str1)
    return res


if __name__ == '__main__':
    get_unique_code()