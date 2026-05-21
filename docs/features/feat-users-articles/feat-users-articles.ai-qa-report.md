---
doc_type: feature-ai-qa
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
ui_changed: "false"
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-12, R-N-01, R-N-05]
  F-ID: [F-01, F-02]
  supersedes: null
---

# feat-users-articles — AI QA Report

> D-06 1단 (AI 게이트). 6축 + Test Plan 4블록 + 로컬 부팅 검증. PASS 후 PR open.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 6축 모두 PASS / Test Plan 4블록 / 부팅 검증 dev profile 1건 |

## 0. Verdict

**PASS** — AI 게이트 6축 모두 통과. PR 생성 진입 허용. Manual verification·DoD coverage 체크박스는 PR body에 미체크 상태로 등록 (ADR-0046 §2.3).

- [reviewer]: woosung.ahn@bespinglobal.com (AI)
- [review_at]: 2026-05-21
- [ui_changed]: false
- [Flow Mode]: add

## 1. Test Plan 4블록

### Build

```bash
cd backend && uv sync --frozen
```

**결과**: 60+ packages audited. exit code 0. 의존성 추가 0건 (alembic·sqlalchemy·pydantic·passlib·python-jose·bcrypt·httpx·email-validator 모두 I-01에 있음).

### Automated tests

```bash
cd backend && uv run alembic upgrade head && uv run ruff check . && uv run ruff format --check . && uv run pytest -v
```

**결과**:
- alembic `0003 (head)` 정합
- ruff check `All checks passed!`
- ruff format `42 files already formatted`
- pytest `52 passed in 11.20s` (3 health + 30 unit + 19 integration)

### Manual verification

사람이 직접 확인 필요. PR body 미체크 상태로 등록 (ADR-0046 §2.3).

- [ ] `cd backend && uv run alembic current` 실행 → `0003 (head)` 출력 확인 (스키마 진행)
- [ ] `cd backend && uv run pytest tests/integration/ -v` 실행 → `19 passed` 확인 (통합 라우트 전체)
- [ ] `cd backend && uv run uvicorn realworld.main:app --host 0.0.0.0 --port 8000` 부팅 → 브라우저 `http://localhost:8000/docs` 진입 → 13 라우트 Swagger UI 노출 확인
- [ ] `cd backend && uv run python -c "from realworld.main import app; print(len(app.routes))"` 실행 → `13` 출력 확인 (라우트 등록 정합)
- [ ] GitHub Actions 워크플로 로컬 검증 (act 또는 manual): `cd backend && uv sync --frozen && uv run alembic upgrade head && uv run ruff check . && uv run ruff format --check . && uv run pytest -v` → 5 step 모두 exit 0 + pytest 52 passed

### DoD coverage

11 항목 — 이슈 #4 body DoD Checklist 11 (D-04-1~11) 매핑. PR body 미체크 상태로 등록 (ADR-0046 §2.3).

- [ ] D-04-1 `models/article.py` Article + Tag + article_tags M2M + re-export
- [ ] D-04-2 `migrations/versions/0003_articles_tags.py` upgrade/downgrade
- [ ] D-04-3 `utils/slug.py` slugify + unique_slug
- [ ] D-04-4 `repositories/article.py` ArticleRepo 6 메서드 + selectinload N+1 회피
- [ ] D-04-5 `services/article.py` ArticleService 5 메서드 + 작성자 검증
- [ ] D-04-6 `schemas/user.py` + `schemas/article.py` Pydantic
- [ ] D-04-7 `routers/users.py` 3 라우트 + `routers/articles.py` 5 라우트
- [ ] D-04-8 `main.py` 라우터 등록 + RealWorldError 핸들러 (422 한글)
- [ ] D-04-9 단위 테스트 ≥ 13 PASS (test_slug 5 + test_article_service 8)
- [ ] D-04-10 통합 테스트 ≥ 14 PASS (19 실측 — test_users_routes 7 + test_articles_routes 12)
- [ ] D-04-11 R-F-12 `?author=` 필터 통합 테스트 + GitHub Actions `backend-ci` green

## 2. AI 게이트 6축

| # | 축 | 결과 | 근거 |
| --- | --- | --- | --- |
| 1 | 컨트랙트 충실도 | ✅ PASS | code-review.md §1 — Before/After 16행 모두 코드 매핑 확인 + Call Sites 8개 매핑 |
| 2 | 단위/통합 테스트 통과 | ✅ PASS | `pytest -v` 52 passed in 11.20s (기존 20 + 신규 32 = 합산 52) |
| 3 | Lint + Format | ✅ PASS | ruff check `All checks passed!` + ruff format `42 files already formatted` |
| 4 | 의존성·lockfile 동기 | ✅ PASS | `uv sync --frozen` 통과. pyproject.toml ruff per-file-ignores 추가만 (의존성 변경 0) |
| 5 | UI/FE 브라우저 골든패스 + stylesheet | ✅ N/A | UI 변경 0 (backend HTTP API). ui_changed=false 자동 통과 |
| 6 | dev/stg/prod 3 profile 부팅 + 부팅 자산 동기 | ✅ PASS (단일 환경 운영 N/A 사유) | dev profile: alembic `0003 (head)` + 13 routes 등록 + 52 passed. stg/prod: N/A (RFP §NFR-06 + ADR-0037 v1.1). 부팅 자산 변경: pyproject.toml 1 + alembic 0003 1건 |

추가 축(ADR-0047 워크플로 양축):
| 축 | 결과 | 근거 |
| --- | --- | --- |
| GitHub Actions 워크플로 로컬 검증 | ✅ PASS (act 미설치 → manual reproduction 채택) | `uv sync --frozen` + `alembic upgrade head` + `ruff check` + `ruff format --check` + `pytest -v` 5 step 모두 통과 (52 passed) |

## 3. 시나리오 인용

| 시나리오 | 출처 | 결과 |
| --- | --- | --- |
| AC-01 Article + Tag + Alembic 0003 진행 | acceptance §1 | ✅ — `alembic current` → `0003 (head)` |
| AC-02 utils/slug 슬러그 생성 | acceptance §1 | ✅ — slugify 5 PASS |
| AC-03 ArticleService 5 메서드 | acceptance §1 | ✅ — 8 단위 PASS |
| AC-04 POST /api/users happy | acceptance §1 | ✅ — test_register_returns_user_with_token PASS |
| AC-05 POST /api/users/login happy + 422 | acceptance §1 | ✅ — 2건 PASS |
| AC-06 GET /api/user JWT + 401 | acceptance §1 | ✅ — 2건 PASS |
| AC-07 POST /api/articles + slug 충돌 | acceptance §1 | ✅ — 2건 PASS |
| AC-08 PUT /api/articles 작성자/타인 | acceptance §1 | ✅ — 2건 PASS |
| AC-09 DELETE /api/articles 작성자/타인 | acceptance §1 | ✅ — 2건 PASS |
| AC-10 ?author= 필터 + 빈 결과 | acceptance §1 | ✅ — 2건 PASS |
| 회귀 — 기존 17 테스트 무영향 | acceptance §4 | ✅ — 전체 `52 passed` (기존 20 + 신규 32) |

## 4. FAIL 항목

(없음) — 10 AC 모두 PASS, 6 축 모두 PASS.

## 5. 발견 사항

- **양호**: contract §0 Referenced-IDs 8행으로 selective read 진입점 명시 — P4 plan에서 09-api-spec §3 8 라우트만 가벼운 읽기로 충분
- **양호**: mode=add 자동 결정(ADR-0032)으로 BLOCKED 0건 — Issue #1·#2·#3에 이어 4번째 무질문 진행
- **양호**: 11 커밋 모두 ADR-0021 정규식 통과 — `feat(backend):` 5 / `test(backend):` 3 / `fix(backend):` 2 / `chore(backend):` 1
- **양호**: FRISK-04 예상 위험(exception_handler 분기)이 실 동작 검증 — 422/401/403/404 매핑 정합 통합 테스트로 cover
- **DEFER (contract drift)**: errors.InvalidCredentials.status_code 401 → 422 변경 (code-review F1). 9-api-spec 정합 + I-03 회귀 0
- **DEFER (인라인 결정)**: ArticleService.update가 refresh 대신 get_by_slug 재조회 (code-review F2). selectin lazy load 회귀 발견 직후 인라인 수정
- **메모 (후속)**: I-05 시드 + p95 측정 시 본 PR ArticleService.create 100회 호출. I-05/I-06 comment 라우트는 본 PR의 require_auth + RealWorldError handler 패턴 재사용

## 6. UI/FE 변경 검증

**N/A — 본 PR ui_changed=false**. backend HTTP API 계층. UI 변경 0건.

- [gstack_qa_used]: gstack /qa N/A 사전 합의 (UI 변경 없음)
- [console_errors]: N/A 사전 합의 (브라우저 미사용)
- [stylesheet 적용 근거]: N/A — backend PR (tailwind/css bundle 무관)

| 화면 | 시나리오 | 스크린샷경로 | stylesheet 적용 |
| --- | --- | --- | --- |
| N/A | N/A — ui_changed=false | N/A | N/A — backend PR |

## 7. 로컬 부팅 가능성

| 프로파일 | 부팅 명령 | 결과 (ready 신호) | 에러 | 부팅 자산 변경 |
| --- | --- | --- | --- | --- |
| dev | `cd backend && uv run alembic upgrade head && uv run alembic current && uv run python -c "from realworld.main import app; print(len(app.routes))"` | ✅ `0003 (head)` 정합 + 13 routes + 52 passed | 0건 | ✅ alembic 0003 1건 (신규 migration) + pyproject.toml 1건 (ruff per-file-ignores 2 추가). .env.example/uv.lock/LOCAL.md 변경 0. 12-scaffolding §1 트리는 P13에서 갱신 (schemas/ + routers/ 추가) |
| stg | N/A — 단일 환경 운영 (RFP §NFR-06 + ADR-0037 v1.1) | N/A | N/A | N/A |
| prod | N/A — 단일 환경 운영 (RFP §NFR-06 + ADR-0037 v1.1) | N/A | N/A | N/A |
