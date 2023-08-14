import os

from src.db.redis_connection import RedisConnection


def get_redis():
    r_session = RedisConnection(host=os.getenv('REDIS_HOST'))
    return r_session
