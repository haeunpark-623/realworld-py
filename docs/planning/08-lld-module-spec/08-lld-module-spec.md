---
doc_type: module-spec
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-09, R-F-10, R-F-11, R-F-12, R-F-13, R-N-03, R-N-04, R-N-05, R-N-06]
  F-ID: [F-01, F-02, F-03]
  supersedes: null
---

# realworld-py — Module Spec (LLD — 모듈/통신)

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, 07 HLD §1 fan-out — 백엔드 5개 모듈) |

## 1. 모듈 개요

본 LLD는 07 HLD §1 핵심 모듈 표의 *백엔드 5개 모듈*(M-API-Router, M-Auth-Service, M-Article-Service, M-Comment-Service, M-Auth-Middleware)을 fan-out해 내부 컴포넌트·외부 인터페이스·에러 처리·테스트 진입점을 정의한다. FE 4개 모듈은 본 메타 범위 외 — 본 프로젝트는 백엔드 학습이 1차 목표.

### 1.1 M-API-Router

- **모듈 ID**: M-API-Router
- **책임**: HTTP 요청 라우팅, Pydantic 입력 검증, 인증 헤더 파싱, 응답 직렬화. 도메인별 router 분리 (`users_router`, `articles_router`, `comments_router`)
- **07 HLD §1 참조**: 07 HLD §1 첫 번째 행 (M-API-Router)
- **R-ID 매핑**: R-F-01·R-F-02·R-F-03·R-F-04·R-F-05·R-F-06·R-F-07·R-F-08·R-F-09·R-F-10·R-F-11·R-F-12·R-F-13 (모든 라우트의 진입점)
- **F-ID 매핑**: F-01·F-02·F-03 (라우트 그룹별)

### 1.2 M-Auth-Service

- **모듈 ID**: M-Auth-Service
- **책임**: 회원가입(중복 검사 + bcrypt 해시), 로그인(자격증명 검증 + JWT 발급), 현재 사용자 조회
- **07 HLD §1 참조**: 07 HLD §1 두 번째 행 (M-Auth-Service)
- **R-ID 매핑**: R-F-01, R-F-02, R-F-03, R-N-03 (bcrypt), R-N-04 (시크릿)
- **F-ID 매핑**: F-01

### 1.3 M-Article-Service

- **모듈 ID**: M-Article-Service
- **책임**: 게시글 CRUD (작성·목록·상세·수정·hard delete) + slug 생성/충돌 회피(숫자 suffix) + 작성자 검증 + 페이지네이션 + 댓글 CASCADE 처리
- **07 HLD §1 참조**: 07 HLD §1 세 번째 행 (M-Article-Service)
- **R-ID 매핑**: R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-12, R-N-01 (퍼포먼스), R-N-05 (XSS escape)
- **F-ID 매핑**: F-02

### 1.4 M-Comment-Service

- **모듈 ID**: M-Comment-Service
- **책임**: 댓글 CRUD (작성·목록·수정·삭제) + 작성자 검증. 글 hard delete 시 FK CASCADE로 자동 삭제됨.
- **07 HLD §1 참조**: 07 HLD §1 네 번째 행 (M-Comment-Service)
- **R-ID 매핑**: R-F-09, R-F-10, R-F-11, R-F-13, R-N-05
- **F-ID 매핑**: F-03

### 1.5 M-Auth-Middleware

- **모듈 ID**: M-Auth-Middleware
- **책임**: FastAPI dependency 형태로 JWT 검증 + 현재 사용자 주입. `require_auth` (로그인 필수), `require_author` (해당 리소스 작성자 검증). 401/403 일관 처리.
- **07 HLD §1 참조**: 07 HLD §1 다섯 번째 행 (M-Auth-Middleware)
- **R-ID 매핑**: R-F-03, R-F-06, R-F-07, R-F-08, R-F-09, R-F-11, R-F-12, R-F-13, R-N-04
- **F-ID 매핑**: F-01, F-02, F-03

## 2. 외부 인터페이스

본 표는 각 모듈이 외부(다른 모듈 또는 HTTP 클라이언트)에 노출하는 인터페이스를 요약한다. HTTP 엔드포인트 상세는 09-lld-api-spec 참조.

| 인터페이스 | 입력 | 출력 | 에러 |
|---|---|---|---|
| `M-API-Router.users_router` (Pydantic RegisterReq/LoginReq) | `UserCreate {username, email, password}` 또는 `UserLogin {email, password}` | `UserResponse {user: {username, email, token, ...}}` | 422 (검증 실패) · 401 (로그인 실패) · 500 |
| `M-API-Router.articles_router` (Pydantic ArticleCreate/Update/Filter) | `ArticleCreate {title, description, body, tagList?}` 또는 query (`limit`, `offset`, `author?`) | `ArticleResponse {article: {...}}` 또는 `ArticlesResponse {articles: [...], articlesCount}` | 401 · 403 · 404 · 422 |
| `M-API-Router.comments_router` (Pydantic CommentCreate/Update) | `CommentCreate {body}` 또는 `CommentUpdate {body}` | `CommentResponse {comment: {...}}` 또는 `CommentsResponse {comments: [...]}` | 401 · 403 · 404 · 422 |
| `M-Auth-Service.register(UserCreate) -> User` | `UserCreate` DTO | `User` 도메인 객체 (token 포함 별도 반환) | `DuplicateEmailError` · `DuplicateUsernameError` · `ValidationError` |
| `M-Auth-Service.authenticate(email, password) -> str` | email·password | JWT 문자열 | `InvalidCredentialsError` (이메일·비밀번호 누설 방지 동일 메시지) |
| `M-Auth-Service.get_current_user(token) -> User` | JWT 문자열 | `User` 객체 | `InvalidTokenError` · `ExpiredTokenError` · `UserNotFoundError` |
| `M-Article-Service.list(limit, offset, author?) -> (list[Article], total)` | int·int·Optional[str] | `(list, int)` | (DB 에러만) |
| `M-Article-Service.get_by_slug(slug) -> Article` | slug str | Article | `ArticleNotFoundError` |
| `M-Article-Service.create(user, ArticleCreate) -> Article` | current_user · DTO | Article | `ValidationError` (slug 생성 단계에서 빈 title 차단) |
| `M-Article-Service.update(user, slug, ArticleUpdate) -> Article` | current_user · slug · DTO | Article | `ArticleNotFoundError` · `ForbiddenError` (타인 시도) |
| `M-Article-Service.delete(user, slug) -> None` | current_user · slug | None | `ArticleNotFoundError` · `ForbiddenError` |
| `M-Comment-Service.create(user, slug, body) -> Comment` | current_user · slug · body | Comment | `ArticleNotFoundError` · `ValidationError` (empty body) |
| `M-Comment-Service.list_by_article(slug) -> list[Comment]` | slug | list (최신순) | `ArticleNotFoundError` |
| `M-Comment-Service.update(user, slug, id, body) -> Comment` | current_user · slug · id · body | Comment | `CommentNotFoundError` · `ForbiddenError` · `ValidationError` |
| `M-Comment-Service.delete(user, slug, id) -> None` | current_user · slug · id | None | `CommentNotFoundError` · `ForbiddenError` |
| `M-Auth-Middleware.require_auth() -> User` (FastAPI Depends) | Authorization 헤더 | `User` 객체 (FastAPI Depends 결과) | 401 (헤더 누락/형식 오류/만료/위조) |
| `M-Auth-Middleware.require_author(user, resource_author_id) -> None` | current_user · resource owner id | None | 403 |

## 3. 내부 컴포넌트

| 모듈 | 내부 컴포넌트 | 역할 |
|---|---|---|
| M-API-Router | `users_router.py` · `articles_router.py` · `comments_router.py` · 공통 에러 핸들러 | 도메인별 라우트 + 422→{errors: {...}} 변환 |
| M-Auth-Service | `services/auth.py` · `utils/security.py`(passlib) · `utils/jwt.py`(python-jose) | 비즈니스 로직 + 보안 유틸 |
| M-Article-Service | `services/article.py` · `utils/slug.py`(kebab-case + 숫자 suffix) | 비즈니스 로직 |
| M-Comment-Service | `services/comment.py` | 비즈니스 로직 |
| M-Auth-Middleware | `deps/auth.py` (`require_auth`, `require_author` dependency) | FastAPI Depends 함수 |
| (공통) Repository | `repositories/user.py` · `repositories/article.py` · `repositories/comment.py` | SQLAlchemy 쿼리 캡슐화. eager loading 정의. N+1 회피 정본 |
| (공통) Models | `models/user.py` · `models/article.py` · `models/comment.py` · `models/tag.py` | SQLAlchemy declarative 모델 + 인덱스·제약·CASCADE 선언 |
| (공통) Schemas | `schemas/user.py` · `schemas/article.py` · `schemas/comment.py` | Pydantic 요청·응답 모델 |

## 4. 데이터 흐름

### 4.1 회원가입 흐름 (R-F-01)

```
HTTP POST /api/users
  → users_router.register(UserCreate)
  → AuthService.register(dto)
      → UserRepo.find_by_email(dto.email)   # 중복 검사
      → UserRepo.find_by_username(dto.username)
      → security.hash_password(dto.password)  # bcrypt
      → UserRepo.create(User(... password_hash=hashed))
      → jwt.encode({user_id, exp}, JWT_SECRET)
      → return (User, token)
  → response: 201 {user: {..., token}}
```

### 4.2 게시글 작성 흐름 (R-F-06, slug 충돌 회피)

```
HTTP POST /api/articles  (Authorization: Token ...)
  → require_auth → current_user
  → articles_router.create(current_user, ArticleCreate)
  → ArticleService.create(current_user, dto)
      → slug = slug.kebab_case(dto.title)
      → while ArticleRepo.exists_by_slug(slug):
            slug = f"{base}-{counter}"
            counter++
      → ArticleRepo.create(Article(slug=slug, author_id=current_user.id, ...))
      → return Article
  → response: 201 {article: {...}}
```

### 4.3 게시글 hard delete + 댓글 CASCADE (R-F-08)

```
HTTP DELETE /api/articles/{slug}  (Authorization: Token ...)
  → require_auth → current_user
  → articles_router.delete(current_user, slug)
  → ArticleService.delete(current_user, slug)
      → article = ArticleRepo.get_by_slug(slug)      # 없으면 404
      → if article.author_id != current_user.id: raise ForbiddenError  # 403
      → ArticleRepo.delete(article)                  # CASCADE: comments 자동 삭제
  → response: 204
```

### 4.4 댓글 수정 흐름 (R-F-13)

```
HTTP PUT /api/articles/{slug}/comments/{id}  (Authorization: Token ...)
  → require_auth → current_user
  → comments_router.update(current_user, slug, id, CommentUpdate)
  → CommentService.update(current_user, slug, id, body)
      → comment = CommentRepo.get(id)
      → if comment is None or comment.article.slug != slug: 404
      → if comment.author_id != current_user.id: 403
      → comment.body = body
      → CommentRepo.save(comment)
      → return Comment
  → response: 200 {comment: {...}}
```

## 5. 상태·라이프사이클

- 본 시스템은 *stateless* 백엔드 (JWT 기반). 서버 측 세션 없음.
- DB 트랜잭션 라이프사이클: 요청 시작 시 SQLAlchemy `Session` 열고, 응답 직전 commit/rollback + close. FastAPI dependency `get_db()` 패턴.
- JWT 라이프사이클: 발급 후 만료(기본 7일, `JWT_EXP_SECONDS` 환경변수) 시까지 stateless 유효. 서버 측 무효화 미적용 (RFP §F-01d 명시).

## 6. 에러 처리

본 시스템의 도메인 에러는 다음과 같이 매핑된다. FastAPI `exception_handlers`로 통합 처리하여 RealWorld spec 응답 형식 `{errors: {field: ["메시지"]}}`로 변환한다.

| 에러 | 발생 조건 | 처리 |
|---|---|---|
| `DuplicateEmailError` | 회원가입 시 동일 email 존재 | 422 `{errors: {email: ["이미 사용 중인 이메일입니다"]}}` |
| `DuplicateUsernameError` | 회원가입 시 동일 username 존재 | 422 `{errors: {username: ["이미 사용 중인 username입니다"]}}` |
| `InvalidCredentialsError` | 로그인 실패(이메일 미존재 OR 비밀번호 불일치) | 422 `{errors: {body: ["이메일 또는 비밀번호가 올바르지 않습니다"]}}` — 어느 쪽이 틀렸는지 누설 안 함 |
| `InvalidTokenError` | JWT 서명 위조 또는 헤더 형식 오류 | 401 `{errors: {body: ["인증 토큰이 유효하지 않습니다"]}}` |
| `ExpiredTokenError` | JWT exp 클레임 만료 | 401 `{errors: {body: ["인증 토큰이 만료되었습니다"]}}` |
| `UserNotFoundError` | JWT user_id가 DB 사용자에 없음 (탈퇴된 사용자 등) | 401 (동일 처리, 정보 누설 방지) |
| `ArticleNotFoundError` | slug에 해당하는 article 부재 | 404 `{errors: {body: ["게시글을 찾을 수 없습니다"]}}` |
| `CommentNotFoundError` | id에 해당하는 comment 부재 | 404 `{errors: {body: ["댓글을 찾을 수 없습니다"]}}` |
| `ForbiddenError` | 작성자가 아닌데 수정/삭제 시도 | 403 `{errors: {body: ["권한이 없습니다"]}}` |
| `ValidationError` (Pydantic) | 요청 body 검증 실패 (필수 누락·타입·길이) | 422 — FastAPI 기본 핸들러 + 한글 메시지 매핑 (11-coding-conventions §2 에러 코드) |
| `IntegrityError` (SQLAlchemy) | DB 제약 위반 (UNIQUE 등, race condition) | 409 또는 422 (도메인 에러로 변환 후 매핑) |
| `Exception` (catch-all) | 미처리 예외 | 500 `{errors: {body: ["서버 오류가 발생했습니다"]}}` + stdout 로깅 |

## 7. 동시성·트랜잭션

- **트랜잭션 단위**: 라우트 1회 = SQLAlchemy `Session` 1개. 응답 직전 commit. 예외 발생 시 rollback.
- **동시성 가정**: 학습 컨텍스트 1~5명 동시 사용자. SQLite 단일 writer 가정 — 부담 없음.
- **race condition (slug 충돌)**: 본 시스템은 단일 writer 가정 + UNIQUE 제약 + 충돌 시 IntegrityError → suffix 증가 retry 1회 (서비스 레벨, R-F-06 Failure-3).
- **JWT 동시 검증**: stateless, 락 없음.

## 8. 테스트 진입점

본 표는 13-test-design/02-catalog에서 fan-in되는 *모듈별 테스트 진입점*을 정의한다.

| 진입점 | 레벨 | 대상 | 테스트 파일(예상) |
|---|---|---|---|
| `AuthService.register` | 단위 | M-Auth-Service | `tests/unit/test_auth_service.py::test_register_*` |
| `AuthService.authenticate` | 단위 | M-Auth-Service | `tests/unit/test_auth_service.py::test_authenticate_*` |
| `AuthService.get_current_user` | 단위 | M-Auth-Service | `tests/unit/test_auth_service.py::test_get_current_user_*` |
| `ArticleService.list / get_by_slug / create / update / delete` | 단위 | M-Article-Service | `tests/unit/test_article_service.py::*` |
| `CommentService.create / list_by_article / update / delete` | 단위 | M-Comment-Service | `tests/unit/test_comment_service.py::*` |
| `require_auth`, `require_author` | 단위 | M-Auth-Middleware | `tests/unit/test_auth_middleware.py::*` |
| POST `/api/users` · POST `/api/users/login` · GET `/api/user` | 통합 | M-API-Router + M-Auth-Service | `tests/integration/test_users_routes.py` |
| `/api/articles` 5개 라우트 | 통합 | M-API-Router + M-Article-Service | `tests/integration/test_articles_routes.py` |
| `/api/articles/{slug}/comments*` 4개 라우트 | 통합 | M-API-Router + M-Comment-Service | `tests/integration/test_comments_routes.py` |
| 게시글 100건 시드 p95 측정 | 통합 (성능) | R-N-01 | `tests/integration/test_performance.py::test_articles_list_p95` |
| 골든패스 (가입→로그인→글→댓글→수정→삭제) | E2E | F-04 / R-F-01~R-F-13 | gstack `/qa` (스크립트 외부 도구) |
| XSS payload escape 검증 | E2E | R-N-05 | gstack `/qa` (1회 페이로드 시도) |
