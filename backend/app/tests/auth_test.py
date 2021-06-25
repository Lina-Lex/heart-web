from datetime import timedelta
from unittest.mock import AsyncMock

from app.auth import create_access_token, get_password_hash
from app.models import UserModel
from fastapi.testclient import TestClient
from settings import conf


def test_user_create(client: TestClient, monkeypatch):
    payload = {
        "username": "test",
        "fullName": "test user",
        "password": "password",
        "email": "test@mail.com",
    }

    user = UserModel(
        username="test",
        hashed_password=get_password_hash("password"),
        email="test@mail.com",
        full_name="test user",
    )

    monkeypatch.setattr(
        "app.routers.auth.create_user",
        AsyncMock(return_value=user),
    )
    expected_response = {
        "username": "test",
    }
    response = client.post("/api/auth/users/create", json=payload)
    assert response.json() == expected_response
    assert response.status_code == 200


def test_login_for_access_token(client: TestClient, monkeypatch):
    payload = {
        "username": "test",
        "password": "testpassword",
    }
    user = UserModel(
        username="test",
        hashed_password=get_password_hash("password"),
        email="test@mail.com",
        full_name="test user",
    )

    monkeypatch.setattr(
        "app.routers.auth.authenticate_user",
        AsyncMock(return_value=user),
    )
    access_token_expires = timedelta(minutes=conf.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": payload["username"]},
        expires_delta=access_token_expires,
    )
    expected_response = {"access_token": access_token, "token_type": "bearer"}

    response = client.post("/api/auth/users/token", json=payload)
    assert response.json() == expected_response
    assert response.status_code == 200


def test_read_users_me(client: TestClient):
    access_token_expires = timedelta(minutes=conf.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "testuser"},
        expires_delta=access_token_expires,
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("api/auth/users/me/", headers=headers)
    expected_response = {
        "username": "testuser",
    }
    assert response.json() == expected_response
    assert response.status_code == 200
