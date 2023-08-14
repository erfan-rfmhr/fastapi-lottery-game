from unittest.mock import patch, AsyncMock

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'swagger': 'http://127.0.0.1:8000/docs'}


@patch("main.get_redis")
async def test_get_users(mock_get_redis):
    mock_redis = AsyncMock()
    mock_redis.get_users.return_value = {"user1": 0, "user2": 1}
    mock_get_redis.return_value = mock_redis

    response = client.get("/api/v1/users/get")
    assert response.status_code == 200
    assert response.json() == {"user1": 0, "user2": 1}


@patch("main.get_redis")
async def test_set_users(mock_get_redis):
    mock_redis = AsyncMock()
    mock_get_redis.return_value = mock_redis

    user_data = {"UUID": "user_id"}
    response = client.post("/api/v1/users/set", json=user_data)
    assert response.status_code == 201
    assert response.json() == user_data


@patch("main.get_redis")
@patch("main.perform_lottery")
async def test_play(mock_perform_lottery, mock_get_redis):
    mock_redis = AsyncMock()
    mock_redis.get_user_play_count.return_value = 2
    mock_get_redis.return_value = mock_redis
    mock_perform_lottery.return_value = "prize"

    user_data = {"UUID": "user_id"}
    response = client.post("/api/v1/lottery", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"user_id": "prize"}
