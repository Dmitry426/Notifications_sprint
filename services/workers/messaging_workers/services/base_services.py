from __future__ import annotations

__all__ = ["confirm_token", "get_notifications", "update_notification"]

import jwt
from asyncpg import connect


async def confirm_token(token: str) -> dict[str, any] | bool:
    try:
        claims = jwt.decode(token=token, key="some_secret_key", algorithms=["HS256"])  # type: ignore  # noqa
        return claims
    except Exception:
        return False


async def get_notifications(postgres_connect: connect, user_id: str) -> list:
    pool = await postgres_connect()
    sql = (
        f"""select body, id from events.notifications
              where user_id = '%s' and is_read = false"""
        % user_id
    )
    try:
        async with pool.acquire() as conn:
            return await conn.fetch(sql)
    finally:
        await pool.close()


async def update_notification(postgres_connect: connect, id: str) -> str:
    pool = await postgres_connect()
    sql = (
        f"""update events.notifications set is_read = true
              where id = '%s'
             """
        % id
    )
    try:
        async with pool.acquire() as conn:
            return await conn.execute(sql)
    finally:
        await pool.close()
