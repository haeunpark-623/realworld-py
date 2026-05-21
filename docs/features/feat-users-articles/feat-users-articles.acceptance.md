---
doc_type: feature-acceptance
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

# feat-users-articles — Acceptance Criteria

> Issue #4 / Sprint 1 / I-04. 10 AC (Given/When/Then) + 11 DoD (D-04-1~11) + 비기능·회귀 인수.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 10 AC + 11 DoD 매핑 |

## 1. 인수 기준 (Given/When/Then)

### AC-01 — Article 모델 + Alembic 0003 진행

- **Given**: I-03 머지 후 alembic 0002 (head)
- **When**: `cd backend && uv run alembic upgrade head`
- **Then**: 0003_articles_tags 적용. `alembic current` → `0003 (head)`. SQLite에 `articles`, `tags`, `article_tags` 3 테이블 존재 + Article.author_id FK CASCADE 명시

### AC-02 — utils/slug 슬러그 생성

- **Given**: `from realworld.utils.slug import slugify`
- **When**: `slugify("My First Article")` 호출
- **Then**: `"my-first-article"` 반환. 한글·특수문자는 ASCII drop 후 kebab. 빈 결과 시 `"article"` fallback

### AC-03 — ArticleService 5 메서드 + 작성자 검증

- **Given**: `from realworld.services.article import ArticleService`
- **When**: `inspect.getmembers(ArticleService, callable)` 호출
- **Then**: `list`, `get_by_slug`, `create`, `update`, `delete` 5 async 메서드 + 작성자 검증 시 Forbidden raise

### AC-04 — POST /api/users 회원가입 happy path

- **Given**: backend 부팅 + DB empty
- **When**: `POST /api/users` body `{"user":{"username":"jane","email":"jane@example.com","password":"supersecret"}}`
- **Then**: 200 + `{"user":{"username":"jane","email":"jane@example.com","token":"eyJ...","bio":null,"image":null}}` 응답

### AC-05 — POST /api/users/login happy path

- **Given**: jane 가입 완료
- **When**: `POST /api/users/login` body `{"user":{"email":"jane@example.com","password":"supersecret"}}`
- **Then**: 200 + `token` 포함 응답. 잘못된 비밀번호 시 422 `{"errors":{"body":["이메일 또는 비밀번호가 올바르지 않습니다"]}}`

### AC-06 — GET /api/user 현재 사용자

- **Given**: jane JWT 발급 완료
- **When**: `GET /api/user` 헤더 `Authorization: Token <JWT>`
- **Then**: 200 + jane 정보 응답. 헤더 누락 시 401 `{"errors":{"body":["인증 토큰이 유효하지 않습니다"]}}`

### AC-07 — POST /api/articles 작성 + slug 충돌 시 suffix

- **Given**: jane JWT
- **When**: 동일 title `"My Post"`로 2회 연속 `POST /api/articles`
- **Then**: 1번째 `"slug":"my-post"` + 2번째 `"slug":"my-post-2"`. tagList 입력 시 신규 tag INSERT

### AC-08 — PUT /api/articles/{slug} 작성자/타인 분기

- **Given**: jane 게시글 `"my-post"` 작성. bob 가입 + JWT
- **When**: bob JWT로 `PUT /api/articles/my-post`
- **Then**: 403 `{"errors":{"body":["권한이 없습니다"]}}`. jane JWT로는 200 + 변경된 article 응답

### AC-09 — DELETE /api/articles/{slug} 작성자/타인 분기

- **Given**: jane 게시글 작성. bob 가입
- **When**: bob JWT로 `DELETE /api/articles/my-post`
- **Then**: 403. jane JWT로는 204 No Content. 이후 `GET /api/articles/my-post` → 404

### AC-10 — GET /api/articles?author= 필터 + 빈 결과

- **Given**: jane·bob 각 2 article. unknown user `nobody`
- **When**: `GET /api/articles?author=jane`
- **Then**: 200 + jane 2건만. `?author=nobody` → 200 + `{"articles":[],"articlesCount":0}` (404 아님)

## 2. Definition of Done (D-06)

- [ ] **D-04-1**: `models/article.py` Article + Tag + article_tags M2M + `models/__init__.py` re-export
- [ ] **D-04-2**: `migrations/versions/0003_articles_tags.py` autogenerate + upgrade/downgrade 함수
- [ ] **D-04-3**: `utils/slug.py` slugify + unique_slug
- [ ] **D-04-4**: `repositories/article.py` ArticleRepo 5 메서드 + selectinload N+1 회피
- [ ] **D-04-5**: `services/article.py` ArticleService 5 메서드 + 작성자 검증
- [ ] **D-04-6**: `schemas/user.py` + `schemas/article.py` Pydantic (RealWorld 래핑 형식)
- [ ] **D-04-7**: `routers/users.py` 3 라우트 + `routers/articles.py` 5 라우트
- [ ] **D-04-8**: `main.py` 라우터 등록 + RealWorldError 핸들러 (422 한글)
- [ ] **D-04-9**: 단위 테스트 ≥ 13건 PASS (test_slug 5 + test_article_service 8)
- [ ] **D-04-10**: 통합 테스트 ≥ 14건 PASS (test_users_routes ≥ 7 + test_articles_routes ≥ 12 = ≥ 19, 14건 조건 충족)
- [ ] **D-04-11**: R-F-12 `?author=` 필터 통합 테스트 1건 명시 + GitHub Actions `backend-ci` workflow green

## 3. 비기능 인수

- **R-N-01 응답 시간** (p95 < 200ms): 본 PR는 미측정. I-05에서 100건 시드 후 측정 (비목표 #2). 통합 테스트 단건 응답 < 500ms 확인 정도
- **R-N-03 보안 — 비밀번호**: I-03 bcrypt round=12 유지. 본 PR 변경 0
- **R-N-04 보안 — JWT secret**: I-03 환경변수 로드 유지. 본 PR 변경 0
- **R-N-05 입력 검증**: Pydantic v2가 422 자동 응답. 한글 메시지는 RealWorldError 핸들러 매핑

## 4. 회귀 인수

- **기존 단위 20건 PASS 유지**: 3 health + 3 user_repo + 3 security + 3 jwt + 8 auth_service
- **alembic 0002 history 유지**: downgrade 0002 가능 (rollback 시)
- **`/health` 라우트 변경 0**: GET /health 200 응답 유지
- **외부 의존 추가 0**: pyproject.toml dependencies 변경 0. uv.lock 변경 0
- **`.env.example` 변경 0**: 신규 환경변수 0
