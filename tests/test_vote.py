from fastapi import status


def test_vote(auth_client, posts):
    res = auth_client.post("/vote", json={"post_id": posts[0].id})
    assert res.status_code == status.HTTP_200_OK


def test_auth_vote(client, posts):
    res = client.post("/vote", json={"post_id": posts[0].id})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
