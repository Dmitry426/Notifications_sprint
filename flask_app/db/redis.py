import os

from redis import Redis

from flask_app.db.cache import AbstractCache

# from db.cache import AbstractCache

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))


class RedisCache(AbstractCache):
    def get(self, key: str, **kwargs):
        return self.cache.get(f"{key}")

    def set(self, *args, **kwargs):
        self.cache.set(*args, **kwargs)

    def add_token(self, key, expire, value):
        self.cache.setex(name=f"{key}", time=expire, value=f"{value}")

    def delete_token(self, key: str):
        self.cache.delete(f"{key}")

    def close(self):
        self.cache.close()

    def pipeline(self, **kwargs):
        return self.cache.pipeline()


redis_db: RedisCache = RedisCache(
    cache_instance=Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True, charset="utf-8"
    )
)
