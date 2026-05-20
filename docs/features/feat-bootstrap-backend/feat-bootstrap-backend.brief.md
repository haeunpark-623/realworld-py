---
doc_type: feature-brief
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: feature
related:
  R-ID: []
  F-ID: []
  supersedes: null
---

# feat-bootstrap-backend — Feature Brief

> Issue #1 — `chore(backend): I-01 스캐폴딩 + DB + 환경설정`. backend/ 빈 디렉토리 → FastAPI 부팅 가능 + Alembic + SQLite 기본 골격 완성.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — Issue #1 의도·범위·비목표 정의 |

## 1. 한 줄 의도

Python FastAPI + SQLAlchemy 2.x async + Alembic + SQLite + uv 기반 백엔드 부팅 골격을 단일 PR로 완성한다 (모든 후속 백엔드 이슈의 전제).

## 2. 사용자 가치

- **개발자 (Sprint 작업자)**: fresh checkout 후 `uv sync && uv run alembic upgrade head && uv run uvicorn realworld.main:app --reload` 1회로 8000 포트에 부팅, `/docs` Swagger UI 확인 가능. 후속 이슈(#2~#6) 작업 시 환경 셋업 재작업 0건.
- **팀장/리뷰어**: LOCAL.md §3.1 부팅 명령으로 5분 이내 로컬 재현 가능. DoD 항목별로 부팅 자산 동기성 검증 가능.
- **CI**: GitHub Actions에서 pytest 워크플로가 동일 명령으로 부팅·테스트할 수 있는 표준 진입점 확보.

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 | 변경 후 |
| --- | --- | --- |
| backend/ 디렉토리 | 존재하지 않음 | `backend/realworld/` 패키지 + 설정 + DB + 마이그레이션 폴더 |
| 의존성 관리 | 없음 | `backend/pyproject.toml` + `backend/uv.lock` (uv 기반) |
| FastAPI 앱 | 없음 | `realworld/main.py` — FastAPI 인스턴스 1개 + `/health` 엔드포인트 + lifespan |
| 설정 | 없음 | `realworld/config.py` — `pydantic-settings.BaseSettings` (DATABASE_URL, JWT_SECRET 등) |
| DB 엔진 | 없음 | `realworld/db.py` — `AsyncEngine` + `async_sessionmaker` (aiosqlite 드라이버) |
| 마이그레이션 | 없음 | `backend/alembic.ini` + `backend/alembic/env.py` + `backend/alembic/versions/0001_initial.py` (빈 init) |
| 환경 변수 템플릿 | 없음 | `backend/.env.example` (DATABASE_URL, JWT_SECRET, JWT_ALG, JWT_EXPIRE_MINUTES) |
| 부팅 가이드 | LOCAL.md §3.1 명령 미검증 | LOCAL.md §3.1 명령이 실제 실행 가능 (8000 포트 부팅 + Swagger UI) |
| pre-commit | 없음 | `.pre-commit-config.yaml` + ruff (lint/format) 훅 |

## 4. 모드 자동 감지 결과

- 라벨: `type:chore`, `area:backend`, `priority:P0`, `status:in-progress` (P-1에서 전이)
- 부정 시그널 검사 (ADR-0032):
  - `type:bug` 라벨? **없음**
  - UI/design 키워드? **없음** (백엔드 스캐폴딩)
  - 기존 동작 변경/breaking? **없음** (빈 디렉토리 → 신규)
- 부정 시그널 합계: **0건** → **mode=add** 자동 결정 (질문 없이 진행)
- 모드별 강조: 산출 강제 `docs/features/feat-bootstrap-backend/feat-bootstrap-backend.{brief,contract,plan}.md` + 최소 침습 원칙. UI 영향 없음 → `/ux-flow-design` skip. `/ui-design-review` skip.

## 5. 영향 범위

**신규 생성 (backend/ 내부)**:
- `backend/pyproject.toml` (uv project metadata, 의존성)
- `backend/uv.lock` (uv sync 자동 생성)
- `backend/realworld/__init__.py` (빈 패키지 marker)
- `backend/realworld/main.py` (FastAPI app + health check)
- `backend/realworld/config.py` (pydantic-settings BaseSettings)
- `backend/realworld/db.py` (AsyncEngine + Session factory)
- `backend/.env.example` (환경 변수 템플릿)
- `backend/alembic.ini` (Alembic 설정)
- `backend/alembic/env.py` (Alembic 환경 — async)
- `backend/alembic/script.py.mako` (Alembic 자동 생성)
- `backend/alembic/versions/0001_initial.py` (빈 init revision)
- `backend/tests/__init__.py`
- `backend/tests/conftest.py` (pytest fixture — TestClient, async session)
- `backend/tests/test_health.py` (health check 통합 테스트)

**신규 생성 (루트)**:
- `.pre-commit-config.yaml` (ruff lint/format)
- `.github/workflows/backend-ci.yml` (pytest 워크플로)

**기존 수정**:
- `LOCAL.md` §3.1 (부팅 명령 검증 후 갱신, ADR-0040)
- `.gitignore` (`backend/.env`, `backend/.venv/`, `backend/__pycache__/`, `backend/realworld.db` 등 추가)

**설계 문서 fan-out 영향 (P13에서 갱신)**:
- `docs/planning/12-scaffolding/python.md` §5 빌드·실행 (실 명령 확정)
- `docs/planning/12-scaffolding/python.md` §7 부팅 자산 (실 파일 매핑)

## 6. 비목표

- **API 엔드포인트 구현 (POST /users 등)** → Issue #4 책임. 본 이슈는 **health check 1개**만.
- **User/Article/Comment 모델 정의** → Issue #2(User), #6(Comment) 책임. 본 이슈는 **빈 init migration**만.
- **인증 미들웨어** → Issue #3 책임.
- **dev/stg/prod 3 profile** → RFP §NFR-06 단일 환경 운영(dev 1 profile)이므로 N/A. ADR-0037 v1.1 §"단일 환경 운영" N/A 명시 적용.
- **프론트엔드 스캐폴딩** → Issue #7 책임.
- **seed 스크립트, p95 통합 테스트** → Issue #5 (P2 cut 후보).

## 7. Open Questions

- (없음) — Gate B에서 7개 Open Q 모두 확정 완료. 본 이슈에서 추가 결정 사항 없음.
