from fastapi import status


def test_signup_success(test_client):
    payload = {
        "email": "newuser@example.com",
        "password": "newpassword123",
        "name": "신규유저"
    }
    res = test_client.post("/api/auth/signup", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]


def test_signup_duplicate_email(test_client):
    payload = {
        "email": "newuser@example.com",
        "password": "newpassword123",
        "name": "중복유저"
    }

    # 최초 가입
    res = test_client.post("/api/auth/signup", json=payload)
    assert res.status_code == 200

    # 중복 가입 시도
    res = test_client.post("/api/auth/signup", json=payload)
    assert res.status_code == 400


def test_login_success(test_client):
    payload = {
        "email": "newuser@example.com",
        "password": "newpassword123",
        "name": "유저"
    }
    # 최초 가입
    res = test_client.post("/api/auth/signup", json=payload)
    assert res.status_code == 200

    res = test_client.post("/api/auth/login", json={
        "email": "newuser@example.com",
        "password": "newpassword123"
    })
    assert res.status_code == 200
    token = res.json()["access_token"]
    assert token
    global access_token
    access_token = token


def test_login_fail_wrong_password(test_client):
    res = test_client.post("/api/auth/login", json={
        "email": "newuser@example.com",
        "password": "wrongpass"
    })
    assert res.status_code == 401


def test_get_me_success(test_client, new_user_token):
    headers = {"Authorization": f"Bearer {new_user_token}"}
    res = test_client.get("/api/auth/me", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "newuser@example.com"


def test_get_me_unauthorized(test_client):
    res = test_client.get("/api/auth/me")
    assert res.status_code == 401
