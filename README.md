<div align="center">

# MindBuilder

**생각을 기록하고 다음 행동의 방향을 찾는 개인 프로토타입**

</div>

<p align="center"><img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=flat-square"/> <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square"/> <img alt="Flutter" src="https://img.shields.io/badge/Flutter-02569B?style=flat-square"/> <img alt="OpenRouter" src="https://img.shields.io/badge/OpenRouter-222222?style=flat-square"/></p>


| 형태 | 목표 | 구성 범위 |
| :--- | :--- | :--- |
| **개인 프로토타입** | 생각 정리 · 행동 방향 탐색 | 앱 · API · DB · LLM 연동 구조 |

## 🧠 프로젝트에서 구성한 내용

<table><tr>
<td width="33%" valign="top"><b>입력과 기록</b><br><br>Flutter 질문 입력<br>답변 데이터 저장<br>사용자별 데이터 관리 구조</td>
<td width="33%" valign="top"><b>분석 구조</b><br><br>점수 · 규칙 기반 처리<br>단계별 분석 결과 구성<br>결과 저장 구조</td>
<td width="33%" valign="top"><b>결과와 추천</b><br><br>LLM API 연결<br>추천 문장 생성<br>분석 결과 화면 구성</td>
</tr></table>

생각은 많지만 무엇부터 실행해야 할지 정하기 어려웠던 경험에서 출발했습니다. 기획과 앱·서버 구성을 개인으로 진행했으며, 분석 규칙과 점수 초안에는 생성형 AI를 활용했습니다.

## 주요 구성

| 영역 | 구성 내용 |
| --- | --- |
| 앱 | Flutter 기반 질문 입력 및 분석 결과 화면 |
| API | FastAPI 기반 사용자·답변·분석 결과 처리 |
| DB | PostgreSQL·SQLAlchemy·Alembic을 활용한 저장 구조 |
| 분석 | 답변을 점수와 규칙으로 처리하고 결과를 단계별로 구성 |
| LLM | OpenRouter를 통한 모델 호출과 추천 문장 생성 |


<details>
<summary><b>📝 개발 상태 · 다음 과제</b></summary>

## 개발 상태와 다음 과제

현재는 기능 구성과 연동을 시도한 프로토타입 단계입니다. 전체 사용자 흐름의 통합 검증과 분석 규칙의 근거 정리를 다음 과제로 두고 있습니다.

- 로그인 → 질문 응답 → 분석 → 결과 조회 흐름 점검
- 분석 규칙과 점수 산정 기준 정리
- 동일 입력 및 오류 상황에 대한 결과 기록

코드의 `Feature`, `Pattern`, `Growth`, `Identity`, `Life Map`, `Human OS`는 내부 기능 구분에 사용하는 이름입니다. 분석 결과는 자기 탐색을 위한 실험적 출력입니다.

</details>

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

