# realworld-py — 로컬에서 켜기

> **목적**: 이 저장소를 처음 clone한 사람이 *이 파일 1개*만 따라 하면 dev profile로 로컬에서 부팅 가능하도록 한다.
> **정본 위치**: 이 파일은 newProject 루트의 *유저 facing* 정본. 부팅 자산 *정의*의 SoT는 `docs/planning/12-scaffolding/python.md` §7. 본 LOCAL.md와 `12-scaffolding/python.md`는 매 PR에서 동기 갱신된다 (ADR-0037 v1.1 + ADR-0040).
> **단일 환경 운영 (ADR-0037 v1.1)**: 본 프로젝트는 RFP §NFR-06에 따라 *dev 1 profile만* 운영한다. stg/prod는 N/A — §3.2·§3.3은 placeholder만 유지.

---

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — `/flow-design` Phase 2/4 진행 중 §1~§6 채움 (FastAPI + React/Vite 풀스택 monorepo, 단일 환경 운영, (e) 워크스페이스별 .env 분리 채택) |
| v0.2 | 2026-05-20 | woosung.ahn@bespinglobal.com | Issue #1 부팅 골격 완성 후 §3.1 backend 명령 실 검증. `/health` `/docs` `/openapi.json` 모두 200 응답 확인. frontend는 Issue #7에서 검증 예정 (해당 부분은 placeholder 유지) |
| v0.3 | 2026-05-21 | woosung.ahn@bespinglobal.com | Issue #7 frontend 워크스페이스 셋업 — §1·§2·§3.1·§4·§5.7 pnpm → **npm** 갱신 (pnpm 미설치 점진 합의, feat-frontend-scaffold/contract §1 + plan §5 trace). frontend dev 서버 5173 부팅 실 검증 (`VITE v5.4.21 ready in 346ms`). §4 lockfile `pnpm-lock.yaml` → `package-lock.json`. §1.5.1·§1.5.3·§1.5.5의 pnpm 언급도 npm 갱신. §3.1 frontend 부팅 검증 표기 추가 |

---

## 1. 사전 요구사항

- **언어/런타임**: Python 3.11 (백엔드) + Node.js 20 LTS 이상 (Vite 5 요구 사항, 본 프로젝트는 Node 24.x로 실 검증)
- **패키지 매니저**: `uv` (Astral, Python) + **`npm` 11.x (Node)** — Issue #7 점진 합의로 pnpm 대신 npm 채택
- **DB**: SQLite (file-based, 별 설치 불필요 — `aiosqlite` 드라이버가 함께 설치됨)
- **OS 가정**: macOS / Linux / Windows 11 (PowerShell 또는 WSL2)
- **컨테이너**: 미사용 (학습 컨텍스트, native 부팅만)

사전 설치 (한 번만):
```bash
# uv 설치 (https://github.com/astral-sh/uv)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Node.js는 LTS 권장 (https://nodejs.org/). npm은 Node 설치 시 함께 설치됨.
node --version    # v20.x+ 필요
npm --version     # 11.x 권장
```

---

## 1.5 흔한 함정 — *사전* 안내

### 1.5.1 워크스페이스별 .env 분리 채택 — 루트 cwd 함정 없음

본 프로젝트는 풀스택 monorepo + FE/BE가 다른 stack (`npm`/`Vite` ↔ `uv`/`FastAPI`) 조합이므로 **§1.5.1 패턴 (e) 워크스페이스별 .env 완전 분리** 채택.

- 구조: 루트에 `.env*` 없음. 각 워크스페이스가 자기 `.env.example` 보유
  - `backend/.env.example`
  - `frontend/.env.example`
- 호출: 각 워크스페이스가 stack native 메커니즘으로 *자기 .env* 자동 로드
  - 백엔드: pydantic-settings의 `Settings(_env_file=".env")` (uv 부팅 cwd가 backend/이므로 자동 로드)
  - 프론트엔드: Vite는 cwd의 `.env` 자동 로드 (`VITE_` prefix만 클라이언트 노출)
- 단일 환경 운영이므로 `.env.dev/stg/prod` 분기 불필요 — `.env` 1개로 충분

본 프로젝트 채택: **(e) — 워크스페이스별 .env 분리**

### 1.5.2 ORM 최초 migration — (a) 분리형 채택

- **(a) 분리형**: dev iteration용 `alembic upgrade head` (스키마 적용) ≠ 운영 release용 (단일 환경이라 동일하게 사용)
- 함정: 모델 변경 후 `alembic revision --autogenerate -m "<msg>"` 로 마이그레이션 파일 생성 안 하면 `alembic upgrade head`는 *기존 파일만* 적용 — DB가 모델 변경 미반영 상태로 남음
- 최초 1회: `alembic revision --autogenerate -m "init"` 후 `alembic upgrade head`. 이후 모델 변경마다 revision 생성

본 프로젝트 채택 분류: **(a) 분리형**
- dev 명령: `uv run alembic upgrade head`
- 단일 환경 운영이라 stg/prod 분기 없음

### 1.5.3 SPA frontend stg/prod 정적 서버 — N/A (단일 환경 운영)

단일 환경 운영이라 stg/prod 부팅 N/A. dev만 `npm run dev` (Vite dev server) 사용.

### 1.5.4 컨테이너 — N/A (학습 컨텍스트, native 부팅만)

본 프로젝트는 Docker 미사용. 학습 컨텍스트에서 native 부팅(`uv run uvicorn ...` + `pnpm dev`) 만으로 충분. 후속 학습 시 도입 검토.

### 1.5.5 multi-stack 의존성 설치 — Python uv + Node npm

본 프로젝트는 Gradle/Maven 등 *parent-aware* 빌드 도구를 사용하지 않으므로 §1.5.5 multi-project syntax 함정은 N/A. 단, **stack별로 자기 디렉토리에서 자기 도구 호출** 원칙 동일 적용:

```bash
# 의존성 설치 — 각 stack별 1줄
(cd backend && uv sync)
(cd frontend && npm install)
```

본 프로젝트 채택: **단일 stack 아님(FE+BE 분리), parent-aware 빌드 도구 미사용 → N/A**

---

## 2. 처음 한 번 셋업 (Initial Setup)

```bash
# 1) clone
git clone <repo-url>
cd realworld-py

# 2) 의존성 설치 — 멀티 stack, 각 워크스페이스에서 자기 도구 호출
(cd backend && uv sync)
(cd frontend && npm install)         # Issue #7: npm 채택 (점진 합의)

# 3) 환경 변수 파일 준비 — (e) 워크스페이스별 분리 채택, 단일 환경이라 .env 1개씩
cp backend/.env.example  backend/.env
cp frontend/.env.example frontend/.env

# backend/.env 안의 JWT_SECRET을 실제 랜덤 값으로 채움 (최소 32자, HS256)
# 예: python -c "import secrets; print(secrets.token_urlsafe(32))"
# frontend/.env 의 VITE_API_BASE_URL은 기본 /api (Vite proxy 사용) 유지

# 4) DB 스키마 적용 — (a) 분리형, 최초 1회
(cd backend && uv run alembic upgrade head)
# ⚠️ 함정 (§1.5.2): 모델 변경 후 'alembic revision --autogenerate'로 마이그레이션 파일 생성 안 하면
#    upgrade head는 기존 파일만 적용해 DB가 모델과 불일치 상태로 남음.

# 5) seed 데이터 (선택, R-N-01 측정용)
(cd backend && uv run python -m scripts.seed_articles)
# 게시글 100건 생성 — 게시글 목록 API p95 < 200ms 측정 준비
```

---

## 3. Profile별 부팅 명령

> 본 프로젝트는 **dev 1 profile만 운영** (RFP §NFR-06, ADR-0037 v1.1 단일 환경 운영). §3.2·§3.3은 N/A.

### 3.1 dev profile (로컬 개발)

```bash
# 옵션 A: 워크스페이스 직접 실행 — 각 1터미널씩, hot reload 동작
# 터미널 1 (backend)
cd backend
uv run uvicorn realworld.main:app --reload --host 0.0.0.0 --port 8000

# 터미널 2 (frontend) — Issue #7부터 사용 가능
cd frontend
npm run dev

# 브라우저
open http://localhost:5173
# Vite dev server가 /api/* 요청을 http://localhost:8000으로 proxy (vite.config.ts)
```

- **기대 출력 (backend)**: `INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)` + `INFO:     Application startup complete.`
- **기대 출력 (frontend)**: `VITE v5.4.21  ready in 346 ms` + `➜  Local:   http://localhost:5173/`
- **환경 변수 출처**: `backend/.env` + `frontend/.env`
- **DB**: `backend/data/realworld.db` (SQLite file)
- **Hot reload**: O (backend `--reload`, frontend Vite HMR)
- **검증 확인 (Issue #1·#7)**: backend는 실 검증 완료 — `curl http://localhost:8000/health` → `{"status":"ok"}` (200), `curl -I http://localhost:8000/docs` → `HTTP/1.1 200 OK`. frontend는 Issue #7 머지 시 실 검증 완료 — `npm run build` 41 modules in 1.38s + `npm run dev` Vite ready in 346ms. 브라우저 6 라우트 placeholder 진입 가능.

### 3.2 stg profile (스테이징)

**N/A — 단일 환경 운영 (RFP §NFR-06)**. stg=dev 공유. 별도 부팅 명령 없음.

### 3.3 prod profile (프로덕션)

**N/A — 단일 환경 운영 (RFP §NFR-06)**. prod 학습은 후속 과제. 클라우드 배포는 Out of Scope (RFP §5).

---

## 4. 부팅 자산 (Runnability Assets)

> 본 표는 `docs/planning/12-scaffolding/python.md` §7과 동기. 자산 변경 시 양쪽 모두 갱신.

| 자산 | 경로 | 변경 trigger | 갱신 책임 |
|---|---|---|---|
| 환경 변수 템플릿 | `backend/.env.example` + `frontend/.env.example` (★1) | 새 환경 변수 추가 | 변수를 도입한 이슈 |
| 스키마 적용 (dev iteration) | `(cd backend && uv run alembic upgrade head)` — 모델 변경 시 `alembic revision --autogenerate -m "<msg>"` 선행 | dev 환경 schema 변경 | 모델 변경 이슈 |
| DB migrations (stg/prod release) | `backend/alembic/versions/` — 단일 환경이라 dev iteration과 동일. N/A — stg/prod 미운영 | 운영 release용 migration 작성 | (단일 환경 운영이라 N/A) |
| lockfile | `backend/uv.lock` + `frontend/package-lock.json` (★2 — Issue #7부터, npm 채택) | 의존성 추가/변경 | 의존성 도입 이슈 |
| 설치/seed scripts | `backend/scripts/seed_articles.py` | seed 데이터 변경 | seed 변경 이슈 |
| 부팅 명령 | 본 LOCAL.md §3.1 + `backend/pyproject.toml` (uv scripts) + `frontend/package.json scripts.dev` (npm scripts, Issue #7) | 명령 변경 | 명령 변경 이슈 |
| 컨테이너 정의 (선택) | 미사용 — N/A | N/A | N/A |

> **★1 monorepo 분리 footnote**: §1.5.1 (e) 채택으로 .env 템플릿이 워크스페이스별로 1개씩 분리. 단일 환경 운영이라 profile 분기 없음(`.env.example` 1개씩).
> **★2 lockfile footnote**: stack이 다르므로 lockfile 2종(`uv.lock` Python + `package-lock.json` Node) 공존. 둘 다 commit + AI 게이트가 누락된 lockfile 갱신을 BLOCK. Issue #7 점진 합의 — pnpm 대신 npm 채택.

---

## 5. 자주 발생하는 문제 (Troubleshooting)

> newProject 도입 후 부팅 시 발견되는 문제를 *이슈 단위*로 본 절에 누적.

### 5.1 포트 충돌 (`EADDRINUSE` / `Address already in use`)

```bash
# macOS/Linux — 8000(backend) 또는 5173(frontend) 점유 프로세스 확인
lsof -i :8000
lsof -i :5173

# Windows PowerShell
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
```

해결: 점유 프로세스 종료 또는 다른 포트로 변경(`--port` 옵션). vite는 `vite.config.ts`의 `server.port` 또는 환경 변수.

### 5.2 환경 변수 누락 (`X is required` / `JWT_SECRET is required`)

- `backend/.env` 와 `frontend/.env` 가 둘 다 존재하는지 (`ls backend/.env frontend/.env`)
- `JWT_SECRET` 최소 길이 — HS256은 32자 미만 시 `WeakKeyException`. `python -c "import secrets; print(secrets.token_urlsafe(32))"` 로 생성
- pydantic-settings가 `Settings(_env_file=".env")` 로 cwd 기준 로드하므로 `cd backend` 위치에서 부팅 (LOCAL.md §3.1 명령 그대로)

### 5.3 DB 연결 실패 / `OperationalError: no such table`

- SQLite 파일 존재 확인: `ls backend/data/realworld.db` (없으면 §2 단계 4 미실행)
- `alembic upgrade head` 미실행 → `(cd backend && uv run alembic upgrade head)` 실행
- 모델 변경 후 마이그레이션 미생성 (§1.5.2) → `(cd backend && uv run alembic revision --autogenerate -m "<msg>")` → `alembic upgrade head`
- `data/` 디렉토리 자체가 .gitignore라서 fresh checkout 후 미생성 → `mkdir -p backend/data` 후 재시도

### 5.4 monorepo cwd에서 `DATABASE_URL not found`

본 프로젝트는 (e) 워크스페이스별 .env 분리 채택이라 *루트 cwd 함정 자체가 없다*. 단, 워크스페이스 위치를 잘못 하면 동일 증상.

증상:
```bash
$ cd realworld-py && uv run alembic upgrade head
... KeyError: 'DATABASE_URL' ...
```

원인: backend cwd가 아닌 루트 cwd에서 실행 → `.env`를 못 찾음.

해결: `(cd backend && uv run alembic upgrade head)` — 항상 backend cwd에서.

### 5.5 컨테이너 베이스 이미지 함정

**N/A** — 본 프로젝트는 Docker 미사용 (§1.5.4 N/A).

### 5.6 multi-stack 의존성 설치 / Gradle multi-project syntax 함정

**N/A** — 본 프로젝트는 Gradle/Maven 등 parent-aware 빌드 도구 미사용. uv + npm 조합으로 워크스페이스별 직호출 (Issue #7).

### 5.7 CORS 에러 (`Access-Control-Allow-Origin missing`)

`frontend (5173) → backend (8000)` 호출 시 발생. FastAPI 측 `CORSMiddleware` 가 `CORS_ORIGINS` 환경변수 값(기본 `http://localhost:5173`)을 허용하도록 설정되어 있어야 함. `backend/.env` 의 `CORS_ORIGINS` 값 확인.

또는 Vite proxy 사용 시 (`vite.config.ts` 의 `server.proxy`) CORS 미발생. 본 프로젝트 권장은 Vite proxy 채택 — `frontend/.env` 의 `VITE_API_BASE_URL=/api` 로 두면 됨.

### 5.8 pytest 커버리지 80% 미달 (`coverage X% < min 80%`)

- 적용 범위 확인: `pytest.ini` 또는 `pyproject.toml [tool.pytest.ini_options]` 의 `--cov=realworld/services --cov=realworld/deps`
- 누락된 모듈을 04-srs §R-N-06 적용 범위(UserService/ArticleService/CommentService/권한 미들웨어)와 대조
- 적용 범위 외(routers·schemas·models)는 측정에서 제외해야 함. 04-srs §R-N-06 본문 재확인

### 5.9 (이슈별 추가 — 발견 시점에 본 절에 누적)

---

## 6. 외부 의존 (선택)

본 프로젝트는 **외부 서비스 의존 0건**. 이메일·SMS·결제·OAuth·푸시·S3 모두 Out of Scope (RFP §5, 06-architecture §3).

---

## 7. 본 문서 갱신 책임 (메타)

- **누가**: 부팅 자산을 변경하는 이슈의 PR 작성자(에이전트 또는 사람)
- **언제**: 같은 PR 안에서 갱신. 별 hotfix PR로 미루지 않음 (ADR-0037 §2.3)
- **검증**: AI 게이트 6번째 축이 (a) 부팅 자산 diff 여부, (b) 본 LOCAL.md 갱신 여부를 동시 확인. 한쪽만 변경 시 BLOCK
- **상위 SoT 동기**: 본 절차가 `docs/planning/12-scaffolding/python.md` §7과 다르면 `/docs-update`가 정합 검수에서 WARN. 양쪽 동기가 우선
