---
doc_type: feature-acceptance
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

# feat-bootstrap-backend — Acceptance Criteria

> Issue #1 — backend 스캐폴딩 인수 기준. PR 머지 게이트(D-06 2단) + DoD 7개 항목.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — Given/When/Then 7건 + DoD 8 항목 (이슈 본문 + RFP §DoD) |

## 1. 인수 기준 (Given/When/Then)

**AC-01 — 의존성 lockfile**
- **Given** fresh checkout (`git clone https://github.com/haeunpark-623/realworld-py && cd realworld-py`)
- **When** `cd backend && uv sync` 실행
- **Then** `backend/uv.lock` 파일 생성 + `backend/.venv/` 생성 + exit code 0 + Python 3.11 핀 적용

**AC-02 — FastAPI 앱 인스턴스 import**
- **Given** AC-01 완료 (uv sync OK)
- **When** `cd backend && uv run python -c "from realworld.main import app; print(app.title)"` 실행
- **Then** stdout에 `RealWorld API` 출력 + exit code 0

**AC-03 — Alembic 마이그레이션 init**
- **Given** AC-02 완료
- **When** `cd backend && uv run alembic upgrade head` 실행
- **Then** `backend/data/realworld.db` SQLite 파일 생성 + `alembic_version` 테이블에 `0001` revision 저장 + exit code 0 + `uv run alembic current`가 `0001 (head)` 출력

**AC-04 — `.env.example` 존재 + 4 필수 키**
- **Given** AC-01 완료
- **When** `cat backend/.env.example` 또는 `Read backend/.env.example`
- **Then** 다음 4개 키가 placeholder 형식으로 정의됨: `DATABASE_URL=...`, `JWT_SECRET=changeme-...`, `JWT_ALG=HS256`, `JWT_EXPIRE_MINUTES=...` (실제 시크릿 평문 없음, 보안 규칙 §3 준수)

**AC-05 — Health check 통합 테스트 PASS**
- **Given** AC-02 완료 + AC-03 완료
- **When** `cd backend && uv run pytest -v` 실행
- **Then** `test_health.py::test_health_returns_ok` PASS + exit code 0 + 최소 1건 테스트 통과

**AC-06 — LOCAL.md §3.1 실 부팅**
- **Given** AC-01 ~ AC-05 완료
- **When** LOCAL.md §3.1 명령 그대로 실행 (`cd backend && uv run uvicorn realworld.main:app --reload --port 8000`)
- **Then** stdout에 `Uvicorn running on http://0.0.0.0:8000` 출력 + 별 터미널에서 `curl -s http://localhost:8000/health` → `{"status":"ok"}` + `curl -sI http://localhost:8000/docs | head -1` → `HTTP/1.1 200 OK`

**AC-07 — Lint + CI 통과**
- **Given** AC-01 ~ AC-06 완료
- **When** `cd backend && uv run ruff check . && uv run ruff format --check .` 실행
- **Then** exit code 0 (위반 0건) + PR open 후 GitHub Actions `backend-ci` 워크플로 status check green

## 2. Definition of Done (D-06)

8개 체크박스 — 이슈 #1 body의 DoD Checklist와 1:1 매핑. **PR body에는 항상 미체크 상태**로 등록 (ADR-0046 §2.3 — Manual verification·DoD coverage는 LLM이 사전 체크 금지). 사람이 머지 직전 수동 체크.

- [ ] **D-06-1** `uv sync` 성공 + `backend/uv.lock` 생성 (AC-01)
- [ ] **D-06-2** `alembic init alembic` 결과 + 빈 init revision (`0001_initial.py`)이 `versions/` 디렉토리에 존재 (AC-03)
- [ ] **D-06-3** `backend/realworld/main.py` — FastAPI app 인스턴스 + `/health` 엔드포인트 + lifespan (AC-02 + AC-06)
- [ ] **D-06-4** `backend/realworld/config.py` — `pydantic-settings.BaseSettings` 기반 `Settings` 클래스 (4 키 매핑)
- [ ] **D-06-5** `backend/realworld/db.py` — `AsyncEngine` + `async_sessionmaker[AsyncSession]` + `get_db()` async generator (AC-03 + 후속 이슈 진입점)
- [ ] **D-06-6** `backend/.env.example` 작성 (AC-04, 보안 규칙 §3 placeholder 형식)
- [ ] **D-06-7** LOCAL.md §3.1 명령 실제 실행 가능 (AC-06)
- [ ] **D-06-8** pre-commit 훅 설치 (`pre-commit install` 명령 안내가 LOCAL.md §3.1에 포함, 로컬 검증)

**PR 본문 추가 체크박스** (ADR-0046 §2.3 — Manual verification 통합 1줄):
- [ ] **Manual verification**: AC-06 8000 포트 부팅 + `/health` + `/docs` 응답 직접 확인 + GitHub Actions 워크플로 로컬 검증 (manual reproduction: `cd backend && uv sync && uv run ruff check . && uv run pytest`)
- [ ] **DoD coverage**: 위 D-06-1 ~ D-06-8 8 항목 모두 만족

## 3. 비기능 인수

| R-ID | 항목 | 검증 방법 | 본 이슈 적용 여부 |
| --- | --- | --- | --- |
| R-N-01 | API p95 < 200ms | seed 100건 + pytest 통합 측정 | **N/A (Issue #5 책임)** — 본 이슈는 health check만 |
| R-N-04 | Python 강제 | pyproject.toml `requires-python = ">=3.11,<3.12"` + uv가 강제 | ✅ AC-01에서 `uv sync` 시 Python 3.11 자동 핀 |
| R-N-05 | 단위/통합 테스트 ≥ 80% (services·deps 한정) | `uv run pytest --cov=realworld/services --cov=realworld/deps --cov-fail-under=80` | **N/A — 본 이슈는 services·deps 0줄.** 후속 이슈 #3·#4부터 측정 정합 시작 |
| R-N-06 | 단일 환경 운영 (dev 1 profile) | 12-scaffolding §6 dev/stg/prod 표에 stg·prod N/A 사유 명시 | ✅ ADR-0037 v1.1 §"단일 환경 운영" 적용 |
| R-N-02 | 보안 (bcrypt + JWT) | `.env.example` JWT 키 4개 + `passlib[bcrypt]` 의존성 pyproject 등록 | ✅ 본 이슈는 의존성·env 키 정의만. 실 구현은 Issue #3 |
| R-N-03 | LOCAL.md 5분 부팅 | LOCAL.md §3.1 명령 실 검증 (AC-06) | ✅ |

## 4. 회귀 인수

- **회귀 영향 화면/엔드포인트**: 없음 — 본 이슈가 *첫* 백엔드 코드. 기존 시나리오 0건.
- **후속 이슈 회귀 방지**:
  - Issue #2 (User 모델 + 마이그레이션)은 본 PR의 `alembic/versions/0001_initial.py`를 `down_revision="0001"`로 연결 → 본 PR의 revision id "0001"이 후속 이슈에서 깨지지 않도록 *고정* (plan §5 결정 사항).
  - Issue #3 (AuthService)는 `realworld.config.Settings.JWT_SECRET` 등 환경 변수명 4개를 *고정 인터페이스*로 사용 → 본 PR `.env.example` 4 키 명명 안정화.
  - Issue #4 (users/articles router)는 `realworld.main.app.include_router(...)` 호출 → 본 PR `app` 인스턴스 위치 안정화.
- **CI 회귀 방지**: backend-ci.yml이 매 PR마다 `uv sync` + `ruff check` + `pytest` 강제 → 후속 이슈에서 의존성 깨짐·lint 위반·테스트 실패 즉시 catch.
- **부팅 자산 동기 회귀 방지**: ADR-0040 LOCAL.md 양축 강제 — 후속 이슈에서 부팅 명령·env 변경 시 LOCAL.md §3.1과 12-scaffolding/python.md §5 동시 갱신 강제.
