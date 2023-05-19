from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostResponse(**post)

    post_map = map(validate, res.json())

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_that_not_exists(authorized_client, test_posts):
    res = authorized_client.get("/posts/8234")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = schemas.PostVoteResponse(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("Awesome", "I am progessing awesomely", True),
    ("Fullstack", "Let's build a fullstack app", False),
    ("Movies", "Let's watch more movies", False),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_published_default_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/", json={"title": "a title", "content": "some content"})

    created_post = schemas.PostResponse(**res.json())
    assert created_post.title == "a title"
    assert created_post.content == "some content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_create_posts(client):
    res = client.post(
        "/posts/", json={"title": "a title", "content": "some content"})
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_exists(authorized_client, test_posts):
    res = authorized_client.delete("/posts/46464")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == "updated title"
    assert updated_post.content == "updated content"


def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_not_exists(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
    }

    res = authorized_client.put("/posts/46464", json=data)
    assert res.status_code == 404
