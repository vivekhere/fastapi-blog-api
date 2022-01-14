import pytest
from fastapi import status
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "user1@email.com", "password": "123456"})
    assert res.status_code == status.HTTP_201_CREATED
    user = schemas.User(**res.json())
    assert user.email == "user1@email.com"


def test_login(user, client):
    res = client.post(
        "/login",
        data={"username": user["email"], "password": user["password"]})
    assert res.status_code == status.HTTP_200_OK
    token = schemas.Token(**res.json())
    payload = jwt.decode(token.access_token, settings.secret_key,
                         [settings.algorithm])
    assert user["id"] == payload.get("user_id")
    assert token.token_type == "bearer"


@pytest.mark.parametrize("email, password, status_code", [
    ("wrong@email.com", "123456", status.HTTP_401_UNAUTHORIZED),
    ("user1@email.com", "wrongpassword", status.HTTP_401_UNAUTHORIZED),
    ("wrong@email.com", "wrongpassword", status.HTTP_401_UNAUTHORIZED),
    (None, "123456", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("user1@email.com", None, status.HTTP_422_UNPROCESSABLE_ENTITY)
])
def test_incorrect_login(user, client, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password})
    assert res.status_code == status_code
