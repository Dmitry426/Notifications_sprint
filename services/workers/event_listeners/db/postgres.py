import asyncpg
import backoff

from ..core.config import settings


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, TimeoutError, ConnectionError),
    max_time=settings.backoff_timeout,
)
async def postgres_connect():
    pool = await asyncpg.create_pool(
        user=settings.postgres.user,
        password=settings.postgres.password,
        host=settings.postgres.host,
        port=settings.postgres.port,
        database=settings.postgres.dbname,
    )
    return pool
