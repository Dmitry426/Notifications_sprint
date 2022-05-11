from abc import ABC, abstractmethod


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    def set(self, key: str, **kwargs):
        pass

    @abstractmethod
    def add_token(self, key: str, expire: int, value: str):
        pass

    @abstractmethod
    def delete_token(self, key: str):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    def pipeline(self, **kwargs):
        pass
