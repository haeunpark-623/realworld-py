---
doc_type: feature-plan
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

# feat-user-model — Implementation Plan

> Issue #2. 5 커밋 DAG. Critical path: C1 → C2 → C3 → C4 → C5.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — 5 커밋 + 3 단위 테스트 + autogenerate 워크플로 검증 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `feat(backend): I-02 SQLAlchemy Base + User declarative 모델` | `backend/realworld/models/__init__.py` (신규) · `backend/realworld/models/user.py` (신규) | (없음 — 모델만) | 0건. import-only 변경 |
| C2 | `feat(backend): I-02 alembic env target_metadata + 0002 add_users autogenerate` | `backend/alembic/env.py` (수정) · `backend/alembic/versions/0002_add_users.py` (신규 autogenerate) | (없음 — 마이그레이션만. 실행 검증은 §4) | Low. dev DB users 테이블 신설(empty) |
| C3 | `feat(backend): I-02 UserRepo 3 메서드 + repositories 패키지` | `backend/realworld/repositories/__init__.py` (신규) · `backend/realworld/repositories/user.py` (신규) | (없음 — 다음 커밋 C4에서 일괄) | 0건. 신규 패키지 |
| C4 | `test(backend): I-02 tests/unit + db_session fixture + UserRepo 3 테스트` | `backend/tests/unit/__init__.py` (신규) · `backend/tests/unit/test_user_repo.py` (신규) · `backend/tests/conftest.py` (수정, db_session fixture 추가) | ✅ 3 unit tests | 0건. 신규 테스트만 |
| C5 | `docs(feat): I-02 feat-user-model brief + contract + plan` | `docs/features/feat-user-model/feat-user-model.{brief,contract,plan,eng-review,acceptance,risk}.md` (신규) | (없음 — 문서) | 0건. 문서만 |

**Critical path**: C1 → C2 → C3 → C4 (C5 docs는 P9~P14에서 추가 커밋들과 함께 진화).

## 2. 의존성 그래프

```
C1 (Base + User 모델)
  ↓
C2 (alembic env target_metadata + 0002 autogenerate)
  │   └─ autogenerate는 C1의 Base.metadata + User 모델 정의 필요
  ↓
C3 (UserRepo 3 메서드)
  │   └─ UserRepo는 C1의 User 모델 import
  ↓
C4 (단위 테스트 + db_session fixture)
  │   └─ in-memory engine + Base.metadata.create_all → C1 의존
  │   └─ UserRepo 호출 → C3 의존
  ↓
(P9~P14)
  └─ C5: docs/features/feat-user-model/*.md (병행 진화)
```

**병렬 가능성**: 없음 — 모두 순차 의존. AI 페어 가속으로 ~30분 내 완주 가능 (effort 0.5d ≈ 30~45분, 14-wbs §0.1).

## 3. 테스트 매핑

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C1 | (없음, 모델 정의만) | 컴파일·import 검증은 C2 alembic autogenerate 단계에서 간접 확인 |
| C2 | (없음, autogenerate 산출) | `alembic upgrade head` 실행 → 0002 적용 PASS = 검증. 본 PR P10 AC-03 |
| C3 | (없음, 다음 커밋에서 일괄) | — |
| C4 | `backend/tests/unit/test_user_repo.py` | **test_create_user_persists**: UserRepo.create → DB에 row 1건 생성 + return User 객체 확인. **test_find_by_email_returns_existing**: create 후 find_by_email로 동일 user 조회. **test_find_by_username_returns_none_for_unknown**: find_by_username("absent") → None |
| 회귀 | `backend/tests/test_health.py` (기존 3건) | 평면 위치 유지 + 무영향 확인 (pytest discovery로 함께 실행) |

**커버리지 목표**: UserRepo 3 메서드 100% (각 1 테스트). I-03·I-04에서 추가 시나리오 fan-in 예정.

## 4. 빌드·실행 검증 단계

각 커밋 직후 + 마지막 일괄 실행. 12-scaffolding §5 + LOCAL.md §3.1 정합.

```bash
# C1 직후 — import 컴파일 검증
cd backend && uv run python -c "from realworld.models import Base, User; print(Base.metadata.tables.keys())"
# 기대: dict_keys(['users'])

# C2 직후 — Alembic autogenerate + 적용
cd backend && rm -f data/realworld.db                          # 기존 dev DB 초기화 (선택)
cd backend && uv run alembic upgrade head
# 기대: 0001 → 0002 순차 적용, exit 0
cd backend && uv run alembic current
# 기대: 0002 (head)

# C3 직후 — UserRepo import 검증
cd backend && uv run python -c "from realworld.repositories.user import UserRepo; print(UserRepo)"
# 기대: <class 'realworld.repositories.user.UserRepo'>

# C4 직후 — 단위 테스트 실행
cd backend && uv run pytest tests/unit/test_user_repo.py -v
# 기대: 3 passed

# 전체 회귀 (마지막)
cd backend && uv run ruff check . && uv run ruff format --check .
cd backend && uv run pytest -v
# 기대: ruff PASS + pytest 6 passed (3 health + 3 user_repo)

# Manual reproduction (ADR-0047 GitHub Actions 양축)
cd backend && uv sync --frozen && uv run ruff check . && uv run ruff format --check . && uv run alembic upgrade head && uv run pytest -v
# 기대: 5 step 모두 exit 0
```

## 5. 점진 합의 / 결정 발생 항목

본 PR 진행 중 다음 결정이 *plan 시점에 미확정*. 발생 시 inline 결정 + risk.md 추가:

- **Alembic autogenerate 결과의 `op.create_index` UNIQUE 표현**: SQLAlchemy 2.0 Mapped 스타일에서 `unique=True`로 선언하면 autogenerate가 index 자체를 안 만들고 UNIQUE 제약만 만들 수 있음 — 결과를 확인하고, 명시적 UNIQUE 제약과 별도 index 필요 여부 결정. 본 PR 기본 정책: autogenerate 결과 그대로 유지(수정 없음). 후속 I-04에서 검색 성능 검토 시 재고려.
- **`User.__repr__` 추가 여부**: 디버깅 편의. 본 PR 미포함 (yagni). 필요 시 후속 별도 커밋.
- **password_hash 컬럼 NOT NULL**: 본 PR에서 NOT NULL로 박음 (I-03 register 시 항상 hash 채움). 향후 OAuth 등으로 NULL 허용이 필요해지면 Alembic 별도 마이그레이션으로 변경.
