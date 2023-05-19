import pytest
from app import models


@pytest.fixture
def test_vote(test_posts, test_user, session):
    vote = models.Vote(post_id=test_posts[0].id, user_id=test_user['id'])

    session.add(vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts, test_user):
    res = authorized_client.post(
        "/vote/", json={"dir": 1, "post_id": test_posts[0].id})

    assert res.status_code == 201


def test_vote_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"dir": 1, "post_id": test_posts[0].id})

    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"dir": 0, "post_id": test_posts[0].id})

    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"dir": 0, "post_id": test_posts[0].id})

    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"dir": 0, "post_id": 54676})

    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts, test_user):
    res = client.post(
        "/vote/", json={"dir": 1, "post_id": test_posts[0].id})

    assert res.status_code == 401
