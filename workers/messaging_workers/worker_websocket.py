__all__ = ["websocket_server"]

import asyncio

import websockets
from websockets.legacy.server import WebSocketServerProtocol

from workers.messaging_workers.core import config
from workers.messaging_workers.core.config import settings
from workers.messaging_workers.db.postgres import postgres_connect
from workers.messaging_workers.models.websocket_postgres import UserWebsock
from workers.messaging_workers.services.base_services import (
    confirm_token,
    get_notifications,
    update_notification,
)

FROM_MAIL = settings.from_mail
WS_HOST = config.settings.ws_host
WS_PORT = config.settings.ws_port


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
