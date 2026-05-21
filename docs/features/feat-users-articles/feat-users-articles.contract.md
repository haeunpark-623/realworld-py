---
doc_type: feature-contract
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-12, R-N-01, R-N-05]
  F-ID: [F-01, F-02]
  supersedes: null
---

# feat-users-articles — Change Contract

> Issue #4 / Sprint 1 / I-04. mode=add. Before/After 16행 + Call Sites 8행 + BC neutral (신규 라우트만, 기존 라우트 0). Rollback = revert PR + alembic downgrade 0002.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — §0 Referenced-IDs 5행 + §2 Before/After 16행 + §3 Call Sites 8행 |

## 0. 참조 정본 ID (Referenced-IDs)

본 contract가 의존하는 정본 위치 — P4 plan 단계에서 selective read 진입점 (ADR-0018).

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| 요구사항 (R-) | docs/planning/04-srs/04-srs.md §3 (R-F-01·02·03·04·05·06·07·08·12) + §4 (R-N-01·05) | R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-12, R-N-01, R-N-05 |
| 기능 (F-) | docs/planning/05-prd/05-prd.md §3 (F-01 Auth) + §4 (F-02 Article) | F-01, F-02 |
| 시나리오 | docs/planning/03-user-scenarios/03-user-scenarios.md UC-01, UC-02, UC-05, UC-06, UC-07, UC-08, UC-09, UC-12 | UC-01, UC-02, UC-05, UC-06, UC-07, UC-08, UC-09, UC-12 |
| API Spec | docs/planning/09-lld-api-spec/09-lld-api-spec.md §3 (8 엔드포인트 본 PR) | EP-POST-users, EP-POST-login, EP-GET-user, EP-GET-articles, EP-GET-article-slug, EP-POST-articles, EP-PUT-article, EP-DELETE-article |
| 모듈 LLD | docs/planning/08-lld-module-spec/08-lld-module-spec.md §3 ArticleService + §4 UserRouter + ArticleRouter | M-ArticleService, M-Router-Users, M-Router-Articles |
| 코드 규약 | docs/planning/11-coding-conventions/11-coding-conventions.md §1 Python 명명 + §3 에러 코드 + §4 Import 정책 | (none) |
| 스캐폴딩 | docs/planning/12-scaffolding/python.md §1 트리 (schemas/, routers/, models/, repositories/, services/, utils/) + §5 빌드·실행 | (none) |
| ADR | ADR-0021 (commit message regex), ADR-0040 (LOCAL.md ↔ scaffolding §7 동기), ADR-0044 (브랜치 전략), ADR-0046 (PR body 체크박스), ADR-0047 (GitHub Actions 워크플로 양축) | ADR-0021, ADR-0040, ADR-0044, ADR-0046, ADR-0047 |

## 1. 변경 의도

I-03 통과 후 비즈니스 계층(AuthService + utils + deps + errors)이 준비된 상태에서, **외부 인터페이스 계층**(routers + 모델 + repository + service + Pydantic 스키마)를 추가해 RealWorld API 8 엔드포인트를 동작 가능 상태로 만든다. Article 도메인은 신규 진입(model + Alembic + repo + service + slug util). users 라우트는 I-03의 AuthService를 라우트 함수로 노출하는 thin layer. 통합 테스트 14건+로 09-api-spec 명세와 코드 정합을 회귀 검증한다 — Sprint 2 React SPA 진입의 backend 안정성 기반.

## 2. Before / After

| 항목 | Before | After |
| --- | --- | --- |
| `realworld/models/article.py` | 없음 | Article (id, slug UNIQUE, title, description, body, author_id FK CASCADE, created_at, updated_at) + Tag (id, name UNIQUE) + article_tags M2M 연결 테이블 + `__init__.py` re-export |
| `realworld/migrations/versions/0003_*.py` | 없음 (head 0002 add_users) | articles 테이블 + tags 테이블 + article_tags 연결 테이블 (alembic autogenerate). upgrade + downgrade 함수 정의 |
| `realworld/repositories/article.py` | 없음 | ArticleRepo (5 메서드: list_with_filters / get_by_slug / add / update / delete). selectinload(Article.author + Article.tags)로 N+1 회피. limit/offset/author 파라미터 지원 |
| `realworld/utils/slug.py` | 없음 | `slugify(title: str) -> str` (kebab-case, ASCII 변환, 비-알파넘 → `-`) + `unique_slug(repo, base: str) -> str` (UNIQUE 충돌 시 `-N` suffix, N=2,3,... 증가) |
| `realworld/services/article.py` | 없음 | ArticleService(session) — list / get_by_slug / create / update / delete 5 async 메서드 + 작성자 검증 (Forbidden raise). create 시 slug 자동 생성·tagList 미존재 tag INSERT |
| `realworld/schemas/__init__.py` | 없음 | 빈 마커 |
| `realworld/schemas/user.py` | 없음 | Pydantic v2 — UserCreate / UserLogin / UserResponse(래핑 `{user: {username, email, token, bio, image}}`) |
| `realworld/schemas/article.py` | 없음 | Pydantic v2 — ArticleCreate / ArticleUpdate / ArticleResponse(`{article: {...}}`) / ArticlesListResponse(`{articles: [...], articlesCount: N}`) / ProfileEmbed(author 내장) |
| `realworld/routers/__init__.py` | 없음 | 빈 마커 |
| `realworld/routers/users.py` | 없음 | APIRouter(prefix="/api"): POST /users / POST /users/login / GET /user. AuthService(session) 호출 thin layer |
| `realworld/routers/articles.py` | 없음 | APIRouter(prefix="/api/articles"): GET "" / GET /{slug} / POST "" / PUT /{slug} / DELETE /{slug}. ArticleService(session) 호출. require_auth 의존성 적용 (GET 2종은 optional) |
| `realworld/main.py` | `/health` 1 라우트만 + lifespan | + `app.include_router(users.router)` + `app.include_router(articles.router)` + 예외 핸들러 (`@app.exception_handler(RealWorldError)` → HTTPException 422 한글 매핑) |
| `tests/unit/test_slug.py` | 없음 | slugify 3 케이스 (영문 / 공백·특수문자 / 빈 입력) + unique_slug 2 케이스 (충돌 없음 / `-2` `-3` 진행) = 5 케이스 |
| `tests/unit/test_article_service.py` | 없음 | ArticleService 8 케이스 (list / get / create + slug 충돌 / update 본인 / update 타인 Forbidden / delete 본인 / delete 타인 Forbidden / NotFound) |
| `tests/integration/__init__.py` + `tests/integration/conftest.py` | 없음 | httpx.AsyncClient + ASGITransport(app) fixture + 사용자 fixture (JWT 발급) |
| `tests/integration/test_users_routes.py` | 없음 | 3 라우트 × happy/failure = 7 케이스 이상 (회원가입 happy + email dup 422 + login happy + 자격 오류 422 + GET /user happy + 401 + 만료 401) |
| `tests/integration/test_articles_routes.py` | 없음 | 5 라우트 × happy/failure = 12 케이스 이상 (GET list happy + ?author= 필터 happy + 빈 결과 / GET detail happy + 404 / POST create happy + 401 + slug 충돌 → -2 / PUT happy + 403 타인 / DELETE happy + 403 타인 + 404). 통합 14건+ 충족 |
| `backend/pyproject.toml` | ruff per-file-ignores: `tests/**` S101/S105/S106 + `errors.py` N818 + `deps/**` B008 S105 | + `routers/**` B008 추가 (FastAPI Depends 표준 패턴) — N818/B008/S105 false positive 일관 처리 |

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| `realworld/main.py` | 라우터 2개 등록 + RealWorldError 핸들러 등록 | `app.include_router(users.router)` + `app.include_router(articles.router)` + `@app.exception_handler` 추가 |
| `realworld/repositories/user.py::UserRepo` | 변경 0건 (find_by_id 이미 I-03에 있음). 호출만 — ArticleService가 author 조회 시 | (수정 없음) |
| `realworld/services/auth.py::AuthService` | 변경 0건. routers/users.py가 register / authenticate / get_current_user 3 메서드를 thin wrapper로 노출 | (수정 없음) |
| `realworld/deps/auth.py::require_auth` | 변경 0건. routers/articles.py POST/PUT/DELETE 3 라우트가 `Depends(require_auth)` | (수정 없음) |
| `realworld/db.py::get_db` | 변경 0건. 라우터 함수가 `Depends(get_db)`로 AsyncSession 주입 | (수정 없음) |
| `realworld/models/user.py::User` | 변경 0건. Article.author_id FK가 User.id 참조. relationship으로 양방향 연결 | (수정 없음) |
| `realworld/errors.py` | 변경 0건. ArticleService가 NotFound·Forbidden·InvalidCredentials raise. main.py 핸들러가 422/401/403/404 매핑 | (수정 없음) |
| `realworld/config.py::get_settings` | 변경 0건. JWT_SECRET 등 환경변수 그대로 사용 | (수정 없음) |

## 4. Backward Compatibility

**BC neutral — 기존 동작 변경 0건**. 본 PR는 *순수 add*:

- 기존 라우트 0개 변경. `/health`는 그대로 유지
- 기존 DB 테이블 0개 변경. alembic 0003은 신규 3 테이블 추가만 (upgrade 멱등, downgrade로 0002 복원 가능)
- 기존 단위 테스트 20건 PASS 유지 (3 health + 3 user_repo + 3 security + 3 jwt + 8 auth_service)
- 기존 환경변수 0개 변경. `.env.example`·LOCAL.md 신규 키 0
- 기존 외부 의존(passlib·python-jose·bcrypt·sqlalchemy·alembic·httpx·pytest) 0개 추가. 모두 I-01에서 도입됨

**소비자 영향**: 본 PR가 신규 8 엔드포인트를 처음 노출하므로 *기존 소비자* 자체가 없다. Sprint 2 I-07 (React SPA)이 최초 소비자.

## 5. Rollback 전략

| 단계 | 명령 | 효과 |
| --- | --- | --- |
| 1. PR revert | GitHub PR revert 또는 `git revert -m 1 <merge-commit>` | 코드 전부 원복 |
| 2. Alembic downgrade | `cd backend && uv run alembic downgrade 0002` | articles/tags/article_tags 3 테이블 DROP. 0002 head 복원. dev SQLite는 데이터 손실 허용 (RFP §NFR-06) |
| 3. 후속 이슈 차단 | I-05 (seed) / I-06 (comments) 모두 본 PR에 의존 → 함께 rollback 검토 | 14-wbs §3 의존성 그래프 fan-out |

**완전 revert는 alembic downgrade까지 포함**. 본 PR 머지 후 backend 라우트 코드만 revert하고 schema는 0003 유지하면 *코드와 schema 불일치* 위험. 한 묶음으로 rollback 한다.

## 6. 비목표

| # | 항목 | 사유 | 위탁 위치 |
| --- | --- | --- | --- |
| 1 | comments 4 라우트 (R-F-09·10·11·13) | 14-wbs §1 I-05/I-06 별도 이슈. 본 PR R-ID에 미포함 | I-05/I-06 |
| 2 | 100건 시드 + R-N-01 p95 측정 자동화 | 14-wbs §1 I-05. 본 PR는 API 동작 가능 상태까지 | I-05 |
| 3 | Profile/Follow/Favorite/Tag feed 라우트 | RFP §Out of Scope. RealWorld spec full 미준수 | 본 과제 전체 비목표 |
| 4 | exception_handlers를 별도 모듈로 분리 | 함수 ≤ 6개 inline이 단순 | retro 후 검토 |
| 5 | OpenAPI 자동 문서 명시적 검증 | FastAPI 자동 생성 — 추가 작업 0. Manual verification에서 `GET /docs` 1회 확인 권장 | (자동) |
| 6 | E2E 테스트 (Playwright 등) | Sprint 2 I-08·I-09에서 React SPA + 골든패스 | I-08·I-09 |
| 7 | DB transaction rollback 시 slug 카운터 초과 처리 | dev SQLite + UNIQUE 제약 + 재시도 1회 패턴으로 충분. 동시성 race는 04-srs §R-F-06 Failure-3에 Out 명시 | (Out of Scope) |
