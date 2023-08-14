import uvicorn
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from db.get_db import get_redis
from schema.user import UserSchema
from utils.lottery import perform_lottery

app = FastAPI()


@app.get('/')
async def root():
    return {'swagger': 'http://127.0.0.1:8000/docs'}


@app.get('/api/v1/users/get')
async def get_users():
    r_client = get_redis()
    all_cache_users = await r_client.get_users()
    return JSONResponse(content=all_cache_users, status_code=status.HTTP_200_OK)


@app.post('/api/v1/users/set')
async def set_users(request: Request, user: UserSchema):
    r_client = get_redis()
    user_data = {str(user.UUID): 0}
    await r_client.set_user(user_data)

    return JSONResponse(content=user_data, status_code=status.HTTP_201_CREATED)


@app.post('/api/v1/lottery')
async def play(request: Request, user: UserSchema):
    r_client = get_redis()
    user_id = str(user.UUID)
    play_count = await r_client.get_user_play_count(user_id=user_id)
    if play_count == 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't play more than 3 times a day")
    lottery_prize = await perform_lottery()
    await r_client.increase_user_play_count(user_id=user_id)
    return JSONResponse(content={user_id: lottery_prize})


if __name__ == '__main__':
    uvicorn.run(app=app)
