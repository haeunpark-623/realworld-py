---
doc_type: test-design
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-09, R-F-10, R-F-11, R-F-12, R-F-13, R-N-01, R-N-02, R-N-03, R-N-04, R-N-05, R-N-06]
  F-ID: [F-01, F-02, F-03, F-04]
  supersedes: null
---

# 13-test-design / 02-catalog — Test Scenario Catalog (단위·통합·E2E 별 묶음)

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, 04-srs R-F-01~R-F-13 + 05-prd F-01~F-04 fan-in. ADR-0034 sub-file BLOCK + ADR-0036 레벨 그룹핑) |

본 카탈로그는 04-srs와 05-prd의 R-ID/F-ID별 *테스트 시나리오* 절을 fan-in하여 단위·통합·E2E 3 레벨로 그룹화한다. 각 시나리오는 상류 ID(04#R-... 또는 05#F-...)를 인용한다.

## 1. 단위 테스트 카탈로그

### R-F-01: 회원가입 (단위)

- 출처: 04#R-F-01 §단위 ✅
- 테스트 레벨: 단위
- 대상: `AuthService.register(UserCreateSchema) -> User`
- Happy path: 신규 username·email·8자+ 비밀번호 → User 반환 + DB row 생성 + password_hash가 `$2b$`로 시작 (bcrypt)
- Failure path:
  - 실패-1: 중복 email → `DuplicateEmailError` 발생
  - 실패-2: 중복 username → `DuplicateUsernameError` 발생
  - 실패-3: 비밀번호 7자 → ValidationError (라우터·스키마 레벨로 위임, 본 단위 테스트는 실패-1·2만 검증)
- 테스트 파일: `tests/unit/test_auth_service.py::test_register_*`

### R-F-02: 로그인 (단위)

- 출처: 04#R-F-02 §단위 ✅
- 테스트 레벨: 단위
- 대상: `AuthService.authenticate(email, password) -> token`
- Happy path: 정상 자격증명 → JWT 문자열 반환 (decode 시 user_id·exp 포함)
- Failure path:
  - 실패-1: 비밀번호 불일치 → `InvalidCredentialsError`
  - 실패-2: 미존재 이메일 → 동일 `InvalidCredentialsError` (정보 누설 방지)
- 테스트 파일: `tests/unit/test_auth_service.py::test_authenticate_*`

### R-F-03: 현재 사용자 조회 (단위)

- 출처: 04#R-F-03 §단위 ✅
- 테스트 레벨: 단위
- 대상: `AuthService.get_current_user(token) -> User`
- Happy path: 유효 JWT → User 반환
- Failure path:
  - 실패-1: JWT 없음 → `InvalidTokenError`
  - 실패-2: JWT 만료 → `ExpiredTokenError`
  - 실패-3: JWT 위조(서명 불일치) → `InvalidTokenError`
- 테스트 파일: `tests/unit/test_auth_service.py::test_get_current_user_*`

### R-F-04: 게시글 목록 (단위)

- 출처: 04#R-F-04 §단위 ✅
- 테스트 레벨: 단위
- 대상: `ArticleService.list(limit, offset, author?) -> (list, total)`
- Happy path: limit=20, offset=0 → 최신순 20건 + total. author 필터 시 해당 사용자 글만
- Failure path: limit > 100 거부 (검증 단계에서 거부, 단위 테스트는 정상 정렬만 검증)
- 테스트 파일: `tests/unit/test_article_service.py::test_list_*`

### R-F-05: 게시글 상세 (단위)

- 출처: 04#R-F-05 §단위 ✅
- 테스트 레벨: 단위
- 대상: `ArticleService.get_by_slug(slug) -> Article`
- Happy path: 존재 slug → Article 반환
- Failure path:
  - 실패-1: 미존재 slug → `ArticleNotFoundError`
- 테스트 파일: `tests/unit/test_article_service.py::test_get_by_slug_*`

### R-F-06: 게시글 작성 + slug 충돌 회피 (단위)

- 출처: 04#R-F-06 §단위 ✅ + `utils/slug.py` 단위
- 테스트 레벨: 단위
- 대상: `ArticleService.create(user, ArticleCreateSchema) -> Article` + `utils/slug.generate_unique(title, exists_fn)`
- Happy path: 정상 작성 → Article + slug=kebab-case
- Failure path:
  - 실패-1: 동명 제목 작성 → slug에 `-2`, 다시 작성 → `-3` 숫자 suffix 정상 (Happy의 변형)
  - 실패-2: title 빈 문자열 → ValidationError (라우터에서 차단, 단위는 슬러그 유틸만 격리 검증)
- 테스트 파일: `tests/unit/test_article_service.py::test_create_*` + `tests/unit/test_slug.py::*`

### R-F-07: 게시글 수정 (단위)

- 출처: 04#R-F-07 §단위 ✅
- 테스트 레벨: 단위
- 대상: `ArticleService.update(user, slug, ArticleUpdateSchema) -> Article`
- Happy path: 작성자 본인 → 부분 갱신된 Article 반환
- Failure path:
  - 실패-1: 타인 시도 → `ForbiddenError`
  - 실패-2: 미존재 slug → `ArticleNotFoundError`
- 테스트 파일: `tests/unit/test_article_service.py::test_update_*`

### R-F-08: 게시글 hard delete (단위)

- 출처: 04#R-F-08 §단위 ✅
- 테스트 레벨: 단위
- 대상: `ArticleService.delete(user, slug) -> None`
- Happy path: 작성자 본인 → None 반환 + DB row 부재 확인
- Failure path:
  - 실패-1: 타인 시도 → `ForbiddenError`
  - 실패-2: 이미 삭제된 글 → `ArticleNotFoundError`
- 비고: 댓글 CASCADE는 SQLAlchemy FK 설정의 책임이므로 본 단위 테스트는 서비스 호출 자체만 검증. CASCADE 실제 동작 검증은 통합 테스트에서.
- 테스트 파일: `tests/unit/test_article_service.py::test_delete_*`

### R-F-09: 댓글 작성 (단위)

- 출처: 04#R-F-09 §단위 ✅
- 테스트 레벨: 단위
- 대상: `CommentService.create(user, slug, body) -> Comment`
- Happy path: 정상 작성 → Comment 반환
- Failure path:
  - 실패-1: 미존재 슬러그 → `ArticleNotFoundError`
  - 실패-2: body 빈 문자열 → ValidationError (라우터·스키마 단계)
- 테스트 파일: `tests/unit/test_comment_service.py::test_create_*`

### R-F-10: 댓글 목록 (단위)

- 출처: 04#R-F-10 §단위 ✅
- 테스트 레벨: 단위
- 대상: `CommentService.list_by_article(slug) -> list[Comment]`
- Happy path: 정상 호출 → 최신순 댓글 배열. 댓글 0건이면 빈 배열
- Failure path:
  - 실패-1: 미존재 slug → `ArticleNotFoundError`
- 테스트 파일: `tests/unit/test_comment_service.py::test_list_by_article_*`

### R-F-11: 댓글 삭제 (단위)

- 출처: 04#R-F-11 §단위 ✅
- 테스트 레벨: 단위
- 대상: `CommentService.delete(user, slug, id) -> None`
- Happy path: 작성자 본인 → None
- Failure path:
  - 실패-1: 타인 시도 → `ForbiddenError`
  - 실패-2: 이미 삭제된 댓글 → `CommentNotFoundError`
- 테스트 파일: `tests/unit/test_comment_service.py::test_delete_*`

### R-F-12: 내 글 목록 (단위)

- 출처: 04#R-F-12 §단위 ✅
- 테스트 레벨: 단위
- 대상: `ArticleService.list(limit, offset, author=username) -> (list, total)`
- Happy path: 본인 username → 본인 글만 반환
- Failure path: 잘못된 username → 빈 배열 (에러 아님)
- 비고: R-F-04와 같은 메서드, author 파라미터 시나리오만 별도 검증
- 테스트 파일: `tests/unit/test_article_service.py::test_list_with_author_filter`

### R-F-13: 댓글 수정 (단위)

- 출처: 04#R-F-13 §단위 ✅
- 테스트 레벨: 단위
- 대상: `CommentService.update(user, slug, id, body) -> Comment`
- Happy path: 작성자 본인 + 비어있지 않은 body → 갱신된 Comment
- Failure path:
  - 실패-1: 타인 시도 → `ForbiddenError`
  - 실패-2: 이미 삭제된 댓글 → `CommentNotFoundError`
  - 실패-3: body 빈 문자열 → ValidationError
- 테스트 파일: `tests/unit/test_comment_service.py::test_update_*`

### R-N-03: 비밀번호 저장 (단위)

- 출처: 04#R-N-03 §단위 ✅
- 테스트 레벨: 단위
- 대상: `utils/security.hash_password(plain) -> str` + `verify_password(plain, hashed) -> bool`
- Happy path: 해시 결과가 `$2b$` 마커로 시작 + verify_password(원본, 해시) == True
- Failure path: verify_password(다른 비밀번호, 해시) == False
- 테스트 파일: `tests/unit/test_security.py`

### R-N-04: 시크릿 관리 (단위)

- 출처: 04#R-N-04 §단위 ✅
- 테스트 레벨: 단위
- 대상: `Settings` (pydantic-settings)
- Happy path: `JWT_SECRET` 환경 변수 설정 + Settings() 로드 성공
- Failure path: `JWT_SECRET` 환경 변수 미설정 → 명시적 ValidationError (Settings 인스턴스 생성 시 즉시 예외)
- 테스트 파일: `tests/unit/test_config.py`

### R-N-06: 단위 테스트 커버리지 (단위, 메타)

- 출처: 04#R-N-06 §단위 ✅
- 테스트 레벨: 단위
- 대상: 적용 범위 모듈 전체 (01-strategy §3 참조)
- Happy path: `uv run pytest --cov=realworld/services --cov=realworld/deps --cov-fail-under=80` exit 0
- Failure path: 미달 시 exit 1 → CI 머지 차단
- 테스트 파일: N/A (CI 명령 자체)

## 2. 통합 테스트 카탈로그

### R-F-01: 회원가입 (통합)

- 출처: 04#R-F-01 §통합 ✅
- 테스트 레벨: 통합
- 대상: `POST /api/users` 라우트 + AuthService + UserRepo + SQLite
- Happy path: 정상 POST → 201 + JWT + DB users row 1개 + password_hash가 `$2b$`
- Failure path:
  - 실패-1: 중복 email → 422 + `{"errors": {"email": ["..."]}}` (한글)
  - 실패-2: password 7자 → 422 (Pydantic 검증)
- 테스트 파일: `tests/integration/test_users_routes.py::test_register_*`

### R-F-02: 로그인 (통합)

- 출처: 04#R-F-02 §통합 ✅
- 테스트 레벨: 통합
- 대상: `POST /api/users/login`
- Happy path: 정상 자격증명 → 200 + JWT
- Failure path: 비밀번호 불일치 → 422 + 한글 메시지
- 테스트 파일: `tests/integration/test_users_routes.py::test_login_*`

### R-F-03: 현재 사용자 조회 (통합)

- 출처: 04#R-F-03 §통합 ✅
- 테스트 레벨: 통합
- 대상: `GET /api/user` + `require_auth` middleware
- Happy path: 유효 JWT → 200 + 본인 정보
- Failure path: JWT 만료 → 401 + 한글 메시지
- 테스트 파일: `tests/integration/test_users_routes.py::test_get_current_user_*`

### R-F-04: 게시글 목록 (통합 + N+1 회피 검증)

- 출처: 04#R-F-04 §통합 ✅ + R-N-01 통합 ✅
- 테스트 레벨: 통합
- 대상: `GET /api/articles`
- Happy path: 100건 시드 + limit=20&offset=0 → 200 + 20건 + total=100 + SQLAlchemy event listener로 N+1 쿼리 0건 확인
- Failure path: limit=200 → 422
- 테스트 파일: `tests/integration/test_articles_routes.py::test_list_*`

### R-F-05: 게시글 상세 (통합)

- 출처: 04#R-F-05 §통합 ✅
- 테스트 레벨: 통합
- 대상: `GET /api/articles/{slug}`
- Happy path: 존재 slug → 200 + Article + author 포함
- Failure path: 미존재 slug → 404 + 한글 메시지
- 테스트 파일: `tests/integration/test_articles_routes.py::test_get_by_slug_*`

### R-F-06: 게시글 작성 (통합)

- 출처: 04#R-F-06 §통합 ✅
- 테스트 레벨: 통합
- 대상: `POST /api/articles` + JWT middleware
- Happy path: 정상 작성 → 201 + slug 응답
- Failure path:
  - 실패-1: 동명 제목 두 번째 작성 → 201 + slug=`my-post-2` (suffix 부여)
  - 실패-2: JWT 만료 → 401
  - 실패-3: title 누락 → 422
- 테스트 파일: `tests/integration/test_articles_routes.py::test_create_*`

### R-F-07: 게시글 수정 (통합)

- 출처: 04#R-F-07 §통합 ✅
- 테스트 레벨: 통합
- 대상: `PUT /api/articles/{slug}`
- Happy path: 작성자 본인 → 200 + 갱신된 Article
- Failure path: 타인 시도 → 403
- 테스트 파일: `tests/integration/test_articles_routes.py::test_update_*`

### R-F-08: 게시글 hard delete + 댓글 CASCADE (통합)

- 출처: 04#R-F-08 §통합 ✅
- 테스트 레벨: 통합
- 대상: `DELETE /api/articles/{slug}` + FK CASCADE
- Happy path: 작성자 본인 + 댓글 N개 달린 글 → 204 + DB에 article·comment 모두 부재 (CASCADE 동작 검증)
- Failure path:
  - 실패-1: 타인 시도 → 403
  - 실패-2: 이미 삭제된 글 → 404
- 테스트 파일: `tests/integration/test_articles_routes.py::test_delete_*`

### R-F-09: 댓글 작성 (통합)

- 출처: 04#R-F-09 §통합 ✅
- 테스트 레벨: 통합
- 대상: `POST /api/articles/{slug}/comments`
- Happy path: 정상 작성 → 201 + comment
- Failure path:
  - 실패-1: 비로그인 → 401
  - 실패-2: 빈 body → 422
  - 실패-3: 미존재 글 slug → 404
- 테스트 파일: `tests/integration/test_comments_routes.py::test_create_*`

### R-F-10: 댓글 목록 (통합)

- 출처: 04#R-F-10 §통합 ✅
- 테스트 레벨: 통합
- 대상: `GET /api/articles/{slug}/comments`
- Happy path: 정상 호출 → 200 + 최신순 배열. 0건이면 빈 배열
- Failure path: 미존재 slug → 404
- 테스트 파일: `tests/integration/test_comments_routes.py::test_list_*`

### R-F-11: 댓글 삭제 (통합)

- 출처: 04#R-F-11 §통합 ✅
- 테스트 레벨: 통합
- 대상: `DELETE /api/articles/{slug}/comments/{id}`
- Happy path: 작성자 본인 → 204
- Failure path: 타인 시도 → 403
- 테스트 파일: `tests/integration/test_comments_routes.py::test_delete_*`

### R-F-12: 내 글 목록 (통합)

- 출처: 04#R-F-12 §통합 ✅
- 테스트 레벨: 통합
- 대상: `GET /api/articles?author={username}`
- Happy path: 본인 username → 200 + 본인 글만
- Failure path: 잘못된 username → 200 + 빈 배열
- 테스트 파일: `tests/integration/test_articles_routes.py::test_list_with_author_filter`

### R-F-13: 댓글 수정 (통합)

- 출처: 04#R-F-13 §통합 ✅
- 테스트 레벨: 통합
- 대상: `PUT /api/articles/{slug}/comments/{id}`
- Happy path: 작성자 본인 + 비어있지 않은 body → 200 + 갱신된 comment
- Failure path:
  - 실패-1: 타인 시도 → 403
  - 실패-2: 빈 body → 422
- 테스트 파일: `tests/integration/test_comments_routes.py::test_update_*`

### R-N-01: API p95 < 200ms (통합/성능)

- 출처: 04#R-N-01 §통합 ✅
- 테스트 레벨: 통합 (성능 측정)
- 대상: `GET /api/articles?limit=20`
- Happy path: 100건 시드 후 100회 호출 → `statistics.quantiles([..], n=20)[18]` (p95) < 200ms
- Failure path: 미달 시 테스트 실패 → eager loading 점검
- 테스트 파일: `tests/integration/test_performance.py::test_articles_list_p95`

### R-N-04: 시크릿 누락 시 부팅 실패 (통합)

- 출처: 04#R-N-04 §통합 ✅
- 테스트 레벨: 통합
- 대상: FastAPI 앱 부팅
- Happy path: `JWT_SECRET` 환경 변수 설정 → 앱 인스턴스 생성 성공
- Failure path: `JWT_SECRET` 미설정 → 부팅 단계에서 ValidationError (pydantic-settings)
- 테스트 파일: `tests/integration/test_bootstrap.py`

### R-N-05: XSS / SQL injection 안전 (통합)

- 출처: 04#R-N-05 §통합 ✅
- 테스트 레벨: 통합
- 대상: `POST /api/articles` body에 XSS 페이로드 → `GET /api/articles/{slug}` 응답
- Happy path: 본문 `<script>alert(1)</script>` 저장 → 응답에서 그대로 텍스트로 반환됨 (저장은 원본, escape는 프론트엔드 JSX 렌더링 단계에서 수행 — React 기본). API 응답 자체는 escape 안 함이 RealWorld spec 표준
- Failure path: 본문에 SQL injection 패턴 `'; DROP TABLE articles; --` → SQLAlchemy 파라미터 바인딩으로 무력화, DB 무결성 영향 없음
- 테스트 파일: `tests/integration/test_security.py::test_xss_payload_safe`, `test_sql_injection_safe`

## 3. E2E 테스트 카탈로그

### F-04: 골든패스 (E2E)

- 출처: 05#F-04 §E2E ✅
- 테스트 레벨: E2E
- 대상: 회원가입 → 로그인 → 글 작성 → 댓글 작성 → 댓글 수정 → 글 수정 → 글 삭제 (7단계, v0.2 갱신)
- Happy path: 모든 단계 PASS + 각 단계 스크린샷 `docs/features/<slug>/screenshots/` 저장
- Failure path: 한 단계 fail → gstack `/qa`가 실패 로그 + 스크린샷 보관, PR 머지 차단
- 도구: gstack `/qa` (외부)
- 비고: F-04 단위·통합 N/A 결정 (v0.2) — 본 E2E가 F-04 검증을 대체

### R-N-02: FCP < 1.5s (E2E)

- 출처: 04#R-N-02 §E2E ✅
- 테스트 레벨: E2E (성능 측정)
- 대상: 게시글 목록 페이지 첫 로드
- Happy path: gstack `/qa` Performance 트레이스 → FCP 메트릭 < 1500ms
- Failure path: 미달 시 코드 스플리팅(React.lazy) 점검
- 도구: gstack `/qa` (외부)

### R-N-05: XSS payload 브라우저 escape (E2E)

- 출처: 04#R-N-05 §E2E ✅
- 테스트 레벨: E2E
- 대상: 게시글 본문에 `<script>alert(1)</script>` 작성 → 상세 페이지에서 alert 미발화
- Happy path: alert 안 뜨고 텍스트로 escape되어 표시 (React JSX 기본 escape)
- Failure path: alert 뜨면 즉시 BLOCK + 템플릿 escape 설정 점검
- 도구: gstack `/qa` (1회 페이로드 시도)

## 4. 레벨 매트릭스 (단위·통합·E2E)

본 표는 R-/F-ID별 적용 결정을 ✅(적용) 또는 N/A(부적합)로 명시한다. 미작성 셀 금지 (ADR-0023).

| ID | 단위 | 통합 | E2E | 출처 / 비고 |
|---|---|---|---|---|
| R-F-01 | ✅ | ✅ | ✅ | 04#R-F-01 + F-04 골든패스 1단계 |
| R-F-02 | ✅ | ✅ | ✅ | 04#R-F-02 + F-04 골든패스 2단계 |
| R-F-03 | ✅ | ✅ | N/A | 04#R-F-03 §E2E N/A (라우트 가드 동작은 다른 흐름에 포함) |
| R-F-04 | ✅ | ✅ | ✅ | 04#R-F-04 + F-04 (홈 진입) |
| R-F-05 | ✅ | ✅ | ✅ | 04#R-F-05 + F-04 (글 상세 진입) |
| R-F-06 | ✅ | ✅ | ✅ | 04#R-F-06 + F-04 골든패스 3단계 |
| R-F-07 | ✅ | ✅ | ✅ | 04#R-F-07 + F-04 골든패스 6단계 |
| R-F-08 | ✅ | ✅ | ✅ | 04#R-F-08 + F-04 골든패스 7단계 (hard delete + CASCADE) |
| R-F-09 | ✅ | ✅ | ✅ | 04#R-F-09 + F-04 골든패스 4단계 |
| R-F-10 | ✅ | ✅ | N/A | 04#R-F-10 — 댓글 목록은 R-F-05 상세 진입에 포함 |
| R-F-11 | ✅ | ✅ | N/A | 04#R-F-11 — 골든패스에 댓글 삭제 미포함 (수정만 포함, 추후 확장) |
| R-F-12 | ✅ | ✅ | N/A | 04#R-F-12 — 시간 부족 시 컷 후보 (P2) |
| R-F-13 | ✅ | ✅ | ✅ | 04#R-F-13 + F-04 골든패스 5단계 (댓글 수정) |
| R-N-01 | N/A | ✅ | N/A | 04#R-N-01 — API p95 측정은 통합 레벨 |
| R-N-02 | N/A | N/A | ✅ | 04#R-N-02 — FCP 측정은 gstack E2E |
| R-N-03 | ✅ | ✅ | N/A | 04#R-N-03 — DB 직접 조회로 형식 검증 |
| R-N-04 | ✅ | ✅ | N/A | 04#R-N-04 — 환경변수 누락 시 부팅 실패 |
| R-N-05 | N/A | ✅ | ✅ | 04#R-N-05 — 단위 레벨 검증 어려움 (escape는 프론트엔드 + DB는 ORM). 통합·E2E로 커버 |
| R-N-06 | ✅ | N/A | N/A | 04#R-N-06 — pytest --cov 측정 자체 |
| F-01 | ✅ | ✅ | ✅ | 05#F-01 — R-F-01·R-F-02·R-F-03 합 |
| F-02 | ✅ | ✅ | ✅ | 05#F-02 — R-F-04~R-F-08·R-F-12 합 |
| F-03 | ✅ | ✅ | ✅ | 05#F-03 — R-F-09·R-F-10·R-F-11·R-F-13 합 |
| F-04 | N/A | N/A | ✅ | 05#F-04 — UI 단위/통합 N/A 결정 (v0.2). 골든패스 1회 |
