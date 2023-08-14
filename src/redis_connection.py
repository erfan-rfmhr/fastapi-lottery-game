import redis


class RedisConnection:
    _instance = None  # This will hold the single instance

    def __new__(cls, host, port=6379, db=0):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = redis.Redis(host=host, port=port, db=db)
        return cls._instance

    async def get_client(self) -> redis.Redis:
        return self._client

    async def get_users(self) -> dict:
        all_cache_data = {}
        for key in self._client.scan_iter("*"):
            all_cache_data[key.decode('utf-8')] = self._client.get(key).decode('utf-8')
        return all_cache_data

    async def get_user_play_count(self, user_id) -> int:
        user_play_count = int(self._client.get(user_id))
        return user_play_count

    async def set_user(self, users: dict) -> None:
        for key, value in users.items():
            self._client.set(key, value)
            self._client.expire(key, time=24*3600)

    async def increase_user_play_count(self, user_id) -> None:
        play_count = int(self._client.get(user_id))
        self._client.set(user_id, play_count + 1)
        self._client.expire(user_id, time=24*3600)

    def __del__(self):
        self._client.close()
