---
doc_type: api-spec
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-09, R-F-10, R-F-11, R-F-12, R-F-13]
  F-ID: [F-01, F-02, F-03]
  supersedes: null
---

# realworld-py — API Spec (LLD — 외부 인터페이스)

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, RealWorld spec 준수 + R-F-13 PUT comment 신설) |

## 1. 개요

- **Base URL (dev)**: `http://localhost:8000/api`
- **인증 헤더**: `Authorization: Token <JWT>` (RealWorld spec 관례, 일반적인 `Bearer`와 다름)
- **요청·응답 형식**: JSON. RealWorld spec의 래핑 객체 형식 (`{user: {...}}`, `{article: {...}}` 등) 준수
- **에러 응답**: `{errors: {field: ["메시지"]}}`. 메시지는 한글 (NFR-03)
- **OpenAPI**: FastAPI 자동 생성 — `GET /docs` (Swagger UI), `GET /openapi.json`
- **R-F-13 비표준 엔드포인트**: RealWorld spec엔 PUT comment 표준 없음. 본 프로젝트에서 `PUT /api/articles/{slug}/comments/{id}`로 신설 (04-srs §6.6 결정).

## 2. 엔드포인트 목록

| 메서드 | 경로 | 목적 | F-ID | R-ID |
|---|---|---|---|---|
| POST | `/api/users` | 회원가입 | F-01 | R-F-01 |
| POST | `/api/users/login` | 로그인 | F-01 | R-F-02 |
| GET | `/api/user` | 현재 사용자 조회 | F-01 | R-F-03 |
| GET | `/api/articles` | 게시글 목록 (페이징·필터) | F-02 | R-F-04, R-F-12 |
| GET | `/api/articles/{slug}` | 게시글 상세 | F-02 | R-F-05 |
| POST | `/api/articles` | 게시글 작성 | F-02 | R-F-06 |
| PUT | `/api/articles/{slug}` | 게시글 수정 | F-02 | R-F-07 |
| DELETE | `/api/articles/{slug}` | 게시글 hard delete | F-02 | R-F-08 |
| GET | `/api/articles/{slug}/comments` | 댓글 목록 | F-03 | R-F-10 |
| POST | `/api/articles/{slug}/comments` | 댓글 작성 | F-03 | R-F-09 |
| PUT | `/api/articles/{slug}/comments/{id}` | 댓글 수정 (비표준, R-F-13) | F-03 | R-F-13 |
| DELETE | `/api/articles/{slug}/comments/{id}` | 댓글 삭제 | F-03 | R-F-11 |

## 3. 엔드포인트 상세

### POST /api/users

회원가입. 가입 즉시 JWT 발급.

- **Request**
  - Body (`application/json`):
    ```json
    { "user": { "username": "jane", "email": "jane@example.com", "password": "supersecret" } }
    ```
  - Pydantic 검증: username ≥ 1, email RFC 5322, password ≥ 8자
  - 인증 헤더: 불필요

- **Response 200** (실제 201)
  ```json
  { "user": { "username": "jane", "email": "jane@example.com", "token": "eyJ...", "bio": null, "image": null } }
  ```

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 422 | email 중복 | `{"errors": {"email": ["이미 사용 중인 이메일입니다"]}}` |
| 422 | username 중복 | `{"errors": {"username": ["이미 사용 중인 username입니다"]}}` |
| 422 | 검증 실패 (필수·길이·형식) | `{"errors": {"<field>": ["..."]}}` |
| 500 | 내부 오류 | `{"errors": {"body": ["서버 오류가 발생했습니다"]}}` |

- **테스트 시나리오**: 정상 가입 (Happy) / 이메일 중복 (Failure-1) / 비밀번호 7자 (Failure-2) → 13/02-catalog §2.1 R-F-01

### POST /api/users/login

로그인. 자격증명 검증 후 JWT 발급.

- **Request**
  - Body: `{ "user": { "email": "jane@example.com", "password": "supersecret" } }`
  - 인증 헤더: 불필요

- **Response 200**
  ```json
  { "user": { "username": "jane", "email": "jane@example.com", "token": "eyJ...", "bio": null, "image": null } }
  ```

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 422 | 이메일 미존재 OR 비밀번호 불일치 | `{"errors": {"body": ["이메일 또는 비밀번호가 올바르지 않습니다"]}}` (구분 누설 안 함) |
| 500 | 내부 오류 | `{"errors": {"body": ["서버 오류가 발생했습니다"]}}` |

- **테스트 시나리오**: 정상 로그인 / 비밀번호 불일치 / 미존재 이메일 → 13/02-catalog §2.1 R-F-02

### GET /api/user

현재 로그인된 사용자 정보 조회. JWT 검증 진입점.

- **Request**
  - 인증 헤더: `Authorization: Token <JWT>` 필수

- **Response 200**
  ```json
  { "user": { "username": "jane", "email": "jane@example.com", "token": "eyJ...", "bio": null, "image": null } }
  ```

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 401 | JWT 누락/위조/만료 | `{"errors": {"body": ["인증 토큰이 유효하지 않습니다"]}}` |

- **테스트 시나리오**: 유효 JWT / 만료 JWT / 위조 JWT → 13/02-catalog §1.1 R-F-03

### GET /api/articles

게시글 목록 조회. limit/offset 페이지네이션 + author 필터.

- **Request**
  - Query: `limit` (default 20, max 100) · `offset` (default 0, ≥ 0) · `author` (optional username)
  - 인증 헤더: optional (있으면 favorited 필드 계산 가능 — 본 MVP는 favorited Out of Scope)

- **Response 200**
  ```json
  {
    "articles": [
      { "slug": "my-post", "title": "...", "description": "...", "body": "...", "tagList": [], "createdAt": "...", "updatedAt": "...", "author": { "username": "jane", "bio": null, "image": null } }
    ],
    "articlesCount": 42
  }
  ```

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 422 | limit > 100 또는 offset < 0 | `{"errors": {"<query>": ["..."]}}` |
| 500 | DB 오류 | `{"errors": {"body": ["서버 오류가 발생했습니다"]}}` |

- **테스트 시나리오**: 정상 페이징 / limit=10 offset=20 / author 필터 / limit=200 거부 → 13/02-catalog §2.2 R-F-04·R-F-12

### GET /api/articles/{slug}

게시글 상세 조회.

- **Request**
  - Path: `slug` (string)
  - 인증 헤더: optional

- **Response 200**
  ```json
  { "article": { "slug": "my-post", "title": "...", "description": "...", "body": "...", "tagList": [], "createdAt": "...", "updatedAt": "...", "author": { "username": "jane", "bio": null, "image": null } } }
  ```

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 404 | slug 미존재 | `{"errors": {"body": ["게시글을 찾을 수 없습니다"]}}` |

- **테스트 시나리오**: 존재 slug / 미존재 slug → 13/02-catalog §2.2 R-F-05

### POST /api/articles

게시글 작성. 로그인 필수. slug 자동 생성 + 충돌 시 숫자 suffix.

- **Request**
  - Body: `{ "article": { "title": "My Post", "description": "...", "body": "...", "tagList": ["intro"] } }`
  - 인증 헤더: 필수
  - Pydantic: title ≥ 1자, body ≥ 1자, description optional, tagList optional

- **Response 200** (실제 201)
  ```json
  { "article": { "slug": "my-post", "title": "My Post", ... } }
  ```
  - 동명 제목 두 번째 작성 시: `"slug": "my-post-2"`, 세 번째: `"slug": "my-post-3"`

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 401 | JWT 누락/만료 | `{"errors": {"body": ["인증 토큰이 유효하지 않습니다"]}}` |
| 422 | title/body 누락 | `{"errors": {"<field>": ["..."]}}` |
| 500 | DB 오류 | `{"errors": {"body": ["서버 오류가 발생했습니다"]}}` |

- **테스트 시나리오**: 정상 작성 / 동명 제목 → suffix / JWT 만료 → 401 / title 누락 → 13/02-catalog §2.2 R-F-06

### PUT /api/articles/{slug}

게시글 수정. 작성자 한정.

- **Request**
  - Body: `{ "article": { "title?": "...", "description?": "...", "body?": "...", "tagList?": [...] } }` (부분 갱신)
  - 인증 헤더: 필수

- **Response 200**
  ```json
  { "article": { "slug": "my-post", "title": "갱신된 제목", ... } }
  ```
  - 본 MVP는 *slug 재생성 안 함* (제목 변경 후에도 기존 slug 유지)

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 401 | JWT 누락/만료 | `{"errors": {"body": ["인증 토큰이 유효하지 않습니다"]}}` |
| 403 | 타인의 글 수정 시도 | `{"errors": {"body": ["권한이 없습니다"]}}` |
| 404 | slug 미존재 | `{"errors": {"body": ["게시글을 찾을 수 없습니다"]}}` |
| 422 | 검증 실패 | `{"errors": {"<field>": ["..."]}}` |

- **테스트 시나리오**: 작성자 본인 / 타인 시도 → 403 / 미존재 slug → 404 → 13/02-catalog §2.2 R-F-07

### DELETE /api/articles/{slug}

게시글 hard delete (작성자 한정). 댓글 FK CASCADE로 함께 삭제.

- **Request**
  - 인증 헤더: 필수

- **Response 200** (실제 204 No Content)
  ```
  (body 없음)
  ```

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 401 | JWT 누락/만료 | `{"errors": {"body": ["인증 토큰이 유효하지 않습니다"]}}` |
| 403 | 타인의 글 삭제 시도 | `{"errors": {"body": ["권한이 없습니다"]}}` |
| 404 | slug 미존재 (이미 삭제 포함) | `{"errors": {"body": ["이미 삭제된 글입니다"]}}` |

- **테스트 시나리오**: 작성자 본인 → 204 + 댓글 CASCADE 검증 / 타인 시도 → 403 → 13/02-catalog §2.2 R-F-08

### GET /api/articles/{slug}/comments

댓글 목록 조회. 최신순.

- **Request**
  - 인증 헤더: optional

- **Response 200**
  ```json
  {
    "comments": [
      { "id": 12, "body": "good post", "createdAt": "...", "updatedAt": "...", "author": { "username": "bob", "bio": null, "image": null } }
    ]
  }
  ```

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 404 | slug 미존재 | `{"errors": {"body": ["게시글을 찾을 수 없습니다"]}}` |

- **테스트 시나리오**: 정상 / 댓글 0건 → 빈 배열 / 미존재 slug → 404 → 13/02-catalog §2.3 R-F-10

### POST /api/articles/{slug}/comments

댓글 작성. 로그인 필수.

- **Request**
  - Body: `{ "comment": { "body": "good post" } }`
  - 인증 헤더: 필수

- **Response 200** (실제 201)
  ```json
  { "comment": { "id": 12, "body": "good post", "createdAt": "...", "updatedAt": "...", "author": { ... } } }
  ```

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 401 | JWT 누락/만료 | `{"errors": {"body": ["인증 토큰이 유효하지 않습니다"]}}` |
| 404 | slug 미존재 | `{"errors": {"body": ["게시글을 찾을 수 없습니다"]}}` |
| 422 | body 빈 문자열 | `{"errors": {"body": ["댓글 내용을 입력해 주세요"]}}` |

- **테스트 시나리오**: 정상 작성 / 비로그인 → 401 / 빈 body → 422 → 13/02-catalog §2.3 R-F-09

### PUT /api/articles/{slug}/comments/{id}

댓글 수정 (작성자 한정, R-F-13). RealWorld spec 비표준 — 본 프로젝트 신설.

- **Request**
  - Body: `{ "comment": { "body": "수정된 댓글" } }`
  - 인증 헤더: 필수

- **Response 200**
  ```json
  { "comment": { "id": 12, "body": "수정된 댓글", "updatedAt": "...", ... } }
  ```

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 401 | JWT 누락/만료 | `{"errors": {"body": ["인증 토큰이 유효하지 않습니다"]}}` |
| 403 | 타인의 댓글 수정 시도 | `{"errors": {"body": ["권한이 없습니다"]}}` |
| 404 | comment id 미존재 또는 slug 불일치 | `{"errors": {"body": ["댓글을 찾을 수 없습니다"]}}` |
| 422 | body 빈 문자열 | `{"errors": {"body": ["댓글 내용을 입력해 주세요"]}}` |

- **테스트 시나리오**: 작성자 본인 / 타인 시도 → 403 / 빈 body → 422 → 13/02-catalog §2.3 R-F-13

### DELETE /api/articles/{slug}/comments/{id}

댓글 삭제 (작성자 한정).

- **Request**
  - 인증 헤더: 필수

- **Response 200** (실제 204)
  ```
  (body 없음)
  ```

- **Response 4xx/5xx**

| 상태 | 조건 | Body |
|---|---|---|
| 401 | JWT 누락/만료 | `{"errors": {"body": ["인증 토큰이 유효하지 않습니다"]}}` |
| 403 | 타인 시도 | `{"errors": {"body": ["권한이 없습니다"]}}` |
| 404 | comment 미존재 | `{"errors": {"body": ["이미 삭제된 댓글입니다"]}}` |

- **테스트 시나리오**: 작성자 본인 → 204 / 타인 시도 → 403 → 13/02-catalog §2.3 R-F-11

## 4. Webhook / 콜백

본 프로젝트는 webhook·콜백을 사용하지 않는다. 외부 시스템 연동 0건.

## 5. Rate Limit / Quota

학습 컨텍스트 + 단일 환경 운영 + 1~5명 동시 사용자 가정으로 본 MVP는 *Rate Limit 미적용*. 다음 시나리오는 후속 검토 항목 (현 시점 BLOCK 아님):

- 로그인 5회 연속 실패 후 일시 차단 — 04-srs R-F-02 Failure-3 Out of Scope 명시
- 동일 IP에서 회원가입 N회 제한
- 게시글 작성 N회/min 제한

운영 환경 학습이 필요해지면 `slowapi` (FastAPI 호환) 도입 검토.
