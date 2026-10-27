# MindBuilder

**질문과 기록을 바탕으로 생각·행동을 정리하는 '인간 운영체제'를 실험한 개인 프로토타입입니다.**

<img src="frontend/artifacts/previews/hos.png" alt="저장소에 보관된 Human OS 화면 미리보기. 실서비스 연동 검증 화면과 구분" width="360"/>

위 이미지는 저장소에 보관된 **화면 미리보기**입니다. 실제 계정·DB·LLM을 연결해 이번 작업에서 새로 캡처한 화면은 아닙니다.

[담당 범위](#담당-범위) · [개발 과정](#개발-과정) · [코드와 확인 범위](#코드와-확인-범위) · [실행 방법](#실행-방법)

## 담당 범위

아이디어와 질문·기록·분석·추천의 기능 구성을 정하고 Flutter·FastAPI·PostgreSQL·LLM을 연결하는 개인 실험을 진행했습니다. 분석 규칙과 점수 초안에는 AI를 활용했습니다. 코드 작성 도구별 기여율은 기록이 없어 수치로 제시하지 않습니다.

## 개발 과정

### 'AI를 붙인다'는 생각을 기능으로 나누기

생각은 많지만 무엇부터 실행해야 할지 정리하기 어려웠던 경험에서 시작했습니다. 처음 구상은 '나를 분석해서 다음 행동을 알려주는 AI'였지만, 이를 코드로 옮기려면 입력·기록·분석·추천을 나눠야 했습니다.

질문 응답을 저장하고, 규칙으로 분석한 정보를 LLM 추천에 사용하는 구조를 구성했습니다. AI에 무엇을 맡길지뿐 아니라 어떤 정보를 정리해 전달할지도 고민한 프로젝트입니다.

### 화면이 있다는 것과 분석이 유효하다는 것

점수와 추천을 화면으로 보여줄 수 있어도 그 기준이 타당하다는 뜻은 아닙니다. 현재 분석 규칙은 실험적 초안이며, 같은 입력에서 결과가 어떻게 달라지는지와 추천 근거를 더 확인해야 합니다.

화면 테스트에는 고정된 fixture 데이터를 주입하는 경로도 있습니다. 따라서 미리보기 화면의 점수를 실제 사용자 분석 결과나 정확도의 증거로 사용하지 않습니다.

## 코드와 확인 범위

| 내용 | 경로 |
| --- | --- |
| LLM 호출·응답 처리 | [LLM 모듈](backend/app/ai/llm) |
| 추천 생성 | [추천 모듈](backend/app/ai/recommendation) |
| 화면 테스트의 데이터·조건 | [HOS 화면 테스트](frontend/test/hos_page_test.dart) |
| 기존 화면 자료 | [미리보기 모음](frontend/artifacts/previews) |

전체 사용자 흐름의 통합 검증과 분석 기준 정리는 남은 과제입니다. 사람의 성향을 검증된 방법으로 진단하거나 성장 효과를 입증한 서비스는 아닙니다.

## 실행 방법

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

