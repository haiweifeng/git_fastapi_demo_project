#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import aiormq
import json
from settings.setting import logger, RABMQ_USERNAME, RABMQ_PASSWORD, RABMQ_HOST


async def sms_on_message(message):
    """
    异步消息存储到数据库
    """
    msg = json.loads(message.body)
    logger.info(f"{msg}")

async def vip_on_message(message):
    """
    执行消息推送！
    """
    msg = json.loads(message.body)
    logger.info(f"{msg}")


async def init_rmq_listen():
    global connection
    connection = await aiormq.connect(f"amqp://{RABMQ_USERNAME}:{RABMQ_PASSWORD}@{RABMQ_HOST}/")
    channel = await connection.channel()

    # Declaring queue
    declare_ok = await channel.queue_declare('demo1', auto_delete=False)
    await channel.basic_consume(
        declare_ok.queue, sms_on_message, no_ack=True
    )
    declare_ok2 = await channel.queue_declare('demo2', auto_delete=False)
    await channel.basic_consume(
        declare_ok2.queue, vip_on_message, no_ack=True
    )
