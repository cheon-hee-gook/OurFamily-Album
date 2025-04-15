import io
from fastapi import status
import uuid

def test_comment_lifecycle(authorized_client):
    # Step 1: 그룹 생성
    group_res = authorized_client.post("/api/groups/", json={"name": "댓글테스트그룹", "type": "가족"})
    assert group_res.status_code == 200
    group_id = group_res.json()["id"]

    # Step 2: 사진 업로드
    file = ("file", ("test.jpg", io.BytesIO(b"fake"), "image/jpeg"))
    upload = authorized_client.post(
        "/api/photos/",
        data={"group_id": group_id, "memo": "", "tags": ""},
        files=[file]
    )
    assert upload.status_code == 200
    photo_id = upload.json()["id"]

    # Step 3: 댓글 작성
    comment_res = authorized_client.post(
        f"/api/comments/photos/{photo_id}/comments",
        json={"text": "첫 댓글입니다"}
    )
    assert comment_res.status_code == 200
    comment = comment_res.json()
    assert comment["text"] == "첫 댓글입니다"
    comment_id = comment["id"]

    # Step 4: 댓글 조회
    get_res = authorized_client.get(f"/api/comments/photos/{photo_id}/comments")
    assert get_res.status_code == 200
    comments = get_res.json()
    assert any(c["id"] == comment_id for c in comments)

    # Step 5: 댓글 삭제
    delete_res = authorized_client.delete(f"/api/comments/{comment_id}")
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "댓글 삭제 완료"

    # Step 6: 삭제 후 댓글 조회
    get_res = authorized_client.get(f"/api/comments/photos/{photo_id}/comments")
    assert get_res.status_code == 200
    assert all(c["id"] != comment_id for c in get_res.json())


def test_create_comment_requires_auth(test_client):
    fake_photo_id = str(uuid.uuid4())
    test_client.headers.pop("Authorization", None)
    res = test_client.post(f"/api/comments/photos/{fake_photo_id}/comments", json={"text": "테스트 댓글"})
    assert res.status_code == 401