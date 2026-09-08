# 🧠 MindBuilder

<div align="center">

### AI-powered Personal Thinking Analysis Platform

**사용자의 사고 데이터를 구조화하고,
Pattern · Growth · Identity · Life Map을 거쳐 개인의 Human OS를 만들어가는 분석 플랫폼입니다.**

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge\&logo=sqlalchemy\&logoColor=white)
![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge\&logo=flutter\&logoColor=white)
![OpenRouter](https://img.shields.io/badge/OpenRouter-000000?style=for-the-badge\&logo=openai\&logoColor=white)

</div>

<br>

---

# 📌 Project Overview

**MindBuilder**는 단순히 사용자의 감정이나 성향을 한 번 분석하는 서비스가 아니라,

> **시간이 지날수록 사용자의 사고 데이터를 축적하고
> 변화하는 사고 패턴과 성장 방향을 구조화하는 시스템**

을 목표로 개발하고 있는 개인 프로젝트입니다.

사용자가 온보딩 질문에 답하면 답변을 그대로 LLM에 전달하는 방식이 아니라,

```text
Answer
  ↓
Feature Extraction
  ↓
Pattern Analysis
  ↓
Growth Analysis
  ↓
Identity
  ↓
Life Map
  ↓
Human Operating System
  ↓
Recommendation
```

과 같은 여러 분석 계층을 거쳐 데이터를 점진적으로 구조화합니다.

<br>

---

# 💡 Why MindBuilder?

기존의 자기계발·성향 분석 서비스는 주로

```text
Question
   ↓
AI
   ↓
Result
```

형태의 일회성 분석에 머무르는 경우가 많습니다.

MindBuilder는 사용자 데이터를 장기적으로 다룰 수 있도록
분석 결과 자체도 Database에 구조화하여 저장하고 다음 분석의 근거로 재사용합니다.

```text
User Data
   ↓
Analysis
   ↓
Structured Data
   ↓
Database
   ↓
Next Analysis
   ↓
Updated User Model
```

즉, 분석 결과가 단순한 텍스트 응답으로 끝나는 것이 아니라
다음 분석을 위한 **지속적인 사용자 데이터 모델**의 일부가 되는 것을 목표로 합니다.

<br>

---

# 🧠 Core Analysis Pipeline

## 1. Scan / Onboarding

사용자의 최초 사고 데이터를 수집하는 단계입니다.

```text
Question Set
     ↓
User Answers
     ↓
Scan
     ↓
Database
```

### 주요 기능

* 활성화된 Question Set 조회
* Scan 생성 및 진행 상태 관리
* 객관식 Answer 저장
* 기타 입력 Detail 저장
* 사용자별 Scan 소유권 검증
* 중복 완료 방지

온보딩이 완료되면 이후 분석 Pipeline이 자동으로 시작됩니다.

<br>

---

## 2. Feature Extraction

저장된 답변을 분석에 바로 사용하지 않고
먼저 의미 있는 Feature로 변환합니다.

```text
Raw Answers
     ↓
Option Rules
     +
Cross Rules
     ↓
Feature Extractor
     ↓
Feature Result
```

현재 주요 분석 Feature는 다음과 같습니다.

```text
Future Orientation
Creativity
Execution
Uncertainty
Perfectionism
Resilience
```

단일 문항의 점수뿐 아니라
여러 응답 간 조합을 분석하는 Cross Rule도 적용하여 Pattern의 근거 데이터를 생성합니다.

<br>

---

## 3. Pattern Analysis

Feature Extraction 결과를 기반으로
사용자의 사고 경향을 Pattern으로 구조화합니다.

```text
Feature Result
      ↓
Pattern Analysis
      ↓
Pattern Scores
      +
Insights
      +
Confidence
```

분석 결과는 Database에 저장되고 이후

* Growth
* Identity
* Life Map
* Recommendation
* Human OS

분석에서 다시 사용됩니다.

<br>

---

## 4. Growth Engine

Pattern과 Feature Evidence를 기반으로
사용자의 성장 방향을 세 가지 관점으로 분리합니다.

### Unlearning

현재 성장을 방해할 가능성이 있는 기존 사고 방식이나 행동 패턴을 식별합니다.

### Relearning

기존 능력이나 사고 방식을 새로운 관점에서 다시 활용할 수 있는 방향을 제시합니다.

### Newlearning

현재 Pattern을 기반으로 새롭게 습득하면 도움이 될 행동이나 사고 방식을 제안합니다.

```text
Feature Evidence
      ↓
Growth Engine
      ↓
┌──────────────┐
│  Unlearning  │
├──────────────┤
│  Relearning  │
├──────────────┤
│  Newlearning │
└──────────────┘
```

각 Growth 결과에는

* Title
* Description
* Priority
* Confidence

등을 저장하며, Recommendation과 Next Action으로 이어질 수 있도록 구성했습니다.

<br>

---

## 5. Identity Engine

단일 Scan만으로 Identity를 결정하지 않고,

```text
Current Feature
       +
Latest Pattern
       +
Recent Patterns
       +
Pattern Average
       +
Pattern Trend
       +
Growth Result
```

를 함께 사용하여 현재 Identity를 생성합니다.

### Identity Output

```text
Identity Name
Description
Confidence

Keywords
Strengths
Growth Points

Primary Identity
Secondary Identity
Ranking
Evidence
```

Identity는 Version을 가지고 저장되며
새로운 Identity가 생성될 경우 기존 Identity는 History로 남습니다.

```text
Identity v1
     ↓
Identity v2
     ↓
Identity v3
```

이를 통해 사용자의 Identity가 시간에 따라 어떻게 변화하는지 추적할 수 있도록 설계했습니다.

<br>

---

## 6. Life Map

Pattern · Growth · Identity 정보를 기반으로
사용자의 주요 관심 영역과 목표를 Graph 형태로 구조화합니다.

```text
Pattern
   +
Growth
   +
Identity
   ↓
Life Map Engine
   ↓
Nodes + Edges
```

### Node Types

```text
IDENTITY
INTEREST
GOAL
VALUE
RELATIONSHIP
CAREER
```

각 Node는

* Importance
* Position
* Tags
* Related Goals

등의 데이터를 가질 수 있습니다.

Node 간 관계는 Edge로 저장합니다.

```text
Node A
  │
  │ Edge
  ▼
Node B
```

즉 Life Map은 단순 목록이 아니라
사용자의 관심·가치·목표 간 관계를 표현할 수 있도록 설계했습니다.

<br>

---

# 🌱 Seed Initialization

MindBuilder는 최초 온보딩 분석이 끝나면
사용자의 초기 상태를 **Seed** 단계로 생성합니다.

```text
Onboarding Complete
        ↓
Pattern
        ↓
Growth
        ↓
Identity
        ↓
Data Confidence
        ↓
Life Map
        ↓
Human OS
        ↓
Seed Created
```

Seed 생성 과정에서는

* 완료된 Scan 수
* Answer Coverage
* Feature Coverage
* 추가 서술 데이터

등을 기준으로 Data Confidence를 계산합니다.

최초 Seed가 생성되면 Archive에도 이벤트를 기록하여
사용자의 분석 History 시작점을 남깁니다.

<br>

---

# 🧬 Human Operating System

MindBuilder의 최종 데이터 계층입니다.

**Human OS**는 지금까지 분석한 데이터를 하나의 사용자 모델로 통합합니다.

```text
Pattern
   +
Growth
   +
Identity
   +
Life Map
   ↓
Human Operating System
```

### Human OS

```text
Stage
Data Confidence
Core Values
Thinking Pattern
Decision Pattern
Operating Rules
Version
```

예를 들어 Pattern Score를 기반으로

```text
Execution-led
Creative-led
Future-oriented
Uncertainty-aware
Quality-focused
Resilient
```

등의 Thinking Pattern을 생성합니다.

Decision Pattern 역시

```text
Action-first
Future-first
Balanced
```

형태로 구조화합니다.

<br>

## Human OS Versioning

Human OS는 생성 시점의 분석 데이터를 기반으로 Version을 생성합니다.

```text
Pattern
Identity
LifeMap
Growth
   ↓
OS Version
```

새로운 Human OS가 생성될 경우 기존 OS를 삭제하지 않고 History로 유지합니다.

이를 통해 향후

> **사용자가 어떤 사고 구조에서 어떤 구조로 변화했는가**

를 추적할 수 있도록 설계했습니다.

<br>

---

# 🎯 Recommendation Engine

MindBuilder Recommendation은 단순히 최신 Pattern 하나만 LLM에 전달하지 않습니다.

```text
Pattern
   +
Growth
   +
Identity
   +
Life Map
   ↓
Recommendation Context
   ↓
LLM
   ↓
Recommendation
   ↓
Next Actions
```

분석된 여러 계층의 데이터를 하나의 Context로 구성한 뒤
LLM을 통해 실행 가능한 Recommendation을 생성합니다.

### Output

```text
Recommendation
│
├── Title
├── Description
├── Priority
└── Actions
     ├── Action 1
     ├── Action 2
     └── ...
```

Recommendation Generation 단위로 결과를 저장하여
어떤 Pattern을 기준으로 생성된 추천인지 추적할 수 있도록 구성했습니다.

<br>

---

# 🤖 LLM Architecture

LLM 호출 로직을 특정 기능에 직접 작성하지 않고
별도의 AI Infrastructure 계층으로 분리했습니다.

```text
Application
     ↓
LLM Client
     ↓
Provider
     ↓
OpenRouter
     ↓
LLM
     ↓
Parser
     ↓
Schema Validation
```

### 구성

```text
client.py
config.py
exceptions.py
loader.py
parser.py
retry.py
types.py

providers/
├── base.py
├── openrouter.py
├── huggingface.py
└── transformers.py
```

현재 실제 Provider는 **OpenRouter**를 중심으로 구성되어 있습니다.

기본 모델 설정:

```text
nvidia/nemotron-3-ultra-550b-a55b:free
```

### Generation Profiles

분석 목적에 따라 LLM Parameter를 분리했습니다.

```text
default
recommendation
growth
identity
lifemap
```

각 Profile별로

* Temperature
* Top P
* Max Tokens

를 별도로 관리합니다.

이를 통해 모든 기능이 동일한 LLM 설정을 사용하는 것을 방지하고
분석 목적에 맞게 Generation Strategy를 변경할 수 있도록 구성했습니다.

<br>

---

# 🔁 Hybrid AI Architecture

MindBuilder는 모든 분석을 LLM에 의존하지 않습니다.

```text
Deterministic / Rule Engine
            +
           LLM
            ↓
     Hybrid AI System
```

### Rule / Deterministic 영역

* Feature Extraction
* Cross Rules
* Pattern Analysis
* Growth Rules
* Identity Analysis
* Life Map 구조화
* Human OS 구성

### LLM 활용 영역

* Recommendation Generation
* 자연어 기반 분석 확장
* 구조화된 결과 생성

즉,

> **계산 가능한 데이터는 코드로 처리하고,
> 생성형 판단이 필요한 영역에서 LLM을 활용하는 구조**

를 지향합니다.

<br>

---

# 📊 Dashboard

Backend에서 여러 분석 결과를 하나의 Dashboard Response로 통합합니다.

### Dashboard Data

```text
Human OS
Data Confidence
Latest Insight
Next Action
Recent Pattern Changes
Recent Archive Events
```

최근 Pattern과 이전 Pattern을 비교하여

```text
Execution
Future Orientation
Creativity
Perfectionism
```

등의 변화량도 계산합니다.

Flutter에서는 이 통합 API를 이용해
사용자가 자신의 현재 상태를 한 화면에서 확인할 수 있도록 구성했습니다.

<br>

---

# 🗂️ Archive

사용자의 중요한 분석 이벤트를 Archive로 기록합니다.

예:

```text
Seed Created
Operating System Generated
Analysis Events
```

Archive는 단순 로그가 아니라

```text
event_type
reference_id
title
summary
created_at
```

형태의 Domain Event로 저장됩니다.

이를 통해 장기적으로 사용자의 변화 History를 구성하는 기반으로 사용합니다.

<br>

---

# 🔐 Authentication

MindBuilder는 OAuth Account 기반 사용자 인증 구조를 사용합니다.

```text
OAuth Login
     ↓
Find / Create User
     ↓
OAuth Account
     ↓
Access Token
     +
Refresh Token
```

### Features

* OAuth 기반 사용자 생성 / 로그인
* Access Token
* Refresh Token
* Token Refresh
* 사용자 Profile 조회
* Nickname 변경
* Profile Image 변경
* 사용자 Data Export
* 회원 탈퇴

JWT의 `sub`에는 User ID를 저장하여
보호된 API에서 현재 사용자를 식별합니다.

<br>

---

# 📱 Flutter Client

MindBuilder는 Backend뿐 아니라
Flutter Mobile Client도 함께 개발하고 있습니다.

### Stack

![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge\&logo=flutter\&logoColor=white)
![Dart](https://img.shields.io/badge/Dart-0175C2?style=for-the-badge\&logo=dart\&logoColor=white)

```text
Riverpod
Dio
GoRouter
Google Sign-In
Flutter Secure Storage
Flutter DotEnv
```

### 주요 Feature

```text
Splash
Auth
Onboarding
Dashboard
Analysis
```

<br>

## Flutter Architecture

Frontend 역시 기능 단위로 구조를 분리했습니다.

```text
lib/
│
├── app/
│
├── core/
│   ├── config/
│   ├── network/
│   ├── routes/
│   ├── storage/
│   └── theme/
│
└── features/
    ├── auth/
    │   ├── application/
    │   ├── data/
    │   └── presentation/
    │
    ├── onboarding/
    ├── dashboard/
    ├── analysis/
    └── splash/
```

Auth와 Dashboard 등 주요 Feature는

```text
Application
Data
Presentation
```

레이어를 분리하여 관리합니다.

<br>

---

# 🏗️ Backend Architecture

Backend는 분석 로직과 Database 접근 로직이 직접 결합되지 않도록
여러 계층으로 분리했습니다.

```text
API Router
    ↓
Service
    ↓
AI Engine
    │
    └─────────────┐
                  │
Repository       LLM
    ↓             │
SQLAlchemy        │
    ↓             │
PostgreSQL ◀──────┘
```

### Responsibility

```text
api/routers/
    HTTP Request / Response

services/
    Application Business Logic

ai/
    Analysis Engine / LLM

repositories/
    Database Access

models/
    SQLAlchemy ORM

schemas/
    Pydantic Request / Response

core/
    Config / Database / Security
```

<br>

---

# 📂 Project Structure

```text
MindBuilder/
│
├── backend/
│   │
│   ├── alembic/
│   │   └── versions/
│   │
│   ├── app/
│   │   │
│   │   ├── ai/
│   │   │   ├── feature_extractor/
│   │   │   ├── growth/
│   │   │   ├── identity/
│   │   │   ├── lifemap/
│   │   │   ├── llm/
│   │   │   └── recommendation/
│   │   │
│   │   ├── api/
│   │   │   └── routers/
│   │   │
│   │   ├── features/
│   │   │   └── auth/
│   │   │
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── alembic.ini
│
└── frontend/
    │
    ├── lib/
    │   ├── app/
    │   ├── core/
    │   ├── features/
    │   └── main.dart
    │
    └── pubspec.yaml
```

<br>

---

# 🗄️ Database

Main Database는 **PostgreSQL**을 사용합니다.

Backend Application에서는

```text
SQLAlchemy AsyncSession
        +
      asyncpg
```

를 사용하고,

Migration은

```text
Alembic
   +
psycopg2
```

조합으로 관리합니다.

### 주요 Domain

```text
User / OAuth

Question / Answer / Scan

Feature / Pattern / Insight

Growth / Recommendation / Next Action

Identity

Life Map / Node / Edge / Goal / Tag

Operating System

Data Confidence

Archive
```

분석 데이터를 하나의 JSON 컬럼에 모두 저장하는 방식보다
각 Domain을 관계형 데이터로 분리하여 저장하는 구조를 사용했습니다.

<br>

---

# ⚙️ Tech Stack

## Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)

`Pydantic` `JWT` `Async API`

<br>

## Database

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge\&logo=sqlalchemy\&logoColor=white)

`SQLAlchemy 2.0` `AsyncSession` `asyncpg` `Alembic`

<br>

## AI / LLM

![OpenAI SDK](https://img.shields.io/badge/OpenAI%20SDK-412991?style=for-the-badge\&logo=openai\&logoColor=white)

`OpenRouter`
`Nemotron`
`Rule-based Engine`
`Structured Output`
`Pydantic Validation`
`Retry / Error Handling`

<br>

## Client

![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge\&logo=flutter\&logoColor=white)
![Dart](https://img.shields.io/badge/Dart-0175C2?style=for-the-badge\&logo=dart\&logoColor=white)

`Riverpod` `Dio` `GoRouter` `Secure Storage`

<br>

---

# 📡 Main API Domains

FastAPI에서 기능별 Router를 분리했습니다.

```text
/auth
/api/v1/onboarding
/api/v1/pattern
/api/v1/growth
/api/v1/identity
/api/v1/lifemap
/api/v1/recommendations
/api/v1/operating-system
/api/v1/archive
/api/v1/dashboard
```

System 상태 확인:

```http
GET /health
```

FastAPI Swagger:

```text
http://localhost:8000/docs
```

<br>

---

# 🔐 Environment Variables

## Backend

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

<br>

---

# 🚀 Getting Started

## Backend

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

<br>

## Frontend

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

<br>

---

# 🔄 Current Core Flow

현재 Repository에 구현된 주요 흐름은 다음과 같습니다.

```text
OAuth Login
      ↓
Onboarding
      ↓
Question / Answer
      ↓
Scan Completed
      ↓
Feature Extraction
      ↓
Pattern Analysis
      ↓
Growth Analysis
      ↓
Identity Generation
      ↓
Seed Initialization
      ↓
Life Map
      ↓
Human Operating System
      ↓
Dashboard
      ↓
Recommendation
```

<br>

---

# 🎯 What I Focused On

MindBuilder를 개발하면서 가장 중점적으로 다룬 부분은
**LLM 호출 자체보다 AI 기능을 하나의 Backend System 안에서 어떻게 구조화할 것인가**였습니다.

특히 다음 내용을 직접 설계하고 구현했습니다.

* FastAPI 기반 Backend Architecture
* PostgreSQL 관계형 Data Modeling
* SQLAlchemy Repository Pattern
* Alembic Database Migration
* Async Database Flow
* Rule-based Feature Extraction
* Pattern Analysis Engine
* Unlearning / Relearning / Newlearning Growth Model
* Versioned Identity Model
* Graph 기반 Life Map
* Human Operating System Data Model
* Data Confidence
* Seed Initialization
* LLM Provider Abstraction
* Structured LLM Output Validation
* Recommendation Generation
* Archive Event History
* Dashboard Aggregation
* JWT Access / Refresh Token
* Flutter ↔ Backend API Integration
* Riverpod / Dio / GoRouter 기반 Flutter 구조

<br>

---

# 🧭 Development Direction

MindBuilder의 장기적인 방향은

```text
Single Analysis
      ↓
Repeated Scans
      ↓
Long-term Pattern
      ↓
Identity Changes
      ↓
Life Structure
      ↓
Human Operating System
```

입니다.

사용자가 서비스를 오래 사용할수록 데이터가 쌓이고,

**“현재 나는 어떤 사람인가?”**

뿐만 아니라

**“나는 어떤 방향으로 변화하고 있는가?”**

까지 보여줄 수 있는 시스템으로 발전시키는 것을 목표로 하고 있습니다.

<br>

---

# 👨‍💻 Developer

**엄인섭**

GitHub
https://github.com/EddieEom
