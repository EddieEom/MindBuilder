import httpx
import time
import uuid

BASE = "http://127.0.0.1:8000"

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
        raise SystemExit("로그인 실패")

    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # 시작
    print('\n2) 온보딩 시작')
    r = client.post(f"{BASE}/api/v1/onboarding/start", headers=headers)
    print(" status:", r.status_code)
    print(r.text)
    if r.status_code != 200:
        raise SystemExit("온보딩 시작 실패")
    scan_id = r.json().get("scan_id")

    # 질문 조회
    print('\n3) 질문 조회')
    r = client.get(f"{BASE}/api/v1/onboarding/questions")
    print(" status:", r.status_code)
    data = r.json()
    print(' question set:', data.get('set_name'))

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
        print("질문/옵션이 비어있어 샘플 답변을 만들 수 없습니다.")
    else:
        req = {"scan_id": scan_id, "answers": answers}
        print('\n4) 답변 제출 (온보딩 완료 및 분석 트리거)')
        r = client.post(f"{BASE}/api/v1/onboarding/answers", json=req, headers=headers, timeout=120.0)
        print(" status:", r.status_code)
        print(r.text)
        if r.status_code != 200:
            raise SystemExit("답변 제출/분석 실패")

        resp = r.json()
        print('\n== Pattern/Growth/Identity 결과 요약 ==')
        print('pattern_id:', resp.get('pattern_id'))
        print('confidence:', resp.get('confidence'))
        print('scores keys:', list(resp.get('scores', {}).keys()))
        growth = resp.get('growth')
        identity = resp.get('identity')
        print('\ngrowth keys:', list(growth.keys()) if growth else None)
        print('identity keys:', list(identity.keys()) if identity else None)

    print('\n테스트 완료')
