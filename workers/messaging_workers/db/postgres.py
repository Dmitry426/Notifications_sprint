import asyncpg
import backoff

from workers.messaging_workers.core.config import settings


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, TimeoutError, ConnectionError),
    max_time=30,
)
async def postgres_connect():
    connect = await asyncpg.connect(
        f"postgres://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.dbname}"
    )
    return connect
