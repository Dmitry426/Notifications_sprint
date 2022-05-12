import asyncpg
import backoff

from workers.event_listeners.core.config import settings


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, TimeoutError, ConnectionError),
    max_time=30,
)
async def postgres_connect():
    connect = await asyncpg.connect(
        f"postgres://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.dbname}"
        # E501
    )
    return connect
