import json
from services.workers import consumer
from Configs.logger_notifications import logger
from Configs import config

import asyncio
import asyncpg

DB_NAME = config.settings.db_name
DB_USER = config.settings.db_user
DB_PASSWORD = config.settings.db_password
DB_HOST = config.settings.db_host
DB_PORT = config.settings.db_port


async def insert_notification(user_id, body) -> list:
    conn = await asyncpg.connect(f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    sql = f"""insert into events.notifications
              (user_id, body) VALUES ('{user_id}', '{body}')"""

    try:
        return await conn.execute(sql)
    finally:
        await conn.close()


def on_message(ch, method, properties, body):
    """Called when a message is received. Log message and ack it."""
    dict_body = json.loads(body)
    logger.info("Delivery properties: %s, message metadata: %s", method, properties)
    logger.info("Message body: %s", dict_body)
    logger.info(" [x] Received %r" % (dict_body,))

    asyncio.run(insert_notification(dict_body['user_id'], dict_body['body']))

    logger.info(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


consumer("websocket", on_message)
