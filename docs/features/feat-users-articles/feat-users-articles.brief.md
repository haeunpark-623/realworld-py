---
doc_type: feature-brief
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

# feat-users-articles — Feature Brief

> Issue #4 / Sprint 1 / I-04 (effort 2d ≈ 2.5~3.5h). I-03 AuthService + utils/security + utils/jwt + deps/auth + errors.py 6 도메인 예외 위에 *경로 계층(routers) + 게시글 도메인(Article + Tag 모델·repo·service·slug util) + Pydantic 스키마 + 통합 테스트 14건+*를 얹어 RealWorld API 8 엔드포인트(users 3 + articles 5)를 동작 가능 상태로 마감한다. comments 4 라우트는 비목표(I-05/I-06로 분리, 14-wbs §1).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — mode=add 자동 결정 / R-ID 11개·F-ID 2개 매핑 / 영향 4 영역 / 비목표 5건 |

## 1. 한 줄 의도

RealWorld API 8 엔드포인트(users 3 + articles 5) FastAPI 라우터 + Article/Tag 모델 + ArticleService + Pydantic 스키마 + 통합 테스트로 backend MVP를 완료한다 (Sprint 1 마감 조건).

## 2. 사용자 가치

- **가입 사용자 (페르소나 P-02)**: 회원가입/로그인 → 글 작성·조회·수정·삭제 → 본인 글 필터(`?author=`) 기능을 HTTP API로 사용할 수 있다. 03-user-scenarios UC-01·UC-02·UC-05·UC-06·UC-07·UC-08·UC-09·UC-12 골든패스 backend 전 구간.
- **비회원 (P-01)**: 글 목록·상세 조회 가능 (인증 헤더 없이 GET /api/articles, GET /api/articles/{slug}).
- **개발자 (간접)**: 통합 테스트 14건+이 09-api-spec 명세와 코드 정합을 회귀 검증 — Sprint 2(I-07 React SPA) 진입 시 backend 변경 위험 ↓.

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 (PR #13 머지 직후) | 변경 후 (본 PR 머지 직후) |
| --- | --- | --- |
| HTTP 라우트 | `/health` 1개만 (main.py에서 직접) | + `routers/users.py` 3 + `routers/articles.py` 5 = 9 라우트 |
| 도메인 모델 | `models/user.py` 1개 | + `models/article.py` (Article + Tag + article_tags M2M 연결 테이블) |
| Alembic | 0001 init + 0002 add_users (head) | + 0003 articles_tags (head) — Article·Tag·article_tags 3 테이블 |
| 비즈니스 서비스 | `services/auth.py` (AuthService 3 메서드) | + `services/article.py` (ArticleService 5 메서드: list/get_by_slug/create/update/delete) |
| Repository | `repositories/user.py` (UserRepo 4 메서드) | + `repositories/article.py` (ArticleRepo selectinload N+1 회피 5 메서드) |
| Util | `utils/security.py` + `utils/jwt.py` | + `utils/slug.py` (kebab-case slugify + UNIQUE 충돌 시 `-N` suffix) |
| Pydantic 스키마 | 없음 (errors.py 도메인 예외만) | + `schemas/user.py` + `schemas/article.py` (RealWorld 래핑 형식 `{user: {...}}` / `{article: {...}}` / `{articles: [...], articlesCount: N}`) |
| FastAPI 예외 핸들러 | 없음 (errors.RealWorldError 미연결) | + `main.py`에 RealWorldError → HTTPException 422 한글 에러 매핑 핸들러 등록 |
| 테스트 | 단위 20 (3 health + 3 user_repo + 3 security + 3 jwt + 8 auth_service) | + 단위 8건+ (test_article_service.py + test_slug.py) + 통합 14건+ (test_users_routes.py + test_articles_routes.py) = 합산 42건+ |
| ID 매핑 (R-F) | R-F-01·02·03 (Auth)·R-N-03·R-N-04 cover | + R-F-04·05·06·07·08·12 (Articles) + R-N-01·R-N-05 부분 cover |

## 4. 모드 자동 감지 결과

**mode=add** (자동 결정, ADR-0032 §2.1 무질문 진행). 부정 시그널 0건:

- ❌ `type:bug` 라벨 → 없음. 본 이슈는 `type:feature`·`area:backend`·`priority:P0`
- ❌ UI/시각/token/리브랜딩 키워드 → 없음 (Frontend는 I-07~I-09 Sprint 2)
- ❌ 기존 동작 변경 / breaking 가능성 → 없음 (신규 모듈·신규 테이블·신규 라우트 추가만)

✅ `type:feature` 라벨 + 신규 동작 → mode=add 결정.

**Mode Decision Trace**: 본 이슈는 PR body Mode Decision Trace 절에 위 3행을 그대로 인용한다 (ADR-0032 §3.2 — 결정 경로 가시화).

## 5. 영향 범위

**3+영역 → PR body Touched Areas 절 필수 (pull-request.md §4.2)**. 본 PR 4 영역:

| 영역 | 변경 내용 | 영향 |
| --- | --- | --- |
| backend 코드 | `models/article.py` + `repositories/article.py` + `services/article.py` + `utils/slug.py` + `schemas/{user,article}.py` + `routers/{users,articles}.py` + `main.py` 라우터 등록 + 예외 핸들러 | 9 신규 파일 + 1 수정 |
| DB 스키마 | `migrations/versions/0003_articles_tags.py` (autogenerate). 신규 테이블 3개. 기존 0001·0002 변경 0 | dev SQLite head 0002 → 0003 진행 |
| 테스트 | `tests/unit/test_article_service.py` + `tests/unit/test_slug.py` + `tests/integration/test_users_routes.py` + `tests/integration/test_articles_routes.py` (신규) + `conftest.py` httpx AsyncClient fixture | 단위 8건+ + 통합 14건+ = 22건+ 추가 |
| 문서 | 12-scaffolding/python.md §1 트리 + §5/§6 NEW 환경변수(없음) + 14-wbs Issue #4 status:in-review + INDEX.md 변경 이력 | docs 3 파일 갱신 |

**UI / FE 영향**: 0건. 본 PR은 백엔드 HTTP API 계층. ui_changed=false. AI 게이트 5번째 축 N/A로 자동 통과 (ADR-0011).

**부팅 자산 동기 (ADR-0040)**: alembic migrations 1건 추가 (head 0002 → 0003). `.env.example`·LOCAL.md·pyproject.toml·uv.lock 변경 0 (외부 의존 추가 없음 — sqlalchemy·pydantic·alembic·httpx 모두 I-01에 도입됨). dev profile만 검증 (RFP §NFR-06 단일 환경 운영).

## 6. 비목표

| # | 항목 | 사유 | 위탁 위치 |
| --- | --- | --- | --- |
| 1 | comments 4 라우트 (GET/POST/PUT/DELETE `/api/articles/{slug}/comments[/{id}]`) | 14-wbs §1 I-05 또는 I-06에 분리. R-F-09·R-F-10·R-F-11·R-F-13 별도 이슈 | I-05/I-06 (Sprint 1 후반 또는 Sprint 2) |
| 2 | 100건 시드 스크립트 + R-N-01 p95 측정 | 14-wbs I-05 단독 이슈. backend 라우트는 본 PR로 동작 가능 | I-05 |
| 3 | Profile/Follow/Favorite/Tag feed | RFP §Out of Scope. RealWorld spec full 미준수 | 본 학습 과제 전체 비목표 |
| 4 | exception_handlers를 별도 모듈로 분리 | 본 PR는 `main.py`에 inline 등록 — 함수 8개 미만이라 모듈 분리 비용 > 이득. I-04 비목표 처리 후 Sprint 2 마지막에 검토 | 후속 (I-06 또는 retro) |
| 5 | R-F-13 PUT comment 비표준 엔드포인트 | comments 라우트에 포함 (비목표 #1) | I-05/I-06 |

## 7. Open Questions

| # | Question | 결정 시점 | 임시 가정 |
| --- | --- | --- | --- |
| 1 | Pydantic schemas 폴더 vs 단일 파일 | P3 contract | **폴더** — `schemas/user.py` + `schemas/article.py` 분리 (한 파일 ≥ 100줄 예상, 12-scaffolding §1 트리에 schemas/ 명시) |
| 2 | exception_handlers 위치 (main.py inline vs 모듈) | P3 contract | **main.py inline** — 함수 4~6개라 모듈 분리 부담 ↑. 비목표 #4와 정합 |
| 3 | Article 모델 author FK CASCADE/SET NULL | P3 contract | **CASCADE** — 09-api-spec DELETE /api/articles 댓글 CASCADE와 일관. 09-api-spec §3 `DELETE /api/articles/{slug}` 본문에 명시 |
| 4 | tag 정규화 — 신규 tag도 INSERT vs 기존만 매핑 | P3 contract | **신규 INSERT** — tagList: [...] 입력 시 미존재 tag는 자동 생성. 04-srs §R-F-06 가정 |
| 5 | R-F-12 `?author=` 미존재 username | P3 contract | **빈 articles 배열 반환** (404 아님) — 09-api-spec GET /api/articles 표 명시 사항 없음. 빈 결과 일관 |
