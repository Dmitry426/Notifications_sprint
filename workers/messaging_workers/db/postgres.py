import asyncpg
import backoff

from workers.messaging_workers.core.config import settings


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, TimeoutError, ConnectionError),
    max_time=settings.max_backoff,
)
async def postgres_connect():
    pool = await asyncpg.create_pool(
        user=settings.user,
        password=settings.password,
        host=settings.host,
        port=settings.port,
        database=settings.dbname,
        max_inactive_connection_lifetime=100,
    )
    return pool
