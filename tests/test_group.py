from fastapi import status


def test_join_group_success(test_client):
    # Step 1: 방장 회원가입 + 로그인
    signup_res = test_client.post("/api/auth/signup", json={
        "email": "owner@example.com",
        "password": "ownerpass",
        "name": "방장"
    })
    assert signup_res.status_code == 200

    login_res = test_client.post("/api/auth/login", json={
        "email": "owner@example.com",
        "password": "ownerpass"
    })
    token = login_res.json()["access_token"]
    test_client.headers.update({"Authorization": f"Bearer {token}"})

    # Step 2: 그룹 생성
    group_res = test_client.post("/api/groups/", json={"name": "가족모임", "type": "가족"})

    assert group_res.status_code == 200
    invite_code = group_res.json()["invite_code"]
    group_id = group_res.json()["id"]

    # Step 3: 다른 유저 회원가입 + 로그인
    signup_res = test_client.post("/api/auth/signup", json={
        "email": "second@example.com",
        "password": "secondpass",
        "name": "두번째유저"
    })
    assert signup_res.status_code == 200

    login_res = test_client.post("/api/auth/login", json={
        "email": "second@example.com",
        "password": "secondpass"
    })
    token = login_res.json()["access_token"]
    test_client.headers.update({"Authorization": f"Bearer {token}"})

    # Step 4: 그룹 참여
    join_res = test_client.post(f"/api/groups/join?invite_code={invite_code}")
    assert join_res.status_code == 200
    assert join_res.json()["id"] == group_id
