from jose import jwt
import pytest
from app import schemas
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     assert res.status_code == 200
#     assert res.json().get('message') == 'Hello World'


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello@test.com", "password": "password123"})
    created_user = schemas.UserResponse(**res.json())
    assert created_user.email == "hello@test.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'],
                                      "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("aslam@test.com", "wrongPassword", 403),
    ("wrong@email.com", "pass123", 403),
    (None, "pass123", 422),
    ("aslam@test.com", None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email,
                                      "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"
