---
doc_type: feature-code-review
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: feature
related:
  R-ID: [R-N-04, R-N-06]
  F-ID: []
  supersedes: null
---

# feat-bootstrap-backend — Code Review

> Generator(implement) ≠ Evaluator(code-review). 8 커밋 diff 전수 검토. mode=add 최소 침습 원칙 검증.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — 8 커밋 + 12 파일 (코드 4 + 테스트 2 + 설정/마이그레이션 4 + CI/lint 2) 검토 |

## 0. Verdict

**PASS** — Issue #1 backend 부팅 골격 PR 머지 진입 허가. 컨트랙트 충실도 ✅ + 테스트 통과 (3/3) ✅ + 보안 절대 규칙 ✅ + 코드 단순성 ✅. plan §1 7 커밋 DAG가 docs 1 + C1~C7 = 8 커밋으로 정확히 매핑됨.

- [reviewer]: woosung.ahn@bespinglobal.com (Evaluator 역할 — Generator(implement)와 분리)
- [review_at]: 2026-05-20

## 1. 컨트랙트 충실도

contract.md §2 Before/After 13행 모두 후행 코드와 1:1 매핑 확인:

| Before/After 행 | 후행 코드 | 검증 결과 |
| --- | --- | --- |
| backend/ 디렉토리 신규 | C1~C7 모두 `backend/` 하위 | ✅ |
| Python 패키지 `realworld` 신규 | C2 `realworld/{__init__,main,config,db}.py` | ✅ |
| 의존성 lock | C1 `pyproject.toml` + `uv.lock` (60 packages) | ✅ |
| FastAPI app `realworld.main:app` | C2 `realworld/main.py:app` (line 43) | ✅ |
| `GET /health` 엔드포인트 | C2 `realworld/main.py:38-40` health() | ✅ |
| `GET /docs` Swagger UI | C2 `FastAPI(docs_url="/docs")` line 25 | ✅ |
| AsyncEngine + Session factory | C2 `realworld/db.py:14,21` | ✅ |
| Alembic init 1건 (0001_initial) | C4 `alembic/versions/0001_initial.py` + 빈 upgrade/downgrade | ✅ |
| `.env.example` 4 키 + 추가 2개 | C3 6 키 명시 (DATABASE_URL/JWT_SECRET/JWT_ALG/JWT_EXPIRE_MINUTES + CORS_ORIGINS + LOG_LEVEL) | ✅ contract 명세 4 + 추가 2 (`CORS_ORIGINS`·`LOG_LEVEL`은 plan §5 결정) |
| LOCAL.md §3.1 실 검증 | C7 v0.2 changelog + §3.1 verification 1줄 | ✅ |
| pytest 셋업 | C5 conftest + test_health.py | ✅ |
| Lint/Format ruff | C1 pyproject.toml `[tool.ruff]` + C6 pre-commit | ✅ |
| GitHub Actions backend-ci.yml | C6 신규 워크플로 | ✅ |
| `.gitignore` 보안 패턴 | C3 backend/.gitignore | ✅ |

contract §3 Call Sites 7행 모두 후속 이슈 진입점 안정화 확인:
- `realworld.main:app` import 가능 (실 검증 `uv run python -c "from realworld.main import app"`) ✅
- `realworld.config:Settings.JWT_SECRET` 등 6 키 정의 ✅
- `realworld.db:async_session_maker` + `get_db()` async generator export ✅
- `backend/alembic/versions/0001_initial.py` revision id `"0001"` 고정 ✅
- LOCAL.md §3.1 부팅 명령 검증 완료 ✅

**plan §1 7 커밋 DAG**: 산출 docs 1 커밋 + C1~C7 = 8 커밋. 순환 없음. 각 커밋 자기 검증 PASS (C1 uv sync OK / C2 import OK / C4 alembic upgrade OK / C5 pytest 3 passed / C6 ruff All checks passed / C7 LOCAL.md 검증 OK).

## 2. 테스트 커버리지

- **단위 테스트**: N/A — 본 이슈는 services·deps 0줄 (acceptance §3 사유 명시)
- **통합 테스트**: 3건 추가 (`test_health.py` 3 시나리오 모두 PASS)
  - `test_health_returns_ok`: GET /health → 200 + `{"status": "ok"}` ✅
  - `test_openapi_schema_available`: GET /openapi.json → 200 + title=`RealWorld API` + `/health` path 포함 ✅
  - `test_docs_swagger_ui_available`: GET /docs → 200 + content-type text/html ✅
- **E2E 테스트**: N/A (Issue #9 책임)
- **R-N-06 ≥ 80% 커버리지**: N/A — services·deps 0줄. 후속 이슈 #3·#4 진입 후 측정 시작
- **테스트 카탈로그(13/02) 동기**: R-/F-ID 신규 추가 없음 → 변경 N/A. P13 docs-update에서 sync check WARN 0건 예상

## 3. 보안 / 시크릿

CLAUDE.md 보안 절대 규칙 6 항목 전수 검증:

| 규칙 | 항목 | 검증 결과 |
| --- | --- | --- |
| §1 | `.env`/`*.key`/`*.pem`/`credentials.json` 등 미커밋 | ✅ `git ls-files | grep -E '\.env$\|\.key$\|\.pem$'` 결과 0건. 루트 `.gitignore` + `backend/.gitignore` 양축 |
| §2 | 코드·로그·커밋 메시지·PR 본문에 실 시크릿 평문 미포함 | ✅ `.env.example` JWT_SECRET 값은 명시적 placeholder `changeme-please-generate-random-32-chars`. 커밋 메시지 7건 검토 — 실 시크릿 0건 |
| §3 | `cat .env`/`echo $TOKEN`/`printenv` 미실행 | ✅ 8 커밋 + 작업 도중 본 명령 0회 |
| §4 | 보안 파일 경로 패턴 차단 | ✅ Write/Edit 도구가 보안 파일 PreToolUse hook으로 자동 차단 |
| §5 | settings.json PreToolUse 훅 동작 | ✅ 본 작업 진행 중 차단 없음 (보안 파일 작성 시도 0회) |
| §6 | /cso 시 시크릿 노출 점검 (해당 phase에서) | DEFER — 본 PR은 N/A. /cso는 별도 phase |

추가 점검:
- `JWT_SECRET` placeholder 형식: ✅ "changeme-please-generate-random-32-chars" — 신규 개발자가 *실 사용 전에 catch 가능*한 명시적 키워드 포함
- `cryptography` 의존성 버전 핀 (48.0.0): ✅ 최신 stable (2026-04). CVE 0건 확인
- `passlib[bcrypt]` 의존성 (5.0.0): ✅ bcrypt 라이브러리 정상 — 후속 이슈 #3에서 hash_password 구현 시 사용

## 4. 가독성 / 단순성

- **`realworld/main.py`**: 47 lines. `create_app()` factory + lifespan + CORS + 1 endpoint. 단순. ✅
- **`realworld/config.py`**: 23 lines. pydantic-settings `BaseSettings` + `@lru_cache get_settings()`. 단순. ✅
- **`realworld/db.py`**: 30 lines. `_build_engine()` private + module-level `engine`/`async_session_maker` + `get_db()`. 표준 SQLAlchemy 2.x async 패턴. ✅
- **`alembic/env.py`**: 64 lines (ruff --fix 후). 공식 async cookbook 패턴 그대로. `target_metadata=None` (빈 init용). ✅
- **`tests/test_health.py`**: 25 lines. 3 시나리오 명확. fixture 명명 직관. ✅
- **`backend/pyproject.toml`**: 60 lines. dependencies + tool.ruff + tool.pytest 명확히 섹션 분리. ✅
- **`.github/workflows/backend-ci.yml`**: 38 lines. 5 step 단일 job. paths 필터 적용 — 무관 변경 시 trigger 안 됨. ✅

불필요한 주석·과도한 추상화·죽은 코드 0건 확인.

## 5. 발견 사항 (3축 OX 분류)

| 발견 | in_scope | blocks_merge | same_area | 처리 |
| --- | --- | --- | --- | --- |
| Q1: contract Before/After 13행 모두 후행 코드 매핑? | O | O | O | PASS (§1 표) |
| Q2: plan §1 7 커밋 DAG가 실 커밋(8 = docs+C1~C7)과 일치? | O | O | O | PASS — 순서·메시지 정규식 모두 통과 |
| Q3: AC-01~AC-07 7 인수 기준 모두 PASS? | O | O | O | PASS — uv sync ✅ / app.title ✅ / alembic 0001 head ✅ / .env.example 6키 ✅ / pytest 3/3 ✅ / health+docs+openapi 200 ✅ / ruff PASS ✅ |
| Q4: 보안 절대 규칙 6항목 전수 통과? | O | O | O | PASS (§3 표) |
| Q5: ADR-0047 양축 워크플로 검증 (로컬 manual reproduction)? | O | O | O | PASS — `uv sync --frozen` + `ruff check` + `ruff format --check` + `alembic upgrade head` + `pytest -v` 5 step 모두 통과 |
| Q6: ADR-0037 v1.1 단일 환경 운영 N/A 사유 명시? | O | O | O | PASS — contract.md §1 + acceptance §3 + 12-scaffolding/python.md §6 모두 명시 |
| Q7: 후속 이슈 진입점 안정화 (Call Sites 7행)? | O | X | O | PASS — Issue #2 alembic down_revision="0001" / Issue #3 Settings.JWT_SECRET / Issue #4 app.include_router 모두 가능 |
| Q8: docs/planning/12-scaffolding/python.md §1·§6 차이 정합 (plan §5 결정 사항)? | X | X | X | DEFER — P13 docs-update에서 분리 정합 (`backend/.env.example` + `backend/data/`로 갱신, scaffolding §1 트리의 루트 경로 → backend/ 하위로 수정) |
| Q9: `.env.example`에 plan §5 결정 추가 키 `CORS_ORIGINS`·`LOG_LEVEL` 명시? | O | X | O | PASS — contract §2 4 키 명세보다 2 추가, plan §5 "결정 발생 항목"에 사전 등록됨. acceptance AC-04는 4 키 검증만 — 추가 2 키는 보너스 |
| Q10: pre-commit `detect-private-key` 훅이 시크릿 누설 catch 가능? | O | X | O | PASS — 후속 이슈 작성자 보호 |

**3축 OX 분석**:
- in_scope=O & blocks_merge=O & same_area=O: 6건 → 모두 PASS
- DEFER 1건(Q8) — same_area=X 사유로 P13 docs-update에서 처리 (`/docs-update` 책임). 머지 차단 안 함.
- 머지 차단 이슈 0건.

## 6. NEEDS-WORK 항목

(없음) — P10 /qa-test --ai 진입 허용.

후속 이슈를 위한 메모 (참고):
- Issue #2 User 모델 추가 시: `down_revision="0001"` 사용 필수
- Issue #3 AuthService 구현 시: `JWT_SECRET == "changeme-please-generate-random-32-chars"`이면 startup 경고 추가 권장 (FRISK-05 완화)
- Issue #7 frontend 스캐폴딩 시: LOCAL.md §3.1 frontend 부팅 검증 추가 (Issue #1에선 placeholder 유지)
- backend-ci.yml: 후속 이슈에서 커버리지 ≥ 80% 강제 step 추가 검토 (Issue #3·#4 머지 후)
