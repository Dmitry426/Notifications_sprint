import asyncio
import websockets
import jwt
import asyncpg

from Configs import config

FROM_MAIL = config.settings.from_mail
DB_NAME = config.settings.db_name
DB_USER = config.settings.db_user
DB_PASSWORD = config.settings.db_password
DB_HOST = config.settings.db_host
DB_PORT = config.settings.db_port
WS_HOST = config.settings.ws_host
WS_PORT = config.settings.ws_port


async def confirm_token(token):
    try:
        claims = jwt.decode(token, "some_secret_key", algorithms=["HS256"])
        return claims
    except Exception:
        return False


async def get_notifications(user_id) -> list:
    conn = await asyncpg.connect(f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    sql = f"""select body, id from events.notifications
              where user_id = '{user_id}' and is_read = false"""
    try:
        return await conn.fetch(sql)
    finally:
        await conn.close()


async def update_notification(id) -> list:
    conn = await asyncpg.connect(f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    sql = f"""update events.notifications set is_read = true
              where id = '{id}'
             """
    try:
        return await conn.execute(sql)
    finally:
        await conn.close()


async def start(websocket):
    token = await websocket.recv()
    ray_token = await confirm_token(token)
    if not ray_token:
        await websocket.send('Error')
        return
    user_id = ray_token['sub']
    while True:
        message = await get_notifications(user_id)
        for msg in message:
            await websocket.send(msg["body"])
            await update_notification(msg["id"])
        await asyncio.sleep(10)


async def receiver(websocket: websockets.WebSocketServerProtocol, path: str) -> None:
    await start(websocket)

if __name__ == '__main__':
    ws_server = websockets.serve(receiver, WS_HOST, WS_PORT)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws_server)
    loop.run_forever()
