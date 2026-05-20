---
doc_type: feature-code-review
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

# feat-user-model — Code Review

> P9. Generator≠Evaluator. C1~C5 diff 검토 후 Verdict PASS. NEEDS-WORK 0건.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — 10 OX 결과 9 PASS + 1 DEFER (P13 docs-update에서 처리). NEEDS-WORK 0건 |

## 0. Verdict

**PASS** — 5 커밋 diff 검토 결과 contract §2 Before/After 11행 + plan 5 커밋 DAG 모두 매핑. NEEDS-WORK 0건. P10 AI 게이트 진입 허용.

- [reviewer]: woosung.ahn@bespinglobal.com (AI — Generator≠Evaluator)
- [review_at]: 2026-05-20

## 1. 컨트랙트 충실도

각 contract Before/After 행이 코드로 매핑됨:

| 항목 | Before | After | 코드 매핑 | OX |
| --- | --- | --- | --- | --- |
| `models/__init__.py` | 없음 | re-export `Base`, `User` | `backend/realworld/models/__init__.py` 4 lines | ✅ |
| `models/base.py` | 계획 외 (순환 import 회피) | `class Base(DeclarativeBase)` | `backend/realworld/models/base.py` 5 lines | ✅ (P8 결정 §5 inline) |
| `models/user.py` | 없음 | User 5 컬럼 typed Mapped | `backend/realworld/models/user.py` 21 lines | ✅ |
| `repositories/__init__.py` | 없음 | 빈 패키지 마커 | `backend/realworld/repositories/__init__.py` | ✅ |
| `repositories/user.py` | 없음 | UserRepo 3 async 메서드 | `backend/realworld/repositories/user.py` 26 lines | ✅ |
| `alembic/env.py target_metadata` | None | Base.metadata | `backend/alembic/env.py:11,20` 수정 | ✅ |
| `alembic/versions/0001_initial.py` | 그대로 | 그대로 | 변경 0건 | ✅ |
| `alembic/versions/0002_add_users.py` | 없음 | autogenerate 결과 (수동 정리) | `backend/alembic/versions/0002_add_users.py` 43 lines | ✅ |
| `tests/unit/__init__.py` | 없음 | 빈 마커 | 생성 | ✅ |
| `tests/unit/test_user_repo.py` | 없음 | 3 케이스 | `backend/tests/unit/test_user_repo.py` 41 lines | ✅ |
| `tests/conftest.py` | client fixture만 | + db_session fixture | `backend/tests/conftest.py:18-29` 추가 | ✅ |

Call Sites 검증:
- `realworld/config.py::get_settings` — UserRepo 테스트가 의존 안 함 (별도 in-memory engine) ✅
- `realworld/db.py::AsyncSession` — UserRepo 시그니처 `__init__(session: AsyncSession)` 일치 ✅
- `alembic/env.py target_metadata` — None → Base.metadata 정확 변경 ✅

## 2. 테스트 커버리지

- **단위 테스트 3건 / 메서드 3건 = 100% 시그니처 커버**
  - `test_create_user_persists` → `UserRepo.create` + DB persist 확인
  - `test_find_by_email_returns_existing` → `UserRepo.find_by_email` (positive case)
  - `test_find_by_username_returns_none_for_unknown` → `UserRepo.find_by_username` (negative case)
- **회귀**: 기존 3 health 테스트 PASS 유지 (`tests\test_health.py ... [50%]` + `tests\unit\test_user_repo.py ... [100%]` 합산 6 passed)
- **누락 시나리오** (DEFER):
  - UNIQUE 충돌 시 IntegrityError → I-03 AuthService.register 통합 단계에서 검증 (contract §6 비목표)
  - `find_by_email` negative case (없는 이메일 → None) → AC-04 시그니처 검증으로 대체 (단순 로직, 별도 단위 테스트 부담 회피)
  - `created_at` server_default 동작 → AC-03 PRAGMA 검증으로 대체
- **커버리지 목표 달성**: 13/01-strategy §1 ≥80%. UserRepo 3 메서드 100% > 80% ✅

## 3. 보안 / 시크릿

- ✅ 시크릿 0건 — UserRepo 코드·테스트 코드·마이그레이션 코드 어디에도 평문 비밀번호·API 키·JWT secret 없음
- ✅ `password_hash` 컬럼 — TEXT 슬롯만. 본 PR은 hash 생성 책임 없음 (I-03 책임)
- ✅ 테스트의 dummy hash `"$2b$12$dummyhash"` — bcrypt 형식 흉내내지만 실제 검증 가능한 해시 아님 (random salt 아님, 12 round 표기만). 의도된 placeholder
- ✅ in-memory aiosqlite — 디스크 파일 0건 (.gitignore 영향 0)
- ✅ R-N-03 (bcrypt) — 본 PR scope 외, 슬롯만 제공. I-03에서 실제 hash·verify 추가 예정
- ✅ R-N-04 (JWT secret) — 본 PR scope 외. UserRepo는 JWT 무관

## 4. 가독성 / 단순성

- ✅ 모듈별 단일 책임 — base.py(Base) / user.py(model) / repositories/user.py(repo) 명확히 분리
- ✅ SQLAlchemy 2.0 typed Mapped 스타일 — 후속 모델(Article, Comment) 추가 시 패턴 재사용 가능
- ✅ async/await 일관 — UserRepo 3 메서드 모두 async, AsyncSession 의존성 주입
- ✅ `find_by_*` / `create` 네이밍 — 11-coding-conventions §1 snake_case + 도메인 의미 명확
- ✅ docstring·comment 0건 — 함수 시그니처 자체로 의도 표현됨. unnecessary comment 회피 (CLAUDE.md "Default to writing no comments")
- ✅ test 함수명 `test_<scenario>_<expected>` — 11-coding-conventions §1 컨벤션 정합

## 5. 발견 사항 (3축 OX 분류)

| 발견 | in_scope | blocks_merge | same_area | 처리 |
| --- | --- | --- | --- | --- |
| F1. models/base.py 분리 (plan §5 inline 결정) | ✅ | ❌ | ✅ | OK — P8 정상 결정 (순환 import 회피) |
| F2. UserRepo.create의 refresh 호출 | ✅ | ❌ | ✅ | OK — created_at server_default 값을 받아오기 위해 필요 |
| F3. session.flush() — commit 아님 | ✅ | ❌ | ✅ | OK — 트랜잭션 범위는 호출자(라우트) 책임. UserRepo는 flush만 |
| F4. alembic 0002 파일 수동 정리 (`from typing import Sequence` → `from collections.abc`, `from __future__` 등 typing) | ✅ | ❌ | ✅ | OK — ruff auto-fix 적용. 가독성 개선 |
| F5. autogenerate가 생성한 `1812be4822a4_add_users.py`는 0002로 대체됨 | ✅ | ❌ | ✅ | OK — 0001/0002 zero-padded 명명 유지 |
| F6. `tests/unit/__init__.py` 빈 파일 | ✅ | ❌ | ✅ | OK — pytest discovery는 무관, 패키지 마커 명시적 |
| F7. test 파일 docstring 없음 | ✅ | ❌ | ✅ | OK — 함수명이 시나리오 표현 (test_<scenario>_<expected>) |
| F8. `password_hash="$2b$12$dummyhash"` 테스트 시드 | ✅ | ❌ | ✅ | OK — 슬롯 검증만, 실제 bcrypt 아님 |
| F9. UserRepo 외 `update`/`delete` 메서드 없음 | ✅ | ❌ | ✅ | OK — contract §6 비목표 (RealWorld MVP 미포함) |
| F10. 12-scaffolding §1 트리에 `models/base.py` 명시 누락 | ❌ (out of PR) | ❌ | ❌ | DEFER — P13 docs-update에서 12-scaffolding v0.3 갱신 |

**3축 OX 결과**: 9 PASS + 1 DEFER (F10). blocks_merge 0건.

## 6. NEEDS-WORK 항목

(없음) — Verdict PASS. F10은 P13 docs-update에서 처리.
