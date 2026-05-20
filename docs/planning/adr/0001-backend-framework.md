---
doc_type: adr
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: [R-N-01, R-N-04, R-N-06]
  F-ID: [F-01, F-02, F-03]
  supersedes: null
---

# ADR 0001 — 백엔드 프레임워크 FastAPI 채택

- **상태**: Draft
- **결정일**: 2026-05-20
- **작성**: 박하은 <woosung.ahn@bespinglobal.com>

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — 게이트 B(v0.2)에서 사용자 결정, 게이트 C에서 ADR로 정식화 |

## 1. 컨텍스트

본 프로젝트는 RFP §NFR-01에 따라 *백엔드 언어 Python 필수* 제약이 있다. 프레임워크는 게이트 C에서 결정. 후보 3종 — FastAPI / Django / Flask. 다음 컨텍스트가 결정에 영향:

- **2일 마감 + 1인 뉴비 학습 컨텍스트** — 학습 곡선이 가장 큰 결정 요인
- **05-prd에서 SPA(React+Vite) 채택 결정** — REST API 친화도가 중요
- **09-lld-api-spec이 OpenAPI 형식** — 자동 생성 가능 여부가 산출 부담에 직접 영향
- **R-N-06 단위 테스트 ≥ 80%** — 서비스·라우터 분리 용이성
- **R-N-04 시크릿 환경변수** — pydantic-settings 같은 표준 도구가 있으면 학습 부담 감소

## 2. 결정

**FastAPI** 채택. 본 결정은 게이트 B(v0.2 Open Q §2)에서 사용자가 사전 결정했고, 본 ADR로 정식화한다.

채택 효과:
- `realworld.main:app = FastAPI(...)` 인스턴스 1개를 진입점으로 라우터 3개(`users_router`, `articles_router`, `comments_router`) 등록
- Pydantic BaseModel로 모든 요청·응답 스키마 정의 → 검증·직렬화 자동
- OpenAPI 스펙 자동 생성 (`GET /docs` Swagger UI) → 09-lld-api-spec 수동 작성 부담 감소
- `Depends()` dependency injection으로 `require_auth`, `require_author`, `get_db` 등을 라우터에 주입
- `async def` 비동기 핸들러 + SQLAlchemy AsyncSession 조합

## 3. 검토된 대안

### 채택안: FastAPI

- **장점**:
  - Pydantic 자동 검증 + OpenAPI 자동 생성 — 09-api-spec 산출 부담 최소
  - SPA(REST) 친화 — 본 프로젝트 컨텍스트 최적
  - 학습 곡선 완만 — 공식 튜토리얼이 1~2일 완주 가능 분량
  - 비동기 지원 native — SQLAlchemy AsyncSession과 자연 결합
  - 풍부한 RealWorld spec 구현 레퍼런스 (FastAPI 버전 다수 공개)
  - 단위·통합 테스트가 `TestClient`/`httpx.AsyncClient`로 깔끔
- **단점**:
  - Django 대비 admin·ORM·인증 통합 도구 없음 — 직접 조립
  - Flask 대비 학습 자료가 약간 적음 (다만 충분)
  - SQLAlchemy 2.x async API가 비교적 신생 → 일부 패턴 자료 부족 가능

### 대안 1: Django (+ Django REST Framework)

- **장점**:
  - admin 자동 생성, ORM·인증·세션 통합
  - 한국어 학습 자료 풍부
  - 정통 Python 웹 프레임워크 학습 효과
- **단점 (불채택 이유)**:
  - 컴포넌트가 모두 패키지로 묶여 있어 *학습 진입 비용*이 FastAPI보다 큼 — 2일 마감 부담
  - REST API + SPA는 DRF 추가 학습 필요 (FastAPI는 native)
  - Pydantic 같은 자동 OpenAPI 생성 부재 → 09-api-spec 수동 분량 증가
  - 비동기 native 지원이 약함 (3.x에서 부분 지원)
  - 본 MVP 규모(9 모듈)에서 admin·ORM·인증 통합이 *과대*

### 대안 2: Flask (+ Flask-RESTful + Flask-JWT-Extended)

- **장점**:
  - 가장 가벼움 — 학습 진입 비용 낮음
  - 풍부한 학습 자료
  - 자유도 높음 (조립 직접)
- **단점 (불채택 이유)**:
  - Pydantic 자동 검증 부재 — 검증·직렬화 코드를 모두 직접 작성
  - OpenAPI 자동 생성 부재 — 09-api-spec 수동 분량 최대
  - 비동기 native 부재 — async 학습 효과 누락
  - 작은 모듈을 모두 직접 조립 → 학습 효과는 좋으나 2일 마감 부담
  - "조립의 자유"는 뉴비에게 *결정 부담*으로 작용

## 4. 결과 (Consequences)

### 긍정

- Pydantic + OpenAPI 자동 생성으로 09-api-spec 산출 부담 감소
- TestClient + httpx로 통합 테스트 작성이 간결
- SPA(React) 컨텍스트와 자연 결합 — CORS 1개 설정으로 끝
- FastAPI 공식 문서·튜토리얼이 뉴비에게 친화적

### 부정 / 트레이드오프

- Django admin 같은 *공짜* 도구 없음 — 게시글 100건 시드는 별 스크립트(`scripts/seed_articles.py`) 작성
- Django ORM 대비 SQLAlchemy 2.x async API 학습 부담 — 일부 마이그레이션 패턴 자료 부족
- Django 인증 통합 부재 — passlib + pyjwt 직접 조립

### 영향 받는 문서

- 06-architecture §Stack Decision (Python 3.11 + FastAPI 명시)
- 07-hld §1·§2 (모듈 분해와 데이터 흐름은 FastAPI 라우터·dependency 패턴 가정)
- 08-lld-module-spec 전체 (FastAPI APIRouter, Depends, exception_handlers 가정)
- 09-lld-api-spec 전체 (RealWorld spec + FastAPI OpenAPI 결합)
- 11-coding-conventions §1·§3 (Python 명명 + 관용구 + Pydantic 명명)
- 12-scaffolding/python.md 전체 (디렉토리 트리·uv·alembic·부팅 명령)
- 13-test-design/01-strategy + 02-catalog (pytest + httpx + TestClient 가정)
- LOCAL.md §3 (uvicorn 부팅 명령)

## 5. 추적 / 재검토 시점

- **재검토 트리거**: 사이클 완주 후 회고(`/retro` 2026-05-22)에서 학습 만족도·구현 난이도 평가. 향후 후속 학습 과제(`realworld-py-v2` 등)에서 Django로 재도전 결정 가능.
- **GitHub Issue 라벨**: 본 결정 변경 시 `decision:reverse` 라벨 사용 — 본 ADR을 `status: Superseded`로 변경 + 신규 ADR 발행.
- **재검토 주기**: 본 학습 과제 1회성. 재검토 의무 없음.
