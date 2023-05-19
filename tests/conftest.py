from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.config import settings
from app.orm import app
from alembic import command
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# This line created the tables in the db.
# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db


# client = TestClient(app)

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
    # We can also create tables using alembic
    # command.upgrade("head")

    # advantage of using yield
    # Runs code before yield. [more like before returning]

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    # Runs code after yield. [more like after returning]

    # We can also delete tables using alembic
    # command.downgrade("base")


@pytest.fixture
def test_user(client):
    new_user = {"email": "aslam@test.com",
                "password": "pass123"}
    res = client.post("/users/", json=new_user)

    created_user = res.json()
    assert res.status_code == 201
    created_user['password'] = new_user['password']

    return created_user


@pytest.fixture
def test_user2(client):
    new_user = {"email": "aslam123@test.com",
                "password": "pass123"}
    res = client.post("/users/", json=new_user)

    created_user = res.json()
    assert res.status_code == 201
    created_user['password'] = new_user['password']

    return created_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }

    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    new_posts = [
        {"title": "1st post",
         "content": "1st content",
         "owner_id": test_user['id']},

        {"title": "2nd post",
         "content": "2nd content",
         "owner_id": test_user['id']},

        {"title": "3rd post",
         "content": "3rd content",
         "owner_id": test_user['id']},

        {"title": "4th post",
         "content": "4th content",
         "owner_id": test_user2['id']},
    ]

    def map_dict_to_post_model(post):
        return models.Post(**post)

    mapped_posts = map(map_dict_to_post_model, new_posts)
    all_posts = list(mapped_posts)

    session.add_all(all_posts)
    session.commit()

    posts = session.query(models.Post).all()

    return posts
