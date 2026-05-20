---
doc_type: feature-contract
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

# feat-user-model — Change Contract

> Issue #2. User SQLAlchemy 모델 + Alembic 마이그레이션 + UserRepo 3 메서드 + 단위 테스트 3건.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — §0 5행 + §2 11 Before/After + §3 6 Call Sites |

## 0. 참조 정본 ID (Referenced-IDs)

본 PR 작업 시 selective read 진입점 (ADR-0018). 후속 P4 implementation-planner가 본 표를 기반으로 *부분 읽기*로 plan 작성.

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| R-ID (SRS) | `docs/planning/04-srs/04-srs.md` §R-F-01 / §R-N-03 / §R-N-04 | R-F-01 (회원가입 데이터 모델), R-N-03 (bcrypt password_hash 슬롯), R-N-04 (DB URL 환경변수) |
| F-ID (PRD) | `docs/planning/05-prd/05-prd.md` §F-01 | F-01 (Auth — User 도메인 데이터 모델) |
| Module (LLD) | `docs/planning/08-lld-module-spec/08-lld-module-spec.md` §3 "Repository" + §8 테스트 진입점 | M-Auth-Service 의존성 (UserRepo) |
| Scaffolding | `docs/planning/12-scaffolding/python.md` §1 트리 (`realworld/models/`, `realworld/repositories/`, `tests/unit/`) | backend 디렉토리 구조 |
| Conventions | `docs/planning/11-coding-conventions/11-coding-conventions.md` §1 명명 규칙 | SQLAlchemy 모델 PascalCase 단수형 `User` / 테이블 복수형 `users` / 컬럼 snake_case |

## 1. 변경 의도

I-01 backend 스캐폴딩 위에 RealWorld User 도메인 *데이터 계층*을 도입한다:

1. **SQLAlchemy declarative Base 수립** — `realworld/models/__init__.py`에 `Base = DeclarativeBase` 정의. Alembic env.py target_metadata에 연결해 autogenerate 워크플로 실증.
2. **User 모델** (`models/user.py`) — `id` PK + `username` UNIQUE + `email` UNIQUE + `password_hash` (TEXT 슬롯, 본 PR 미사용) + `created_at` server_default.
3. **첫 실제 마이그레이션** — `alembic revision --autogenerate -m "add users"` → `0002_add_users.py` 생성. `alembic upgrade head` 실행 후 SQLite `users` 테이블 + 2 UNIQUE 인덱스 확인.
4. **Repository 패턴 도입** (`repositories/user.py`) — 3 메서드 (`find_by_email`, `find_by_username`, `create`). 후속 I-03 AuthService가 ORM 쿼리를 직접 다루지 않고 본 인터페이스만 의존.
5. **단위 테스트** (`tests/unit/test_user_repo.py`) — 3 케이스. in-memory aiosqlite + Base.metadata.create_all fixture.

본 PR의 *외부 사용자 동작 영향 0*. I-03·I-04 진입을 위한 필수 선행 인프라.

## 2. Before / After

| 항목 | Before | After |
| --- | --- | --- |
| `realworld/models/__init__.py` | 없음 | `from sqlalchemy.orm import DeclarativeBase` + `class Base(DeclarativeBase): pass` + `__all__ = ["Base", "User"]` |
| `realworld/models/user.py` | 없음 | SQLAlchemy 2.0 typed Mapped 스타일. `id: Mapped[int] primary_key` / `username: Mapped[str] UNIQUE` / `email: Mapped[str] UNIQUE` / `password_hash: Mapped[str]` / `created_at: Mapped[datetime] server_default=func.now()`. `__tablename__ = "users"` |
| `realworld/repositories/__init__.py` | 없음 | 빈 패키지 마커 (`""""""`) |
| `realworld/repositories/user.py` | 없음 | `class UserRepo` + AsyncSession 의존성 주입. 3 async 메서드: `find_by_email(email: str) -> User \| None` / `find_by_username(username: str) -> User \| None` / `create(username, email, password_hash) -> User` |
| `alembic/env.py` `target_metadata` | `None` | `from realworld.models import Base` import + `target_metadata = Base.metadata` |
| `alembic/versions/0001_initial.py` | 빈 init (revision="0001", down="None") | 그대로 (변경 없음, 본 PR baseline) |
| `alembic/versions/0002_add_users.py` | 없음 | autogenerate 결과. `revision="0002", down_revision="0001"`. `op.create_table("users", ...)` + 2 `op.create_index` (UNIQUE) |
| DB 스키마 (런타임) | 빈 SQLite (revision 0001) | `users` 테이블 + 2 UNIQUE 인덱스 + revision 0002 head |
| `tests/__init__.py` | 빈 마커 | 그대로 |
| `tests/unit/__init__.py` | 없음 | 빈 마커 |
| `tests/unit/test_user_repo.py` | 없음 | 3 케이스: `test_create_user_persists`, `test_find_by_email_returns_existing`, `test_find_by_username_returns_none_for_unknown` |
| `tests/conftest.py` | health check용 `client` fixture만 | + `db_session` fixture (in-memory aiosqlite + AsyncSession, scope="function") |

## 3. 호출자·의존자 (Call Sites)

본 PR 머지 후 *직접 의존하는 후속 모듈*과 *본 PR이 의존하는 기존 모듈*.

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| `realworld/config.py::get_settings` (I-01) | UserRepo 단위 테스트가 DATABASE_URL 의존하지 않도록 fixture가 별도 in-memory URL 사용 | 변경 없음. test conftest fixture가 자체 engine 생성 |
| `realworld/db.py::AsyncSession` / `get_db` (I-01) | UserRepo 시그니처가 AsyncSession 주입 받음 | 변경 없음. UserRepo는 외부에서 session 받음 |
| `alembic/env.py::target_metadata` (I-01) | `None` → `Base.metadata` | 본 PR §2 변경 — 11째 행 |
| 후속 `realworld/services/auth.py` (I-03 예정) | `UserRepo.find_by_email/find_by_username/create` 호출 예정 | 본 PR에서 인터페이스 확정. I-03가 import |
| 후속 `realworld/routers/users.py` (I-04 예정) | `Depends(get_db)` + `UserRepo(session)` 패턴 사용 예정 | 본 PR에서 패턴 시연 (테스트 fixture 동일 패턴) |
| 후속 `models/article.py::Article.author_id` (I-04 예정) | `ForeignKey("users.id")` 참조 | 본 PR이 users.id PK 확정 |

## 4. Backward Compatibility

**N/A — neutral**. 본 PR은 *신규 도입*만. 기존 동작 변경 0.

- 기존 `/health` 라우트 + 3 health 테스트: 무영향
- 기존 Alembic 0001 init revision: 그대로 유지, 본 PR 0002가 down_revision="0001" 체이닝
- 기존 `tests/test_health.py`: 평면 위치 유지 (pytest discovery 자동). `tests/unit/` 추가는 *별도 폴더* 도입이라 무영향

**dev DB 데이터 영향**: I-01에서 alembic upgrade head로 0001 적용된 `backend/data/realworld.db` 있다면 0002 추가 적용 시 users 테이블 신설 (빈 테이블). 기존 데이터 손실 0.

**다국어 / 다양한 SQLAlchemy 버전 호환**: SQLAlchemy 2.0+ typed Mapped 스타일 사용. I-01 pyproject.toml이 `sqlalchemy>=2.0.35,<2.1.0`로 박혀 있어 호환 안전.

## 5. Rollback 전략

**1차 (PR 머지 전 회귀)**: 본 PR open 상태에서 close + 브랜치 삭제. 영향 0.

**2차 (PR 머지 후 회귀)**:
1. **Alembic downgrade**: `cd backend && uv run alembic downgrade 0001` — 0002 revision의 `op.drop_table("users")` + `op.drop_index` 자동 실행. dev DB의 users 테이블 제거.
2. **revert PR**: `git revert <merge_sha>` 후 별도 PR. 모델·repo·테스트 파일 일괄 삭제.
3. **revert 영향**: I-03 미진입 상태라면 무영향. I-03가 이미 머지된 상태에서 본 PR revert는 *블로커* — I-03도 함께 revert 필요 (cascade revert).

**Trigger 조건**:
- Alembic 마이그레이션 적용 후 DB 부정합 (UNIQUE 충돌 등) → 1순위 downgrade
- UserRepo 테스트 30% 이상 실패 → revert PR
- 단순 import 에러는 hotfix PR 권장 (revert 부담 큼)

## 6. 비목표

- AuthService 비즈니스 로직 (회원가입·로그인) — I-03
- bcrypt 해시 / JWT 발급 — I-03
- POST /api/users · POST /api/users/login 라우트 — I-04
- bio / image 컬럼 (RealWorld spec 일부) — MVP Out of Scope (RFP §3)
- Article·Comment 모델 — 후속 이슈
- UserRepo의 update / delete — 본 PR scope 외. RealWorld MVP는 회원 정보 수정 미포함
- 통합 테스트 (HTTP 라우트 통한) — I-04
- 마이그레이션 dry-run 도구 (`alembic --sql`) — 본 학습 과제 미사용
