---
doc_type: feature-brief
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

# feat-user-model — Feature Brief

> Issue #2 — `feat(backend): I-02 User 모델 + 마이그레이션 + UserRepo`. SQLAlchemy User declarative 모델 + Alembic users 테이블 + UserRepo 3 메서드 + 단위 테스트.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — `/flow-feature 2` 진입. mode=add 자동 결정 (type:feature 라벨 + 부정 시그널 0건) |

## 1. 한 줄 의도

I-01 backend 스캐폴딩 위에 RealWorld User 도메인의 *영속 계층*(SQLAlchemy declarative 모델 + Alembic users 테이블 마이그레이션 + Repository 패턴 3 메서드)을 도입한다. I-03(AuthService) + I-04(users router)가 본 PR의 User 모델·UserRepo를 의존성으로 가져다 쓴다.

## 2. 사용자 가치

본 PR 자체는 *외부 사용자에게 보이는 동작 변경 0*. 다만 후속 I-03·I-04에서 회원가입(R-F-01)·로그인(R-F-02) 흐름이 가능해지려면 영속 계층이 먼저 자리잡혀야 한다 — 본 PR은 인증·게시판 모든 후속 기능의 *필수 선행 인프라*.

내부 가치:
- **데이터 모델 정본 수립**: `users` 테이블 5 컬럼(id/username/email/password_hash/created_at) + UNIQUE 제약이 Alembic 마이그레이션으로 *재현 가능한 형태*로 박힌다.
- **Repository 패턴 도입**: 서비스 계층(I-03 AuthService)이 ORM 쿼리를 직접 다루지 않고, `UserRepo.find_by_email/find_by_username/create` 3 메서드 인터페이스로 격리됨.
- **autogenerate 워크플로 검증**: I-01의 빈 init revision(0001) 위에 첫 실제 마이그레이션(0002)을 autogenerate으로 생성 → Alembic 워크플로가 실증된다.

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 (I-01 머지 직후) | 변경 후 (본 PR 머지 후) |
| --- | --- | --- |
| backend 패키지 | `realworld/{config,db,main}.py` 3개만 | + `realworld/models/{__init__,user}.py` + `realworld/repositories/{__init__,user}.py` |
| Declarative Base | 없음 (target_metadata=None) | `models/__init__.py`에 `Base = DeclarativeBase` 정의 + alembic `env.py` target_metadata 연결 |
| Alembic versions | `0001_initial.py` 빈 revision 1개 | + `0002_add_users.py` (users 테이블 5 컬럼 + 2 UNIQUE) |
| DB 스키마 | 빈 SQLite | `users` 테이블 1개 (autogenerate로 생성) |
| Repository 계층 | 없음 | `UserRepo.find_by_email`, `find_by_username`, `create` 3 메서드 (async, AsyncSession 주입) |
| 단위 테스트 | health check 3건 (test_health.py) | + `tests/unit/test_user_repo.py` 3 케이스 (in-memory SQLite fixture) |
| pytest 디렉토리 | `tests/` flat 1단 | `tests/unit/` 하위 폴더 도입 (08 §8 테스트 진입점 매핑) |
| 후속 의존 | (없음) | I-03 AuthService가 UserRepo를 import해 사용 |

## 4. 모드 자동 감지 결과

- **결정 모드**: `add` (자동 결정, 부정 시그널 0건)
- **시그널**:
  - 라벨: `type:feature` ✅ (add 양의 시그널)
  - 자연어: "User 모델 + 마이그레이션 + UserRepo" — 신규 동작
  - 부정 시그널 (bug / design / modify): 0건
- **수동 override**: 없음. ADR-0032 §2.1 무질문 자동 결정 발동.
- **결정 시각**: 2026-05-20

## 5. 영향 범위

| 영역 | 변경 | 비고 |
|---|---|---|
| backend 코드 | 신규: `models/__init__.py`, `models/user.py`, `repositories/__init__.py`, `repositories/user.py`. 수정: `alembic/env.py` (target_metadata 연결) | 5 신규 + 1 수정 |
| Alembic | 신규 revision `0002_add_users.py` (autogenerate) | down_revision="0001" |
| DB | `users` 테이블 1개 신설 (autogenerate) | dev/data/realworld.db |
| 테스트 | `tests/unit/__init__.py` + `tests/unit/test_user_repo.py` 신설 | 3 케이스 |
| conftest fixture | 추가: `db_session` (in-memory aiosqlite + Base.metadata.create_all) | 단위 테스트용 |
| 문서 | 14-wbs §2 I-02 status:in-review 갱신, INDEX.md v0.6 갱신 | P13 docs-update |
| UI / FE | 영향 0 | ui_changed=false |
| 부팅 자산 | `alembic/versions/` 추가 1개, 그 외 .env.example/LOCAL.md/uv.lock 변경 0 | 단일 환경 운영 N/A (dev only) |

**3+영역 변경**: backend 코드 / Alembic / 테스트 / 문서 (4 영역) → PR Touched Areas 절 필수.

## 6. 비목표

- **AuthService 구현 (회원가입·로그인 비즈니스 로직)** — I-03 책임. 본 PR은 *데이터 계층*만.
- **JWT 발급 / bcrypt 해시** — I-03 책임. 본 PR의 `password_hash` 컬럼은 *문자열 저장 슬롯*만 제공.
- **POST /api/users 라우트** — I-04 책임.
- **Article·Comment 모델** — I-04 (article) + I-06 (comment).
- **고급 사용자 필드**: bio, image (RealWorld spec 일부) → MVP Out of Scope (RFP §3 / SRS R-F-01).
- **테스트 fixture·factory 도구** (pytest-factoryboy 등) — 학습 부담 회피 (INDEX.md Open Q 항목, 13/01-strategy §2).
- **통합 테스트 (HTTP 라우트 거치는 테스트)** — I-04 책임.

## 7. Open Questions

| Q | 결정 |
|---|---|
| `users.username` 최대 길이 | RealWorld spec 기본값 따라 미설정 (TEXT). 후속 입력 검증은 I-03 Pydantic schema에서 (예: max_length=64) |
| password_hash 컬럼 길이 | TEXT (bcrypt 결과 60자 고정이나, 향후 알고리즘 교체 여지). I-03에서도 별도 검증 없음 |
| `created_at` timezone | UTC (server_default=`func.now()`). 응답 시 ISO8601 직렬화는 I-04 Pydantic 책임 |
| Async vs Sync SQLAlchemy | Async (`AsyncSession`). I-01 db.py에 이미 결정 (08 §1 M-Auth-Service 책임 — async session) |
| 단위 테스트 DB | in-memory aiosqlite (`sqlite+aiosqlite:///:memory:`). 테스트별 격리, Base.metadata.create_all로 스키마 생성 |
| migration 파일명 | `0002_add_users.py` — I-01 0001과 zero-padded 4자리 연속 (Alembic file_template 정합) |
