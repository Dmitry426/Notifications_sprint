import asyncpg
import backoff

from workers.workers.core.config import settings


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, TimeoutError, ConnectionError),
    max_time=settings.max_backoff,
)
async def postgres_connect():
    # connect = await asyncpg.connect(
    #     f"postgres://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.dbname}"
    # )
    pool = await asyncpg.create_pool(user=settings.user, password=settings.password,
                                     host=settings.host, port=settings.port,
                                     database=settings.dbname)
    return pool
