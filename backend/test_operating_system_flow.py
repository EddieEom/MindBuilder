import httpx
import time
import uuid
import sys

BASE = "http://127.0.0.1:8000"

def fail(msg: str):
    print(msg)
    sys.exit(1)

email = f"testuser+{int(time.time())}@example.com"
payload = {
    "email": email,
    "nickname": "testuser",
    "provider": "google",
    "provider_user_id": str(uuid.uuid4()),
    "profile_image": None,
}

with httpx.Client(timeout=60.0) as client:
    print("1) 로그인 요청...", payload["email"])
    r = client.post(f"{BASE}/auth/login/oauth", json=payload)
    print(" status:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        fail("로그인 실패")

    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    print("\n2) 온보딩 시작")
    r = client.post(f"{BASE}/api/v1/onboarding/start", headers=headers)
    print(" start status:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        fail("온보딩 시작 실패")
    scan_id = r.json().get("scan_id")

    print("\n3) 질문 조회")
    r = client.get(f"{BASE}/api/v1/onboarding/questions")
    print(" questions status:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        fail("질문 조회 실패")
    data = r.json()
    questions = data.get("questions", [])
    answers = []
    for q in questions:
        opts = q.get("options", [])
        if opts:
            answers.append({
                "question_id": q["question_id"],
                "option_id": opts[0]["option_id"],
                "point_value": 0,
                "detail_text": None,
            })

    if not answers:
        fail("질문/옵션이 비어있어 샘플 답변을 만들 수 없습니다.")

    print("\n4) 답변 제출")
    req = {"scan_id": scan_id, "answers": answers}
    r = client.post(f"{BASE}/api/v1/onboarding/answers", json=req, headers=headers, timeout=120.0)
    print(" submit status:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        fail("답변 제출/분석 실패")

    print("\n5) LifeMap 생성")
    r = client.post(f"{BASE}/api/v1/lifemap/generate", headers=headers, timeout=120.0)
    print(" lifemap status:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        fail("LifeMap 생성 실패")

    print("\n6) OS 생성")
    r = client.post(f"{BASE}/api/v1/operating-system/generate", headers=headers, timeout=120.0)
    print(" generate status:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        fail("OS 생성 실패")

    print("\n7) 현재 OS 조회")
    r = client.get(f"{BASE}/api/v1/operating-system/current", headers=headers)
    print(" current status:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        fail("현재 OS 조회 실패")

    print("\n7) OS 히스토리 조회")
    r = client.get(f"{BASE}/api/v1/operating-system/history", headers=headers)
    print(" history status:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        fail("OS 히스토리 조회 실패")

    print("\n테스트 완료")
