__all__ = ["confirm_token", "get_notifications", "update_notification"]


from typing import Any, Dict, Union

import jwt
from asyncpg import connect


async def confirm_token(token: str) -> Union[Dict[str, Any], bool]:
    try:
        claims = jwt.decode(token, "some_secret_key", algorithms=["HS256"])
        return claims
    except Exception:
        return False


async def get_notifications(conn: connect, user_id: Dict[str, Any]) -> str:
    conn = await conn()

    sql = f"""select body, id from events.notifications
              where user_id = '{user_id}' and is_read = false"""
    try:
        return await conn.fetch(sql)
    finally:
        await conn.close()


async def update_notification(conn: connect, id: str) -> str:
    conn = await conn()

    sql = f"""update events.notifications set is_read = true
              where id = '{id}'
             """
    try:
        return await conn.execute(sql)
    finally:
        await conn.close()
