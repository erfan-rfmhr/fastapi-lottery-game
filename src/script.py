import asyncio

from db.get_db import get_redis

r_client = get_redis()


async def main():
    users = await r_client.get_users()
    for user_id in users:
        await r_client.reset_user_play_count(user_id=user_id)


asyncio.run(main())
