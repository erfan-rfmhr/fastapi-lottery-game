import asyncio

from redis_connection import get_redis


async def main():
    r_client = await get_redis()
    users = await r_client.get_users()
    for user_id in users:
        await r_client.reset_user_play_count(user_id=user_id)


asyncio.run(main())
