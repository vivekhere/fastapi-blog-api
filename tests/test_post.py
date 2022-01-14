import pytest
from fastapi import status
from app import schemas


def test_get_all_posts(auth_client, posts):
    res = auth_client.get("/posts")
    assert res.status_code == status.HTTP_200_OK
    res_posts = res.json()
    assert len(res_posts) == len(posts)

    def validate(post):
        return schemas.PostWithVotes(**post)
    map(validate, res_posts)


def test_get_post_not_exist(client):
    res = client.get("/posts/0")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post(client, posts):
    res = client.get(f"/posts/{posts[0].id}")
    post = schemas.PostWithVotes(**res.json())
    assert post.Post.id == posts[0].id
    assert post.Post.title == posts[0].title


@pytest.mark.parametrize("title, content, is_published", [
    ("awesome new title", "awesome new content", True),
    ("favourite pizza", "i love pepperoni", False),
    ("tallest skyscrapper", "Burj Khalifa", True)
])
def test_create_post(auth_client, user, title, content, is_published):
    res = auth_client.post(
        "/posts",
        json={"title": title, "content": content, "is_published": is_published}
    )
    assert res.status_code == status.HTTP_201_CREATED
    posts = schemas.Post(**res.json())
    assert posts.title == title
    assert posts.content == content
    assert posts.is_published == is_published
    assert posts.owner_id == user["id"]


def test_unauth_create_post(client, user):
    res = client.post(
        "/posts",
        json={"title": "New title", "content": "New content"}
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauth_delete_post(client, user, posts):
    res = client.delete(f"/posts/{posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post_success(auth_client, user, posts):
    res = auth_client.delete(f"/posts/{posts[0].id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_post_not_exist(auth_client, user):
    res = auth_client.delete("/posts/0")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_post_success(auth_client, user, posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": posts[0].id
    }
    res = auth_client.put(f"/posts/{posts[0].id}", json=data)
    assert res.status_code == status.HTTP_200_OK
    post = schemas.Post(**res.json())
    assert post.title == data["title"]
    assert post.content == data["content"]
