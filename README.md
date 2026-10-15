# MindBuilder

생각을 정리하거나 다음에 무엇을 해야 할지 갈피가 잡히지 않을 때, 질문에 답하고 결과를 살펴볼 수 있는 도구를 만들어 보고자 시작한 개인 프로젝트입니다.

## 진행 방식과 현재 상태

기획부터 앱·서버 개발까지 혼자 진행했습니다. 분석 점수와 규칙은 AI의 제안에 의존해 구성했습니다.

현재 전체 기능 중 어디까지 정상 동작하는지 체계적으로 확인한 기록은 정리하지 못했습니다. 분석 결과의 정확도와 실제 행동 결정에 도움이 되는지도 검증하지 않았습니다.

## 구성한 내용

기존 프로젝트는 다음과 같은 구성으로 작성했습니다. 아래 목록은 프로젝트의 구성 설명이며, 전체 기능의 정상 동작을 보장하는 체크리스트는 아닙니다.

- Flutter: 질문 입력과 분석 결과를 보여주는 앱
- FastAPI: 사용자·답변·분석 결과를 다루는 API
- PostgreSQL·SQLAlchemy·Alembic: 데이터 저장과 DB 변경 관리
- 답변을 점수와 규칙으로 처리하고 여러 분석 결과로 저장하는 구조
- OpenRouter: LLM 호출과 추천 문장 생성

기존 코드에서 사용하는 `Feature`, `Pattern`, `Growth`, `Identity`, `Life Map`, `Human OS`는 프로젝트 내부의 데이터·기능 이름입니다. 검증된 심리 분석 지표를 의미하지 않습니다.

## 정리가 필요한 부분

- 로그인부터 질문 응답, 분석, 결과 조회까지 실제 동작 범위 확인
- 분석 점수와 규칙이 어떤 근거로 정해졌는지 정리
- 같은 입력에 대한 결과와 오류 상황 기록

## 환경변수

### Backend

프로젝트 실행을 위해 `backend/.env`에 다음 설정이 필요합니다.

```env
POSTGRES_USER=mindbuilder_user
POSTGRES_PASSWORD=
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=mindbuilder

SECRET_KEY=
ALGORITHM=HS256

OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
```

> API Key와 Secret 값은 Repository에 Commit하지 않습니다.



## 실행 방법

### Backend

### 1. Clone

```bash
git clone https://github.com/EddieEom/MindBuilder.git
cd MindBuilder/backend
```

### 2. Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Migration

```bash
alembic upgrade head
```

### 5. Run

```bash
uvicorn app.main:app --reload
```


### Frontend

```bash
cd ../frontend
flutter pub get
flutter run
```

Backend Server 주소는

```text
frontend/lib/core/config/api_config.dart
```

에서 개발 환경에 맞게 설정합니다.

위 실행 안내는 기존 README의 개발 환경 설정을 유지한 것입니다. 이번 문서 정리 과정에서 앱과 서버를 다시 실행해 확인하지는 않았습니다.
