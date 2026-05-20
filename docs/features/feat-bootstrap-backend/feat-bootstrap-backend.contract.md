---
doc_type: feature-contract
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: feature
related:
  R-ID: [R-N-01, R-N-04, R-N-05, R-N-06]
  F-ID: []
  supersedes: null
---

# feat-bootstrap-backend — Change Contract

> Issue #1 — backend/ 부팅 골격 정의. §0 Referenced-IDs는 P4 selective read 진입점 (ADR-0018).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — Referenced-IDs + Before/After + Call Sites + Rollback |

## 0. 참조 정본 ID (Referenced-IDs)

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| R-ID (SRS 비기능) | `docs/planning/04-srs/04-srs.md` | R-N-01 (성능 p95), R-N-04 (Python 강제), R-N-05 (단위/통합 테스트 80%), R-N-06 (단일 환경 운영) |
| F-ID (PRD 기능) | `docs/planning/05-prd/05-prd.md` | (none) — 본 이슈는 인프라/스캐폴딩, 사용자 기능 미포함 |
| ADR (의사 결정) | `docs/planning/adr/` | ADR-0001 (FastAPI), ADR-0003 (SQLite), ADR-0037 (부팅 자산 + 단일 환경 N/A), ADR-0040 (LOCAL.md 양축) |
| Architecture | `docs/planning/06-architecture/06-architecture.md` | §Stack Decision 표 (Python 3.11 + FastAPI + SQLAlchemy 2.x + SQLite + uv) |
| HLD | `docs/planning/07-hld/07-hld.md` | §1 핵심 모듈 표 (M-API-Router, M-Auth-Middleware는 후속 이슈) |
| LLD module-spec | `docs/planning/08-lld-module-spec/08-lld-module-spec.md` | (전체 §0 — 모듈 등장 전 베이스라인 스캐폴딩) |
| Scaffolding | `docs/planning/12-scaffolding/python.md` | §3 디렉토리 트리, §5 빌드·실행, §6 환경 변수, §7 부팅 자산 |
| LOCAL.md (boot 정본 양축) | 루트 `LOCAL.md` | §3.1 dev profile 부팅 명령 |

## 1. 변경 의도

빈 `backend/` 디렉토리 → FastAPI 부팅 가능한 최소 골격으로 채운다. 후속 이슈(#2 User 모델 ~ #6 Comment)가 의존하는 부팅 자산(`pyproject.toml`, `uv.lock`, `alembic`, `.env.example`, FastAPI app)을 단일 PR로 일괄 작성한다. 본 이슈는 사용자 기능 0개 — health check 1개만 노출. 후속 이슈에서 router/service/model 추가 시 본 골격의 import 진입점(`realworld.main`, `realworld.config`, `realworld.db`)을 재사용한다.

## 2. Before / After

| 항목 | Before | After |
| --- | --- | --- |
| backend/ 디렉토리 | 존재하지 않음 | 존재함 (pyproject.toml + realworld/ + alembic/ + tests/) |
| Python 패키지 | (없음) | `realworld` (FastAPI app + config + db) |
| 의존성 lock | (없음) | `backend/uv.lock` 생성 (재현 가능 설치) |
| FastAPI app 인스턴스 | (없음) | `realworld.main:app` — 단일 ASGI app 객체 |
| HTTP 엔드포인트 | (없음) | `GET /health` → `{"status": "ok"}` (200) |
| OpenAPI 문서 | (없음) | `GET /docs` → Swagger UI (FastAPI 기본) |
| DB 엔진 | (없음) | `AsyncEngine` 인스턴스 (aiosqlite, file://./realworld.db) |
| Session factory | (없음) | `async_sessionmaker[AsyncSession]` (의존성 주입용) |
| 마이그레이션 | (없음) | Alembic init 1건 (`0001_initial.py`, 빈 upgrade/downgrade) |
| 환경 변수 | (없음) | `.env.example`에 4종 (DATABASE_URL, JWT_SECRET, JWT_ALG, JWT_EXPIRE_MINUTES) |
| 부팅 명령 (LOCAL.md §3.1) | 미검증 | 실제 8000 포트 부팅 + `/docs` 응답 확인 |
| pytest 셋업 | (없음) | conftest.py + 1건 통합 테스트 (health check) |
| Lint/Format | (없음) | ruff (lint + format) + pre-commit 훅 |
| GitHub Actions | (없음) | `backend-ci.yml` — push/PR 트리거, uv sync + ruff + pytest |
| .gitignore | (toolkit 기본) | + `backend/.env`, `backend/.venv/`, `backend/__pycache__/`, `*.db` |

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| `realworld.main:app` | 후속 이슈(#3 인증, #4 users/articles router, #6 comments router)가 `app.include_router(...)`로 마운트 | router stub은 작성하지 않음. 후속 이슈가 자유롭게 추가 |
| `realworld.config:Settings` | 후속 이슈(#3 JWT)가 `Settings.JWT_SECRET` 등 참조 | BaseSettings 인터페이스 안정화. 환경 변수명 4종 고정 |
| `realworld.db:async_session_maker` | 후속 이슈(#2~#6 repo·service)가 `Depends(get_db)`로 주입 | `get_db()` async generator 표준 제공 |
| `backend/.env.example` | 후속 이슈가 새 환경 변수 추가 시 본 파일 갱신 | ADR-0037 부팅 자산 동기 강제 — 본 PR이 첫 baseline |
| `backend/alembic/versions/0001_initial.py` | 후속 이슈(#2 User, #6 Comment)가 새 revision을 `down_revision="0001"`로 연결 | revision id "0001" 고정 |
| LOCAL.md §3.1 | 매 PR 부팅 자산 변경 시 동기 갱신 (ADR-0040) | 본 PR이 §3.1 첫 검증 완료 시점 |
| `.github/workflows/backend-ci.yml` | 후속 이슈의 PR마다 자동 트리거 | uv sync + ruff + pytest 표준 진입점 확보 |

**파생 이슈 추적**: 없음 (본 이슈는 NEW_PROJECT 첫 작업).

## 4. Backward Compatibility

- **신규 디렉토리·파일만 생성** — 기존 코드 0줄 (backend/는 빈 상태). breaking change 없음.
- **루트 파일 수정**:
  - `LOCAL.md` §3.1: 부팅 명령 실 검증 결과 반영 (구문 변경 없음, 명령 자체는 기존 placeholder와 동일 의도)
  - `.gitignore`: 신규 패턴 추가만 (기존 패턴 제거 없음)
- **GitHub Actions 워크플로 추가**: 신규 `.github/workflows/backend-ci.yml`만. 기존 워크플로 없음 (사용자가 newProject 시 ADR-0047 확장).

## 5. Rollback 전략

- **Git revert**: 단일 PR 머지로 모든 변경 squash 통합. 문제 시 `git revert <merge-sha>` 1회로 backend/ 전체 + 루트 수정 모두 회귀.
- **DB rollback**: SQLite 파일(`backend/realworld.db`) 삭제로 즉시 초기화. Alembic은 빈 init만 등록되어 데이터 손실 없음.
- **외부 의존성 rollback**: uv.lock 삭제 + `uv sync`로 재현. 의존성 버전 핀은 pyproject.toml에 명시.
- **부팅 실패 시**: LOCAL.md §3.1 명령 실행 결과 stderr를 PR 코멘트로 남기고 `status:blocked` 라벨 부착 후 사용자 확인.
- **CI 실패 영구화 위험**: backend-ci.yml이 main 브랜치 status check로 요구되지 않은 상태로 PR 머지 → main에서 첫 실패. 본 PR 머지 후 사용자가 GitHub branch protection에 `backend-ci`를 required로 등록 (ADR-0044 branch protection 9개 규칙 적용 단계).

## 6. 비목표

- **사용자 기능 (회원가입·로그인·게시글 CRUD)**: Issue #2~#6 책임. 본 PR은 health check 1개만.
- **User/Article/Comment 모델 정의 + 마이그레이션 본문**: Issue #2(User), #6(Comment) 책임.
- **인증 미들웨어, JWT util**: Issue #3 책임.
- **dev/stg/prod 3 profile**: RFP §NFR-06 단일 환경 운영으로 N/A. ADR-0037 v1.1 §"단일 환경 운영" 사유 명시 적용.
- **프론트엔드 (Vite + React)**: Issue #7 책임.
- **seed 스크립트, p95 성능 테스트**: Issue #5 (P2 cut 후보).
- **OpenAPI tag 그룹화, 응답 schema 표준화**: 후속 이슈 또는 별도 modify 이슈.
