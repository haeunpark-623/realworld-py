---
doc_type: feature-plan
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

# feat-bootstrap-backend — Implementation Plan

> Issue #1 — backend/ 스캐폴딩 구현 계획. 7개 커밋 DAG로 분할. AI 페어 가속 환산 30~45분 (= 0.5d).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — 커밋 시퀀스 7개 + 의존성 DAG + 테스트 매핑 + 빌드·실행 검증 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `chore(backend): I-01 uv project + pyproject.toml + lockfile` | `backend/pyproject.toml` (신규) + `backend/uv.lock` (auto) + `backend/.python-version` | (없음 — 의존성만) | 없음 (신규 디렉토리) |
| C2 | `chore(backend): I-01 realworld 패키지 + config + db + main` | `backend/realworld/__init__.py` + `backend/realworld/main.py` + `backend/realworld/config.py` + `backend/realworld/db.py` | (없음 — C5에서 일괄) | 없음 |
| C3 | `chore(backend): I-01 .env.example + .gitignore + data/` | `backend/.env.example` + `backend/.gitignore` + `backend/data/.gitkeep` + 루트 `.gitignore` 갱신 | (없음) | 없음 (env 파일 추가만) |
| C4 | `chore(backend): I-01 alembic init + 0001_initial revision` | `backend/alembic.ini` + `backend/alembic/env.py` + `backend/alembic/script.py.mako` + `backend/alembic/versions/0001_initial.py` | (없음) | 없음 (빈 init) |
| C5 | `test(backend): I-01 conftest + health check 통합 테스트` | `backend/tests/__init__.py` + `backend/tests/conftest.py` + `backend/tests/test_health.py` | `tests/test_health.py::test_health_returns_ok` | 없음 (테스트 추가) |
| C6 | `chore(backend): I-01 ruff + pre-commit + backend-ci 워크플로` | `backend/pyproject.toml` (ruff 섹션 추가) + 루트 `.pre-commit-config.yaml` + 루트 `.github/workflows/backend-ci.yml` | (없음 — CI 검증) | 워크플로 추가만 (기존 0개) |
| C7 | `docs(boot): I-01 LOCAL.md §3.1 실 검증 + 12-scaffolding §5 정합` | 루트 `LOCAL.md` + (필요시) `docs/planning/12-scaffolding/python.md` 부수정 | (없음 — 문서 동기) | 없음 |

**커밋 메시지 규칙**: ADR-0021 `^(feat|fix|chore|docs|test|refactor)\([a-z][a-z0-9,_-]*\): .+` 정규식 통과. 본문에 `Refs #1` 명시 (C1~C7 모두), 최종 PR squash 본문에 `Closes #1` 통합 — `/qa-test --ai` 단계가 생성.

## 2. 의존성 그래프

```
C1 (pyproject + lockfile)
  └─→ C2 (realworld 패키지)
        └─→ C4 (alembic — db.py 사용)
              └─→ C5 (테스트 — main.app + alembic upgrade 필요)
                    └─→ C7 (LOCAL.md 검증 — 전체 부팅 가능 상태)
  └─→ C3 (.env.example — pyproject와 독립, C1 후 합류 가능)
        └─→ C5 (테스트가 .env 또는 기본값 사용)
  └─→ C6 (ruff/pre-commit/CI — C2 코드 존재해야 lint 의미 있음)
        └─→ C7 (CI 통과 후 LOCAL.md 갱신)
```

순환 없음. C1 → C2 → C4 → C5 → C7 단일 critical path. C3·C6는 병행 가능 (현실적으로는 순차 작업).

**Subtask당 1 커밋 원칙** (ADR-0021): 7개 커밋이 각각 자기 검증 통과 (구문 OK + 부팅 가능). 마지막 커밋(C7)이 LOCAL.md §3.1 명령 실 실행 결과를 본문에 1줄로 명시.

## 3. 테스트 매핑

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C5 | `backend/tests/test_health.py::test_health_returns_ok` | Given FastAPI app + TestClient When `GET /health` Then status=200, body=`{"status": "ok"}` (R-N-06 단위 테스트 골격 — health 자체는 통합 성격이지만 본 PR에서 유일한 endpoint이므로 카탈로그 §1에 등재) |
| C5 | (선택) `backend/tests/test_health.py::test_app_openapi_schema_available` | Given app When `GET /docs` Then status=200, content-type=`text/html` (Swagger UI 응답) — DoD `LOCAL.md §3.1` 명령의 `/docs` 확인을 자동화 |
| C5 | (선택) `backend/tests/conftest.py::client fixture` | TestClient + AsyncSession fixture — 후속 이슈(#2~#6)에서 재사용 |

**커버리지 정책**: R-N-06 ≥ 80%는 `realworld/services` + `realworld/deps`에만 적용 (04-srs §R-N-06). 본 이슈는 services·deps 0줄이라 커버리지 측정 N/A. C5는 `uv run pytest` 통과 검증만 요구. 후속 이슈 #3·#4에서 커버리지 측정 정합 시작.

**테스트 카탈로그 (13/02-catalog) 동기**: 본 이슈는 R-/F-ID 신규 추가 없음 → 카탈로그 변경 N/A (P13 docs-update에서 `check-test-catalog-sync.sh` WARN 0건 예상).

## 4. 빌드·실행 검증 단계

```bash
# C1 후 — 의존성 lock
cd backend
uv sync
test -f uv.lock && echo "uv.lock OK"

# C2 후 — 구문 검증
uv run python -c "from realworld.main import app; print(app.title)"
# 기대: "RealWorld API" 등 app.title 출력

# C3 후 — env 파일
test -f backend/.env.example && echo ".env.example OK"
test -f backend/.gitignore && echo "backend/.gitignore OK"

# C4 후 — alembic
uv run alembic upgrade head
test -f backend/data/realworld.db && echo "DB file OK"
uv run alembic current
# 기대: "0001 (head)" 출력

# C5 후 — pytest
uv run pytest -v
# 기대: test_health_returns_ok PASSED

# C6 후 — lint + format
uv run ruff check .
uv run ruff format --check .

# C7 후 — LOCAL.md §3.1 실 부팅 (수동, gstack /browse 또는 curl)
# Terminal 1
cd backend && uv run uvicorn realworld.main:app --reload --port 8000 &
# Terminal 2
sleep 3
curl -s http://localhost:8000/health
# 기대: {"status":"ok"}
curl -sI http://localhost:8000/docs | head -1
# 기대: HTTP/1.1 200 OK
```

**AI 게이트 6번째 축 (dev/stg/prod 3 profile 부팅 검증)**:
- dev profile: 위 절차로 실 부팅 검증 ✅
- stg/prod: **N/A — 단일 환경 운영** (ADR-0037 v1.1 + RFP §NFR-06). PR Manual verification 절에 사유 명시.

**ADR-0047 GitHub Actions 워크플로 양축 검증**:
- C6에서 `.github/workflows/backend-ci.yml` 신규 추가 → 양축 검증 BLOCK.
- 로컬 검증: act 미설치 가정 시 manual reproduction — `cd backend && uv sync && uv run ruff check . && uv run pytest`로 워크플로 step 재현.
- GitHub 검증: PR open 후 workflow run 결과 확인.
- 증거: PR body `### Manual verification` 절에 1줄 `- [ ] GitHub Actions 워크플로 로컬 검증 (manual reproduction): <명령> → <결과>`.

## 5. 점진 합의 / 결정 발생 항목

- **DB 파일 위치**: `backend/data/realworld.db` 채택 (scaffolding §6 `./data/realworld.db` + uvicorn cwd=`backend/`). 루트 `data/`가 아님 — backend 격리 우선. scaffolding §1 트리의 루트 `data/`는 P13에서 수정 권고 (별도 docs-update 또는 본 PR C7에서 부수정).
- **`.env.example` 위치**: `backend/.env.example` 채택 (이슈 #1 body 명시 + ADR-0037 §"부팅 자산" path 합치). scaffolding §1 트리의 루트 `.env.example`은 frontend·backend 통합 위치였으나 backend 격리로 변경. P13에서 scaffolding §1·§6 정합 갱신.
- **`.python-version` 추가**: Python 3.11 핀 (uv가 자동 인식). pyproject.toml `requires-python = ">=3.11,<3.12"`과 양축.
- **OpenAPI 설정**: `app = FastAPI(title="RealWorld API", version="0.1.0", openapi_url="/openapi.json", docs_url="/docs")`. 기본값 그대로 + title/version만 명시.
- **lifespan**: `@asynccontextmanager` 기반 lifespan에서 startup 시 DB 연결 검증 (`engine.dispose` 등록만). 본 PR은 health check만 — 연결 풀 warmup 등 후속 이슈로.
- **JWT_SECRET .env.example 형식**: `JWT_SECRET=changeme-please-generate-random-32-chars`. placeholder 명시 (보안 규칙 §3 — 실제 시크릿 평문 금지). 후속 이슈 #3에서 startup 시 `JWT_SECRET == "changeme..."` 경고 추가 검토.
- **pre-commit 설치 강제 여부**: pre-commit은 권고만. CI(GitHub Actions)에서 ruff check를 강제 → 로컬 설치 누락 시에도 PR 단계에서 catch. C7 LOCAL.md §3.1에 `pre-commit install` 명령 안내만 추가.
- **backend-ci.yml 트리거 경로**: `paths: ['backend/**', '.github/workflows/backend-ci.yml']`. 루트 문서/frontend 변경 시 backend CI 미트리거 — efficiency 최적화. 후속 이슈에서 frontend-ci.yml은 별도 추가.
