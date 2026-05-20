---
doc_type: hld
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

# realworld-py — High-Level Design (HLD)

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, ADR-0031 신설 — 06에서 분리된 모듈 분해 본체) |

## 1. 핵심 모듈 / 컴포넌트

본 시스템은 백엔드 5개 + 프론트엔드 4개 = 9개 모듈로 분해된다. 각 모듈은 08-lld-module-spec에서 LLD 상세를 작성한다.

| 모듈 | 책임 | 의존 | 08에서 상세 |
|---|---|---|---|
| M-API-Router (FastAPI 라우터) | HTTP 요청 라우팅, Pydantic 검증, 인증 헤더 파싱, 응답 직렬화 | M-Auth-Service, M-Article-Service, M-Comment-Service, M-Auth-Middleware | 08 §1 모듈 개요 §1.1 |
| M-Auth-Service | 회원가입(bcrypt 해시) + 로그인(자격증명 검증 + JWT 발급) + 현재 사용자 조회 | M-User-Repo, M-JWT-Util | 08 §1.2 |
| M-Article-Service | 게시글 CRUD + slug 생성·충돌 회피 (숫자 suffix) + 작성자 검증 + 페이지네이션 | M-Article-Repo, M-Comment-Repo (hard delete CASCADE) | 08 §1.3 |
| M-Comment-Service | 댓글 CRUD (수정 포함, R-F-13) + 작성자 검증 | M-Comment-Repo | 08 §1.4 |
| M-Auth-Middleware | JWT 검증 dependency (`require_auth`, `require_author`) | M-JWT-Util | 08 §1.5 |
| M-FE-Pages | SPA 페이지 — Home/Article/Editor/Login/Register/Profile | M-FE-Components, M-FE-ApiClient, M-FE-AuthStore | (FE는 본 메타 범위 외 — 본 프로젝트는 BE 학습 1차) |
| M-FE-Components | 공통 UI 컴포넌트 — Button, Input, Card, CommentItem 등 | (없음) | (FE 범위 외) |
| M-FE-ApiClient | fetch 래퍼, `Authorization: Token` 헤더 자동 첨부, 에러 매핑 | M-FE-AuthStore (토큰) | (FE 범위 외) |
| M-FE-AuthStore | JWT localStorage 보관, 로그인 상태 zustand store | (없음) | (FE 범위 외) |

> 본 프로젝트는 백엔드 학습이 1차 목표. FE 모듈 LLD는 12-scaffolding/python.md 작성 후 시간 여유에 따라 별도로 작성. 08-lld-module-spec은 BE 5개 모듈만 정식 LLD.

## 2. 모듈 간 데이터 흐름

### 2.1 골든패스 데이터 흐름 (회원가입 → 글 작성 → 댓글 작성)

```
[Browser] ──POST /api/users (body: {user: {username, email, password}})──▶ [M-API-Router]
                                                                                │
                                                                                ▼
                                                                       [M-Auth-Service]
                                                                                │ bcrypt 해시
                                                                                │ JWT 발급
                                                                                ▼
                                                                       [M-User-Repo] ──▶ [SQLite users]
                                                                                │
                                                                                ▼
[Browser] ◀──201 {user: {..., token}}──────────────────────────────────── [M-API-Router]
   │ JWT를 localStorage 저장
   │
   ▼
[Browser] ──POST /api/articles (Authorization: Token <JWT>)─────────────▶ [M-API-Router]
                                                                                │
                                                                                ▼
                                                              [M-Auth-Middleware: require_auth]
                                                                                │ JWT 검증 성공
                                                                                ▼
                                                                       [M-Article-Service]
                                                                                │ slug 생성 + 충돌 회피
                                                                                ▼
                                                                    [M-Article-Repo] ──▶ [SQLite articles]
                                                                                │
                                                                                ▼
[Browser] ◀──201 {article: {...}}────────────────────────────────────── [M-API-Router]
   │
   ▼
[Browser] ──POST /api/articles/{slug}/comments (Authorization: Token)──▶ [M-API-Router]
                                                                                │
                                                                                ▼
                                                              [M-Auth-Middleware: require_auth]
                                                                                │
                                                                                ▼
                                                                       [M-Comment-Service]
                                                                                ▼
                                                                    [M-Comment-Repo] ──▶ [SQLite comments]
```

### 2.2 권한 거부 흐름 (타인의 글 삭제 시도)

```
[Browser User-B] ──DELETE /api/articles/{slug-by-User-A}──▶ [M-API-Router]
                                                                  │
                                                                  ▼
                                                    [M-Auth-Middleware: require_auth] (PASS)
                                                                  │
                                                                  ▼
                                                          [M-Article-Service]
                                                                  │ slug → article 조회
                                                                  │ article.author_id != current_user.id
                                                                  ▼
                                                       Forbidden 예외 발생
                                                                  │
                                                                  ▼
[Browser] ◀──403 {errors: {body: ["권한이 없습니다"]}}───── [M-API-Router 에러 핸들러]
```

### 2.3 게시글 hard delete CASCADE 흐름

```
[Browser Owner] ──DELETE /api/articles/{slug}──▶ [M-API-Router]
                                                       │
                                                       ▼
                                            [M-Auth-Middleware: require_auth + require_author]
                                                       │
                                                       ▼
                                                [M-Article-Service.delete]
                                                       │ DB 트랜잭션 BEGIN
                                                       ▼
                                            [M-Comment-Repo] (article_id FK CASCADE로 자동)
                                            [M-Article-Repo.delete] ── DB 트랜잭션 COMMIT
                                                       │
                                                       ▼
[Browser] ◀──204 No Content
```

## 3. 비기능 대응

| 비기능 R-ID | 대응 전략 | 상세 |
|---|---|---|
| R-N-01 (API p95 < 200ms) | 인덱스 + eager loading | `articles.slug` UNIQUE 인덱스, `articles.created_at` 인덱스. SQLAlchemy `selectinload`로 author 조인 시 N+1 회피. 게시글 100건 시드 후 통합 테스트로 측정 |
| R-N-02 (FCP < 1.5s) | Vite 번들 + 코드 스플리팅 | React.lazy로 페이지별 chunk 분리. 게시글 목록 페이지는 진입 시 첫 화면 우선 렌더. 측정은 gstack `/qa` Performance 트레이스 1회 |
| R-N-03 (bcrypt) | passlib[bcrypt] | rounds=12 (기본). 평문/SHA·MD5 단방향 사용 금지. UserService.register에서 단방향 적용 |
| R-N-04 (시크릿 환경변수) | pydantic-settings + .env | `JWT_SECRET`, `DATABASE_URL` 등은 `Settings` 클래스로 로드, 미설정 시 부팅 단계 명시적 예외. .env는 .gitignore 강제 + PreToolUse 훅 보안 파일 Write 차단 |
| R-N-05 (XSS / SQL injection) | ORM 파라미터 바인딩 + React JSX 기본 escape | SQLAlchemy 파라미터 바인딩 사용, raw SQL 금지. React는 JSX 문자열 자동 escape (위험은 `dangerouslySetInnerHTML` 사용 시인데 본 프로젝트는 0건). FastAPI Pydantic validator로 입력 길이 상한 부과 |
| R-N-06 (단위 테스트 ≥ 80%) | pytest-cov + 적용 범위 한정 | `UserService`·`ArticleService`·`CommentService`·인증 미들웨어만 측정. `pytest.ini`에 `--cov=backend/realworld/services --cov-fail-under=80` 설정. 13-test-design §01-strategy 정식화 |

## 4. 외부 인터페이스 윤곽

- **REST API (Frontend → Backend)**: RealWorld spec 준수. 09-lld-api-spec에서 OpenAPI 형식으로 정식화.
- **외부 서비스 호출**: 없음
- **이벤트 / 메시지 큐**: 없음
- **파일 업로드 / 다운로드**: 없음 (프로필 이미지 Out of Scope)
- **CLI / 백그라운드 작업**: seed 스크립트 1개 (`backend/scripts/seed_articles.py`, 게시글 100건 생성 — 12-scaffolding §7 자산)
