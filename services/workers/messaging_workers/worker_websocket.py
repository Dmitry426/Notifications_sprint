__all__ = ["websocket_server"]

import asyncio

import websockets
from websockets.legacy.server import WebSocketServerProtocol


from .core.config import settings
from .db.postgres import postgres_connect
from .models.websocket_postgres import UserWebsock
from .services.base_services import (
    confirm_token,
    get_notifications,
    update_notification,
)

FROM_MAIL = settings.mail.email_from
WS_HOST = settings.websocket.host
WS_PORT = settings.websocket.port


async def start(websocket):
    token = await websocket.recv()
    ray_token = await confirm_token(token)
    if not ray_token:
        await websocket.send("Error")
        return
    user_id = ray_token["sub"]
    while True:
        message = await get_notifications(
            postgres_connect=postgres_connect, user_id=user_id
        )
        for msg in message:
            msg = UserWebsock(**msg)
            await websocket.send(msg.body)
            await update_notification(postgres_connect=postgres_connect, id=str(msg.id))
        await asyncio.sleep(10)


async def receiver(websocket: WebSocketServerProtocol) -> None:
    await start(websocket)


def websocket_server():
    ws_server = websockets.serve(receiver, WS_HOST, WS_PORT)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws_server)
    loop.run_forever()
