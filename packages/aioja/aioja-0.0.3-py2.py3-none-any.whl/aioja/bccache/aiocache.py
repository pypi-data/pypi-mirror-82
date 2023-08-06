from aiocache import caches
from . import AsyncBytecodeCache


class AioCacheBytecodeCache(AsyncBytecodeCache):
    def __init__(
        self,
        cache_name: str = 'default',
        prefix: str = 'jinja2'
    ):
        self._backend = None
        self._cache_name = cache_name
        self._prefix = prefix

    @property
    def backend(self):
        if self._backend is None:
            self._backend = caches.get(self._cache_name)
        return self._backend

    def make_key(self, bucket):
        return '%s:%s' % (self._prefix, str(bucket.key))

    async def load_bytecode(self, bucket):
        key = self.make_key(bucket)
        bytecode = await self.backend.get(key)
        if bytecode:
            bucket.bytecode_from_string(bytecode)

    async def dump_bytecode(self, bucket):
        key = self.make_key(bucket)
        await self.backend.set(key, bucket.bytecode_to_string())
