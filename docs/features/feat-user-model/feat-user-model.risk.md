---
doc_type: feature-risk
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

# feat-user-model — Feature Risk

> Issue #2. 5 FRISK 모두 Low. High 0건 → 단계적 롤아웃 N/A. 데이터 영속성 변경 1건 (users 테이블 신설).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — 5 FRISK 모두 Low |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| FRISK-01 | Alembic autogenerate 결과 검증 누락으로 컬럼 불일치 | 3 | 2 | Low |
| FRISK-02 | UNIQUE 제약 누락 또는 인덱스 미생성 | 3 | 1 | Low |
| FRISK-03 | password_hash NOT NULL로 박은 후 OAuth 도입 시 변경 부담 | 2 | 2 | Low |
| FRISK-04 | in-memory aiosqlite fixture에서 Base.metadata.create_all 실패 | 2 | 1 | Low |
| FRISK-05 | tests/unit/ 하위 폴더 도입으로 기존 pytest discovery 변경 | 1 | 1 | Low |

등급 계산: 영향 × 가능성 (최대 25). 9 이하 = Low, 10~14 = Medium, 15+ = High.

## 2. 리스크 상세

### FRISK-01: Alembic autogenerate 결과 검증 누락
- **시나리오**: `alembic revision --autogenerate -m "add users"` 실행 후 생성된 0002 파일의 `op.create_table` 컬럼이 의도와 미세하게 다른 경우 (예: `nullable=True` 잘못 박힘, `server_default=func.now()`가 `text("CURRENT_TIMESTAMP")`로 출력 등)
- **완화**: P8 implement에서 autogenerate 결과를 *반드시 사람이 읽고* PR diff에 commit. AC-03이 PRAGMA로 컬럼 정합 검증.
- **검출**: pytest test_create_user_persists에서 INSERT 실패 시 즉시 발각.
- **롤백**: 별도 마이그레이션 추가 (0003)로 컬럼 수정. Alembic의 stamp head로 rebase 회피.

### FRISK-02: UNIQUE 제약 누락
- **시나리오**: `Mapped[str] = mapped_column(unique=True)`로 선언했는데 autogenerate가 ix_users_email 같은 명시 인덱스 안 만들고 ALTER TABLE ADD CONSTRAINT만 생성. SQLite는 둘 다 작동하나 PRAGMA index_list 출력 형태가 달라짐.
- **완화**: 본 PR 정책 — autogenerate 결과 그대로 수용. AC-03이 sqlite ".schema users"로 UNIQUE 키워드 등장 확인.
- **검출**: I-03 통합 테스트에서 중복 이메일 가입 시 IntegrityError 발생 확인.

### FRISK-03: password_hash NOT NULL 부담
- **시나리오**: 향후 OAuth (Google·GitHub 로그인) 도입 시 password_hash NULL 사용자 등장 → schema 변경 필요.
- **완화**: 본 학습 과제는 RFP §3 / SRS R-F-01에서 OAuth Out of Scope 명시. 후속 학습 과제 ADR로 NULL 허용 마이그레이션 검토.
- **결정**: NOT NULL 유지 (이번 PR).

### FRISK-04: in-memory aiosqlite fixture 실패
- **시나리오**: pytest fixture `db_session`이 `create_async_engine("sqlite+aiosqlite:///:memory:")` + `Base.metadata.create_all(engine.sync_engine)` 호출. SQLAlchemy 2.0 async + sync conn mix 패턴이라 typo 가능.
- **완화**: 표준 SQLAlchemy 2.0 async 패턴 따름. `async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)` 사용.
- **검출**: pytest 첫 실행 시 즉시 발각.
- **롤백**: 파일 DB(tmp_path)로 대체.

### FRISK-05: tests/unit/ 디렉토리 신설 영향
- **시나리오**: 기존 `tests/test_health.py`가 평면, 신규 `tests/unit/test_user_repo.py`가 1단 하위. pytest 기본 discovery는 둘 다 수집 (default).
- **완화**: pyproject.toml `[tool.pytest.ini_options]`에 testpaths 또는 rootdir 명시 안 함 → pytest 기본 동작 = 양쪽 수집.
- **검출**: AC-06 회귀 전체 pytest로 6 passed 확인.

## 3. High 등급 단계적 롤아웃

**N/A** — High 등급 0건. 5 FRISK 모두 Low. 단계적 롤아웃 불필요.

## 4. 데이터 영속성 변경

| 변경 | 종류 | 영향 |
|---|---|---|
| `users` 테이블 신설 (5 컬럼 + 2 UNIQUE) | 신규 테이블 | dev DB에 빈 테이블 추가. 기존 데이터 없음 (I-01 직후 dev DB 자체 빈 상태) |
| Alembic head 0001 → 0002 | revision 추가 | downgrade로 회귀 가능 |

**dev DB 마이그레이션 절차** (사람용):
1. `cd backend && uv run alembic upgrade head` → 0001 + 0002 적용
2. `cd backend && uv run alembic current` → `0002 (head)` 확인
3. (선택) `sqlite3 data/realworld.db ".schema users"` → 5 컬럼 + UNIQUE 확인

**회귀**: `cd backend && uv run alembic downgrade 0001` → users 테이블 drop. dev DB 0001 상태로.

## 5. 15-risk.md 갱신 항목

(없음) — 본 PR의 5 FRISK 모두 *기능 단위 리스크*로, 시스템 차원 영향 없음. 15-risk.md (RISK-01~08) 갱신 불필요.

다음 이슈에서 갱신 후보:
- I-03 AuthService: R-N-03 bcrypt 단위 검증이 RISK-03 (보안) 단계적 검증 항목과 연결될 수 있음
- I-05 100건 시드 + p95: RISK-04 (퍼포먼스) 측정 갱신 예상
