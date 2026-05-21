---
doc_type: scaffolding
version: v0.6 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: C
related:
  R-ID: [R-F-01, R-F-02, R-F-04, R-F-06, R-N-01, R-N-04, R-N-06]
  F-ID: [F-01, F-02, F-03, F-04]
  supersedes: null
---

# realworld-py — Scaffolding

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.6 | 2026-05-21 | woosung.ahn@bespinglobal.com | Issue #5 진입 — §1 트리에 `scripts/__init__.py` 명시 + `scripts/seed_articles.py` 실제 도입 표기 (멱등 seed: User 10 + Article 100 + Tag 5, random.seed(42) 고정) + `tests/integration/test_performance.py` 실제 도입 표기 (R-N-01 p95 < 200ms 측정 — 실측 p95=4.24ms PASS). pyproject.toml ruff per-file-ignores `scripts/** = [S105, S311]` 추가 (dev seed 공통 password + random.seed 재현성). 빌드·실행 §5 변경 0 (v0.5에서 seed 명령 이미 명시) |
| v0.5 | 2026-05-21 | woosung.ahn@bespinglobal.com | Issue #4 진입 — §1 트리에 `models/article.py`(Article + Tag + article_tags) + `repositories/article.py` + `services/article.py` + `utils/slug.py` + `schemas/{__init__,user,article}.py` + `routers/{__init__,users,articles}.py` 실제 도입 표기 + `alembic/versions/0003_articles_tags.py` + `tests/integration/{__init__,conftest,test_users_routes,test_articles_routes}.py` 추가. errors.py exception_handler `main.py`에 inline 등록 명시 (handler 모듈 분리 비목표) |
| v0.4 | 2026-05-21 | woosung.ahn@bespinglobal.com | Issue #3 진입 — §1 트리에 `utils/{__init__,security,jwt}.py` + `services/{__init__,auth}.py` + `deps/{__init__,auth}.py` + `errors.py` 실제 도입 표기 + `tests/unit/test_{security,jwt,auth_service}.py` 추가. errors.py는 클래스 정의만 (handler 등록은 I-04) 명시 |
| v0.3 | 2026-05-20 | woosung.ahn@bespinglobal.com | Issue #2 머지 진입 — §1 트리에서 `tests/unit/test_user_repo.py` 명시 (현 PR 추가) + `models/base.py`·`models/user.py`·`repositories/user.py` 실제 도입 확인 (v0.1 트리에서 이미 명시). v0.4에서 후속 모델·repo 도입 시 갱신 |
| v0.2 | 2026-05-20 | woosung.ahn@bespinglobal.com | Issue #1 머지 진입 후 정합 갱신 — §1 트리에서 backend/ 하위로 `.env.example`·`data/`·`.gitignore`·`.python-version`·`.pre-commit-config.yaml` 위치 명시(루트 위치 placeholder 제거) / §6 DATABASE_URL 경로 명시 (backend cwd 기준) + JWT_ALG/JWT_EXPIRE_MINUTES 본 PR 채택 키명 반영 / §1 backend-ci.yml + 기존 워크플로 2건 추가 |
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, Python + FastAPI 백엔드 + frontend 큰 그림. ADR-0037 v1.1 단일 환경 운영 명시 / ADR-0040 LOCAL.md 양축) |

## 1. 디렉토리 트리

```
realworld-py/
├── backend/
│   ├── pyproject.toml              # uv 패키지·도구 설정
│   ├── uv.lock                     # 의존성 lockfile
│   ├── .python-version             # Python 3.11 핀 (uv 자동 인식, Issue #1)
│   ├── .env.example                # 환경 변수 템플릿 — backend 워크스페이스 분리 채택 (Issue #1, (e) §1.5.1)
│   ├── .gitignore                  # backend 한정 (`.env`, `.venv/`, `data/*`, `__pycache__/` 등 — Issue #1)
│   ├── data/                       # SQLite 파일 (.gitkeep만 추적, `*.db` ignore — Issue #1)
│   ├── alembic.ini                 # Alembic 마이그레이션 설정
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/               # migration 파일 디렉토리 (stg/prod release용)
│   ├── realworld/                  # 백엔드 메인 패키지 (모듈명)
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI 앱 인스턴스 + 라우터 등록
│   │   ├── config.py               # pydantic-settings (Settings 클래스)
│   │   ├── db.py                   # AsyncEngine·Session factory
│   │   ├── deps/
│   │   │   ├── __init__.py         # (Issue #3)
│   │   │   └── auth.py             # require_auth (Issue #3)
│   │   ├── routers/
│   │   │   ├── __init__.py         # (Issue #4)
│   │   │   ├── users.py            # POST /api/users · /login · GET /api/user (Issue #4)
│   │   │   ├── articles.py         # /api/articles 5개 라우트 (Issue #4)
│   │   │   └── comments.py         # /api/articles/{slug}/comments 4개 라우트 (Issue #5/#6)
│   │   ├── services/
│   │   │   ├── __init__.py         # (Issue #3)
│   │   │   ├── auth.py             # AuthService (Issue #3)
│   │   │   ├── article.py          # ArticleService (Issue #4 — list/get_by_slug/create/update/delete + 작성자 검증)
│   │   │   └── comment.py          # CommentService (Issue #5/#6)
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # UserRepo 4 메서드 (Issue #2 + find_by_id Issue #3)
│   │   │   ├── article.py          # ArticleRepo 6 메서드 + selectinload N+1 회피 (Issue #4)
│   │   │   └── comment.py          # (Issue #5/#6)
│   │   ├── models/
│   │   │   ├── __init__.py         # User + Article + Tag + article_tags re-export (Issue #2·#4)
│   │   │   ├── base.py             # DeclarativeBase (Issue #2)
│   │   │   ├── user.py             # User 모델 (Issue #2)
│   │   │   ├── article.py          # Article + Tag + article_tags M2M secondary (Issue #4)
│   │   │   └── comment.py          # Comment 모델 (FK ondelete=CASCADE) (Issue #5/#6)
│   │   ├── schemas/
│   │   │   ├── __init__.py         # (Issue #4)
│   │   │   ├── user.py             # UserCreateRequest, UserLoginRequest, UserResponse (Issue #4 — RealWorld 래핑)
│   │   │   ├── article.py          # ArticleCreate/Update + View/Response + ListResponse + ProfileEmbed (Issue #4)
│   │   │   └── comment.py          # (Issue #5/#6)
│   │   ├── utils/
│   │   │   ├── __init__.py         # (Issue #3)
│   │   │   ├── security.py         # bcrypt hash_password / verify_password (Issue #3)
│   │   │   ├── jwt.py              # encode / decode JWT (Issue #3)
│   │   │   └── slug.py             # kebab-case + 숫자 suffix (Issue #4)
│   │   └── errors.py               # 도메인 예외 클래스 + RealWorldError handler `main.py` inline 등록 (Issue #3 클래스 / Issue #4 handler. InvalidCredentials.status_code 422 — Issue #4 정합 갱신)
│   ├── scripts/
│   │   ├── __init__.py             # (Issue #5)
│   │   └── seed_articles.py        # 게시글 100건 + 사용자 10명 + 태그 5종 멱등 시드 (Issue #5, random.seed(42))
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py             # pytest fixture (DB, app, client, user factory)
│       ├── unit/
│       │   ├── test_user_repo.py     # UserRepo 3 메서드 (Issue #2)
│       │   ├── test_security.py      # bcrypt hash/verify 3 (Issue #3)
│       │   ├── test_jwt.py           # encode/decode + 만료 + 변조 3 (Issue #3)
│       │   ├── test_auth_service.py  # register 3 / authenticate 2 / get_current_user 3 (Issue #3)
│       │   ├── test_article_service.py  # 8 케이스 — create + slug 충돌 / list / get / update 본인·타인 / delete 본인·타인 (Issue #4)
│       │   ├── test_comment_service.py  # (Issue #5/#6)
│       │   ├── test_auth_middleware.py  # (require_auth 단위 검증 — DEFER, AuthService.get_current_user 8건이 cover)
│       │   └── test_slug.py            # 5 케이스 — slugify 3 + unique_slug 2 (Issue #4)
│       └── integration/
│           ├── __init__.py             # (Issue #4)
│           ├── conftest.py             # AsyncClient + dependency_overrides[get_db] in-memory aiosqlite + register_user 헬퍼 (Issue #4)
│           ├── test_users_routes.py    # 7 케이스 — register happy/422 dup/422 short + login happy/422 invalid + GET /user happy/401 (Issue #4)
│           ├── test_articles_routes.py # 12 케이스 — list happy/?author= 필터/unknown 빈/detail happy/404/POST happy+401+slug 충돌 -2/PUT happy+403/DELETE 204+follow-up 404+403 (Issue #4)
│           ├── test_comments_routes.py # (Issue #5/#6)
│           └── test_performance.py     # R-N-01 p95 측정 (Issue #5)
├── frontend/
│   ├── package.json
│   ├── pnpm-lock.yaml              # FE lockfile (pnpm 가정)
│   ├── vite.config.ts
│   ├── tailwind.config.js          # Tailwind CSS 설정
│   ├── postcss.config.js
│   ├── tsconfig.json
│   ├── index.html
│   └── src/
│       ├── main.tsx                # React 진입점 (stylesheet import)
│       ├── App.tsx                 # 라우터 (S-01~S-06)
│       ├── index.css               # Tailwind directives (@tailwind base/components/utilities)
│       ├── api/
│       │   └── client.ts           # M-FE-ApiClient (fetch 래퍼)
│       ├── store/
│       │   └── auth.ts             # M-FE-AuthStore (zustand)
│       ├── pages/                  # M-FE-Pages
│       │   ├── HomePage.tsx        # S-01
│       │   ├── ArticlePage.tsx     # S-02
│       │   ├── EditorPage.tsx      # S-03
│       │   ├── LoginPage.tsx       # S-04
│       │   ├── RegisterPage.tsx    # S-05
│       │   └── ProfilePage.tsx     # S-06
│       ├── components/             # M-FE-Components
│       │   ├── Header.tsx
│       │   ├── ArticleCard.tsx
│       │   ├── CommentItem.tsx
│       │   ├── Button.tsx
│       │   ├── Input.tsx
│       │   └── Modal.tsx
│       └── types/
│           └── api.ts              # RealWorld spec 응답 타입
├── .gitignore
├── .pre-commit-config.yaml          # ruff + 일반 6 훅 (Issue #1 채택)
├── .github/
│   └── workflows/
│       ├── backend-ci.yml           # backend PR/push 트리거 — uv sync + ruff + alembic + pytest (Issue #1)
│       ├── issue-pr-title-lint.yml  # ADR-0021 정규식 검증
│       └── sync-issue-labels.yml    # FSM 라벨 sync
├── LOCAL.md                         # 부팅 가이드 (사용자 정본, ADR-0040)
├── CLAUDE.md                        # 툴킷 지침
├── README.md                        # 프로젝트 개요
├── RFP.md                           # 요구사항
└── docs/planning/                   # 14 산출 문서
```

## 2. 패키지 명명 규칙

- **backend Python 패키지 루트**: `realworld` (단일 패키지). `backend/realworld/` 하위에 모든 도메인 모듈 배치.
- **import 경로 예**: `from realworld.services.auth import AuthService`, `from realworld.models.user import User`, `from realworld.routers.articles import router`.
- **frontend TS alias**: `@/` → `frontend/src/`. 예: `import { ArticleCard } from '@/components/ArticleCard';`.
- 11-coding-conventions §1 명명 규칙(파일/모듈/클래스)을 정본으로 따른다.

## 3. 디자인 패턴 결정

- **선택 패턴**: **Layered** (백엔드) — `router → service → repository → model` 4계층.
  - `router`: HTTP·검증·직렬화만
  - `service`: 비즈니스 로직·트랜잭션·도메인 예외 발생
  - `repository`: SQLAlchemy 쿼리 캡슐화·eager loading 정의
  - `model`: SQLAlchemy declarative
- **이유**:
  - 학습 컨텍스트 + 2일 마감 + 9개 모듈 규모에서 Layered가 가장 익히기 쉽다. DDD·Hexagonal은 학습 부담 초과.
  - FastAPI 공식 예제·튜토리얼이 모두 Layered 구조 — 참고 자료가 풍부.
  - R-N-05(raw SQL 금지) + R-N-06(서비스 모듈 단위 테스트 ≥ 80%) 모두 service·repository 분리 시 자연스럽게 충족.
- **프론트엔드 패턴**: feature-based의 단순화 변형 — `pages/` + `components/` + `api/` + `store/` + `types/`. Atomic·FSD는 학습 부담 초과.

## 4. 모듈 경계 (08-lld-module-spec와 fan-out)

08-lld-module-spec의 5개 백엔드 모듈은 본 디렉토리 구조에서 다음과 같이 매핑된다.

| 08 모듈 | 08 §1 위치 | 본 구조 위치 | 비고 |
|---|---|---|---|
| M-API-Router | 08 §1.1 | `backend/realworld/routers/` (`users.py`·`articles.py`·`comments.py`) + `errors.py` | FastAPI APIRouter 인스턴스 3개. errors.py가 exception_handlers 등록 |
| M-Auth-Service | 08 §1.2 | `backend/realworld/services/auth.py` + `utils/security.py` + `utils/jwt.py` | 비즈니스 로직과 보안 유틸 분리 |
| M-Article-Service | 08 §1.3 | `backend/realworld/services/article.py` + `utils/slug.py` | slug 유틸은 분리 |
| M-Comment-Service | 08 §1.4 | `backend/realworld/services/comment.py` | 단일 파일 |
| M-Auth-Middleware | 08 §1.5 | `backend/realworld/deps/auth.py` | FastAPI Depends 함수 2개 (require_auth, require_author) |
| (공통) Repository | 08 §3 | `backend/realworld/repositories/` (`user.py`·`article.py`·`comment.py`) | SQLAlchemy 쿼리 |
| (공통) Models | 08 §3 | `backend/realworld/models/` | SQLAlchemy declarative |
| (공통) Schemas | 08 §3 | `backend/realworld/schemas/` | Pydantic |

## 5. 빌드·실행

> **정본 양축**: 본 §5(SoT) + 루트 `LOCAL.md §3` (사용자 facing). 매 PR 동시 갱신 (ADR-0040). 호출 방식은 native script 직호출 (ADR-0041 — wrapper 미사용).

### 5.1 백엔드 (FastAPI + uv)

```bash
# 의존성 설치 (lockfile 기반, fresh checkout)
cd backend
uv sync

# DB 초기화 (dev iteration — Alembic upgrade head)
uv run alembic upgrade head

# 게시글 100건 시드 (선택, R-N-01 측정용)
uv run python -m scripts.seed_articles

# 개발 서버 부팅 (포트 8000, hot reload)
uv run uvicorn realworld.main:app --reload --host 0.0.0.0 --port 8000

# 단위 + 통합 테스트
uv run pytest

# 커버리지 (R-N-06 ≥ 80% 측정)
uv run pytest --cov=realworld/services --cov=realworld/deps --cov-fail-under=80

# 린트 + 포맷
uv run ruff check .
uv run ruff format --check .
uv run black --check .
```

### 5.2 프론트엔드 (React + Vite + pnpm)

```bash
# 의존성 설치 (lockfile 기반)
cd frontend
pnpm install --frozen-lockfile

# 개발 서버 부팅 (포트 5173, hot reload)
pnpm dev

# 타입 체크 + 린트
pnpm tsc --noEmit
pnpm eslint .

# 프로덕션 빌드 (학습 컨텍스트에선 선택, 부팅 검증용)
pnpm build
```

### 5.3 전체 동시 부팅 (LOCAL.md §3과 동기)

```bash
# 터미널 1
cd backend && uv sync && uv run alembic upgrade head && uv run uvicorn realworld.main:app --reload --port 8000

# 터미널 2
cd frontend && pnpm install --frozen-lockfile && pnpm dev

# 브라우저: http://localhost:5173
# Vite dev server는 /api/* 요청을 http://localhost:8000으로 proxy (vite.config.ts)
```

## 6. 환경 변수 / 설정 분리

> **단일 환경 운영 명시 (ADR-0037 v1.1)**: 본 프로젝트는 RFP §NFR-06 정의에 따라 dev 1 profile만 운영한다. stg/prod는 N/A (단일 환경 운영). 환경 변수 표는 schema BLOCK 충족을 위해 dev/stg/prod 컬럼을 유지하되 stg·prod는 모두 "N/A — dev 공유 또는 미운영"으로 명시.

| 키 | dev | stg | prod | 노출 위치 |
|---|---|---|---|---|
| `DATABASE_URL` | `sqlite+aiosqlite:///./data/realworld.db` (backend cwd 기준 — `backend/data/realworld.db`) | N/A — 단일 환경 운영 | N/A — 단일 환경 운영 | `backend/.env.example`, FastAPI `Settings` |
| `JWT_SECRET` | 로컬 랜덤 (각자 생성, `backend/.env`에 보관). `python -c "import secrets; print(secrets.token_urlsafe(32))"` | N/A | N/A | `backend/.env.example` placeholder `changeme-please-generate-random-32-chars`, `Settings` |
| `JWT_ALG` | `HS256` | N/A | N/A | `backend/.env.example`, `Settings` |
| `JWT_EXPIRE_MINUTES` | `10080` (7일 = 60*24*7) | N/A | N/A | `backend/.env.example`, `Settings` |
| `CORS_ORIGINS` | `http://localhost:5173` | N/A | N/A | `backend/.env.example`, FastAPI 앱 init |
| `LOG_LEVEL` | `INFO` | N/A | N/A | `backend/.env.example`, stdlib logging |
| `VITE_API_BASE_URL` | `http://localhost:8000/api` | N/A | N/A | `frontend/.env.example` (vite는 `VITE_` prefix만 클라이언트 노출) |

**보안 절대 규칙 (CLAUDE.md)**: `.env` 파일은 .gitignore 강제. `JWT_SECRET` 등 실제 값은 코드·로그·커밋 메시지·PR 본문 어디에도 평문 포함 금지. `.env.example` placeholder 형식 — `JWT_SECRET=<your-random-secret-here>`.

## 7. 부팅 자산 (Runnability Assets)

> **단일 환경 운영**: 본 표의 stg/prod 경로는 모두 N/A 또는 dev 공유. 단일 환경 운영 명시 (ADR-0037 v1.1).

| 자산 | 경로 (profile별) | 변경 trigger 이슈 유형 | 갱신 책임 |
|---|---|---|---|
| 환경 변수 템플릿 | `.env.example` (dev) + `frontend/.env.example` / stg·prod N/A — 단일 환경 운영 | 새 환경변수 추가, 형식 변경 | 작성자(이슈 PR), AI 게이트 6번째 축 검증 |
| 스키마 적용 (dev iteration) | `alembic upgrade head` (`backend/alembic/versions/` 사용) | 모델 변경 → migration 신규 작성 | 작성자(이슈 PR) |
| DB migrations (stg/prod release) | `backend/alembic/versions/` (단일 환경 운영이라 dev iteration과 동일 디렉토리·동일 명령. N/A — dev 공유) | 모델 변경 | 작성자(이슈 PR) |
| lockfile | `backend/uv.lock` + `frontend/pnpm-lock.yaml` | 의존성 추가·버전 변경 | 작성자(이슈 PR), 같은 커밋에 포함 |
| 설치/seed scripts | `backend/scripts/seed_articles.py` (게시글 100건) | seed 데이터 형식 변경, R-N-01 측정 시드 갱신 | 작성자(이슈 PR) |
| 부팅 명령 | dev: `uv run uvicorn realworld.main:app --reload --port 8000` + `pnpm dev` / stg·prod: N/A — 단일 환경 운영 | 부팅 절차 변경 (포트·옵션·proxy 등) | 작성자(이슈 PR), §5 본문도 동시 갱신 |
| LOCAL.md | 루트 `LOCAL.md` (사용자 가이드, ADR-0040) | 위 자산 중 하나라도 변경 시 동시 갱신 | 작성자(이슈 PR), 같은 PR에 포함 |

## 8. 스타일링 솔루션

> Frontend layer 존재 → ADR-0038 강제. 결정: **Tailwind CSS 3.x** (게이트 C 결정).

| 항목 | 결정 |
|---|---|
| 솔루션 | Tailwind CSS 3.x |
| 이유 | (1) Vite 공식 plugin 1개로 통합. (2) utility-first가 10-lld-screen-design §3 디자인 토큰(Color·Typography·Spacing) 직접 매핑. (3) 학습 곡선 완만, 풍부한 문서. (4) Component primitives(Button·Input·Card)를 JSX + utility만으로 작성 — 컴포넌트 라이브러리 의존 0. |
| 의존성 | `frontend/package.json devDependencies`: `tailwindcss@^3.4`, `postcss@^8`, `autoprefixer@^10`. (`@tailwindcss/forms` 등 plugin은 선택, 본 MVP는 미적용) |
| entrypoint 적용 | `frontend/src/main.tsx`에서 `import './index.css';` (index.css 안에 `@tailwind base;`, `@tailwind components;`, `@tailwind utilities;` 3 directive 포함) |
| 디자인 토큰 매핑 | 10-lld-screen-design §3 토큰 → Tailwind 클래스 매핑. 색상은 §3.1 표 (Tailwind 표준 팔레트 채택 — `blue-600`, `gray-900` 등). 폰트 스케일은 §3.2 (Tailwind 기본 `text-base`, `text-2xl`, `text-3xl`). spacing은 §3.3 (4px 그리드, `p-1`/`p-2`/`p-4`/`p-8`). 컴포넌트 primitives는 `frontend/src/components/Button.tsx` 등에 utility 조합으로 구현. |
