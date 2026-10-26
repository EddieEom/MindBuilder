# MindBuilder

'나의 성장을 위한 인간 운영체제를 만들면 어떨까?'라는 생각에서 시작한 개인 실험입니다. 생각은 많은데 무엇부터 실행해야 할지 정리하기 어려웠고, AI를 그 과정에 써 보고 싶었습니다.

## 이 프로젝트에서 고민한 것

AI를 단순히 질문에 답하는 용도 외에 어떻게 활용하면 좋을지 고민했습니다. 질문과 기록을 저장하고, 규칙 기반 분석과 LLM의 추천으로 이어지는 구조를 앱으로 옮겨 봤습니다.

Flutter·FastAPI·PostgreSQL과 LLM API를 연결했고, 분석 규칙과 점수의 초안을 만드는 과정에도 AI를 활용했습니다. AI에 어떤 정보를 전달하고 어떤 처리를 코드로 나눌지 생각해 본 프로젝트입니다.

현재는 개인 프로토타입입니다. AI 활용 효율이나 사용자 성장 효과를 검증한 결과는 아니며, 전체 흐름의 통합 검증과 분석 기준 정리가 남아 있습니다.

<details>
<summary><b>⚙️ 환경변수 · 실행 방법</b></summary>

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

</details>

