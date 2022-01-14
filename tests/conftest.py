import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app import models
from app.database import get_db, Base
from app.main import app
from app.oauth2 import create_access_token
from .database import engine, TestingSessionLocal


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def user(client):
    user = {"email": "user1@email.com", "password": "123456"}
    res = client.post("/users", json=user)
    assert res.status_code == status.HTTP_201_CREATED
    user = {**res.json(), "password": user["password"]}
    return user


@pytest.fixture
def token(user):
    return create_access_token({"user_id": user["id"]})


@pytest.fixture
def auth_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def posts(user, session):
    posts = [{
        "title": "first title",
        "content": "first content",
        "owner_id": user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": user['id']
    }]

    def map_posts_to_models(post):
        return models.Post(**post)
    posts = list(map(map_posts_to_models, posts))

    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()
