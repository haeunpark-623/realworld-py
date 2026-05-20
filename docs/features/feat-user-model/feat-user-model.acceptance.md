---
doc_type: feature-acceptance
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: feature
related:
  R-ID: [R-F-01, R-N-03, R-N-04]
  F-ID: [F-01]
  supersedes: null
---

# feat-user-model — Acceptance Criteria

> Issue #2. 6 AC + 5 DoD. P10 AI 게이트가 AC 자동 검증, P14 휴먼 게이트가 DoD 사람 검증.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — Given/When/Then 6건 + DoD 5건 + 비기능·회귀 |

## 1. 인수 기준 (Given/When/Then)

### AC-01: User 모델 import + Base.metadata 등록
- **Given** I-01 backend 스캐폴딩 머지 후 본 PR 적용 상태
- **When** `cd backend && uv run python -c "from realworld.models import Base, User; print(sorted(Base.metadata.tables.keys()))"` 실행
- **Then** stdout에 `['users']` 출력 + exit 0

### AC-02: Alembic 0002 revision 생성 + head 정합
- **Given** 본 PR 머지된 상태
- **When** `cd backend && uv run alembic upgrade head && uv run alembic current` 실행
- **Then** `0002 (head)` 출력 + exit 0. `data/realworld.db` 파일에 `users` 테이블 존재 (`sqlite3 data/realworld.db ".schema users"`로 확인)

### AC-03: users 테이블 컬럼 정합
- **Given** alembic upgrade head 완료된 dev DB
- **When** SQLite `PRAGMA table_info(users)` 또는 `.schema users` 실행
- **Then** 5 컬럼 모두 존재: `id INTEGER PRIMARY KEY` / `username TEXT NOT NULL UNIQUE` / `email TEXT NOT NULL UNIQUE` / `password_hash TEXT NOT NULL` / `created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP (또는 server_default 표현)`

### AC-04: UserRepo 3 메서드 시그니처
- **Given** 본 PR 머지된 상태
- **When** `cd backend && uv run python -c "import inspect; from realworld.repositories.user import UserRepo; print([m for m in dir(UserRepo) if not m.startswith('_')])"` 실행
- **Then** 출력에 `find_by_email`, `find_by_username`, `create` 3 메서드 포함. 각각 async 함수 (`inspect.iscoroutinefunction` True)

### AC-05: pytest 단위 테스트 3 PASS
- **Given** 본 PR 머지된 상태
- **When** `cd backend && uv run pytest tests/unit/test_user_repo.py -v` 실행
- **Then** `3 passed` + exit 0. 케이스: `test_create_user_persists`, `test_find_by_email_returns_existing`, `test_find_by_username_returns_none_for_unknown`

### AC-06: 회귀 — 기존 health 테스트 무영향
- **Given** 본 PR 머지된 상태
- **When** `cd backend && uv run pytest -v` 실행 (전체)
- **Then** `6 passed` (3 health + 3 user_repo) + exit 0. health 테스트 회귀 0건

## 2. Definition of Done (D-06)

본 8 DoD 항목은 Issue #2 body의 5 DoD checklist + 본 PR 표준 3 (ruff·tests·CI) 일치. P14 휴먼 게이트에서 사람이 미체크 → 체크로 전환.

- [ ] D-02-1 `models/user.py` declarative 클래스 (SQLAlchemy 2.0 typed Mapped)
- [ ] D-02-2 `alembic revision --autogenerate -m "add users"` + `0002_add_users.py` commit
- [ ] D-02-3 `repositories/user.py` 3 메서드 (`find_by_email`, `find_by_username`, `create`)
- [ ] D-02-4 `tests/unit/test_user_repo.py` 3 케이스 PASS
- [ ] D-02-5 `alembic upgrade head` 실행 후 DB 스키마 확인 (5 컬럼 + 2 UNIQUE)
- [ ] D-02-6 ruff check + format PASS (pre-commit 훅 자동)
- [ ] D-02-7 pytest 전체 6 PASS (3 health 회귀 0건)
- [ ] D-02-8 GitHub Actions `backend-ci` workflow green (lint + pytest 5 step)

## 3. 비기능 인수

- **R-N-03 bcrypt 슬롯**: 본 PR은 `password_hash: Mapped[str]` 컬럼 TEXT 슬롯만 제공. 실제 bcrypt 해시는 I-03 책임 — *형식 검증 없음* (slot only). RFP §NFR-04 단위 적용은 I-03 통합 확인.
- **R-N-04 시크릿 환경변수**: 본 PR은 `JWT_SECRET` 변경 없음 (I-01에서 이미 .env.example 등록). DATABASE_URL은 `config.py::get_settings`로 환경 변수 주입. 단위 테스트 fixture는 in-memory aiosqlite로 별도 URL 사용 (실제 DB 분리).
- **R-N-06 단일 환경 운영**: dev 1 profile만. stg/prod N/A (RFP §NFR-06).
- **보안**: 마이그레이션 0002 파일에 비밀번호 평문 / API 키 / JWT secret 0건. password_hash 컬럼명만 등장.

## 4. 회귀 인수

- **기존 3 health 테스트** (`tests/test_health.py`): 본 PR 머지 후 PASS 유지. pytest collection이 `tests/` 평면 + `tests/unit/` 하위 모두 자동 발견 (pytest 기본 동작).
- **기존 alembic 0001 init revision**: 본 PR 0002가 `down_revision="0001"` 체이닝. `alembic downgrade 0001`로 본 PR 회귀 가능.
- **uv.lock 변경**: 본 PR 의존성 추가 0건 (모두 I-01에서 도입된 sqlalchemy / aiosqlite / alembic 재사용). uv sync 결과 drift 0 기대.
- **GitHub Actions backend-ci**: I-01의 5 step workflow 그대로 적용. 본 PR에서 추가 step 0건.
