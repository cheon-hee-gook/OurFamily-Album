import io
import uuid
from fastapi import status


def test_photo_lifecycle(authorized_client):
    # 1. 그룹 생성
    group_res = authorized_client.post("/api/groups/", json={"name": "테스트그룹", "type": "기타"})
    assert group_res.status_code == 200
    group_id = group_res.json()["id"]

    # 2. 사진 업로드
    file_content = io.BytesIO(b"fake-image-content")
    file = ("file", ("test.jpg", file_content, "image/jpeg"))
    data = {
        "group_id": group_id,
        "memo": "테스트 메모",
        "tags": "가족,여행"
    }
    upload_res = authorized_client.post("/api/photos/", data=data, files=[file])
    assert upload_res.status_code == 200
    photo = upload_res.json()
    photo_id = photo["id"]
    assert photo["memo"] == "테스트 메모"
    assert len(photo["tags"]) == 2

    print(type(group_id))

    # 3. 목록 조회
    list_res = authorized_client.get(f"/api/photos/?group_id={group_id}")
    assert list_res.status_code == 200
    assert any(p["id"] == photo_id for p in list_res.json())

    # 4. 상세 조회
    detail_res = authorized_client.get(f"/api/photos/{photo_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["id"] == photo_id

    # 5. 삭제
    delete_res = authorized_client.delete(f"/api/photos/{photo_id}")
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "삭제 완료"

    # 6. 삭제 확인
    confirm_res = authorized_client.get(f"/api/photos/{photo_id}")
    assert confirm_res.status_code == 404
