---
doc_type: wbs
version: v0.7 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: operations
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-09, R-F-10, R-F-11, R-F-12, R-F-13, R-N-01, R-N-02, R-N-03, R-N-04, R-N-05, R-N-06]
  F-ID: [F-01, F-02, F-03, F-04]
  supersedes: null
---

# realworld-py — WBS

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.7 | 2026-05-21 | woosung.ahn@bespinglobal.com | Issue #3 머지 완료(PR #13) + Issue #4 작업 진입 — `I-04` status:in-review 전이. PR #14 (feat/users-articles-issue-4). feat(backend) 5 + test(backend) 3 + fix(backend) 2 + chore(backend) 1 + docs(feat) 1 = 12 커밋. Article + Tag M2M 모델 + alembic 0003 + ArticleRepo selectinload + ArticleService 5 메서드 + utils/slug + Pydantic schemas + 8 라우트(users 3 + articles 5) + main.py 라우터 등록 + RealWorldError handler inline + 단위 13 + 통합 19 = 52 passed. errors.InvalidCredentials.status_code 401→422 정합 갱신 (9-api-spec 정합, code-review F1). ArticleService.update refresh→get_by_slug reload 인라인 결정 (selectin lazy 회귀 회피, F2). 다음 진입: I-05 seed + p95 측정 |
| v0.6 | 2026-05-21 | woosung.ahn@bespinglobal.com | Issue #2 머지 완료(PR #12) + Issue #3 작업 진입 — `I-03` status:in-review 전이. PR #13 (feat/auth-service-issue-3). feat(backend) 3 + test(backend) 3 + chore(backend) 1 + docs(feat) 1 = 7 커밋. AuthService 3 메서드 + utils/security(bcrypt) + utils/jwt(python-jose HS256) + deps/auth(require_auth) + errors(6 도메인 예외) + 단위 테스트 14 PASS. FRISK-01 (passlib + bcrypt 4.x 호환) 실 발현 → bcrypt 직접 사용. 다음 진입: I-04 users router + articles router |
| v0.5 | 2026-05-20 | woosung.ahn@bespinglobal.com | Issue #1 머지 완료(PR #11) + Issue #2 작업 진입 — `I-02` status:in-review 전이. PR #12 (feat/user-model-issue-2). feat(backend)+test(backend)+docs(feat) 6 커밋. User 모델·UserRepo 3 메서드·alembic 0002 add_users + 단위 테스트 3 PASS. 다음 진입: I-03 AuthService + bcrypt + JWT |
| v0.4 | 2026-05-20 | woosung.ahn@bespinglobal.com | Issue #1 머지 진입 — `I-01` status:in-review 전이. PR #11 (feat/bootstrap-backend-issue-1). docs(boot)+chore(backend) 8 커밋. 다음 진입: I-02 User 모델 + 마이그레이션 |
| v0.3 | 2026-05-20 | woosung.ahn@bespinglobal.com | §7 sprint-bootstrap YAML 정합 갱신 — milestone/due 키 추가, ADR-0021 title 형식(`<type>(<area>): <summary>`), priority:P0/P1 라벨 정합 |
| v0.2 | 2026-05-20 | woosung.ahn@bespinglobal.com | 일정 16h(2일 × 8h) 기준 재조정 — §0·§6 절대 시간 단위로 명시. effort 단위 의미 재정의(AI 페어 가속 환산). RISK-01 §3.1과 동기 |
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-wbs` Phase 3/4, Sprint 2 × Issue 10 — R-/F-ID 100% 매핑, §7 sprint-bootstrap YAML 작성) |

## 0. 개요

본 WBS는 **2 sprint × 10 issue** 구조. **실제 마감 = 16h (2일 × 8h, 점심·회의 제외 순 작업 시간)**.

### 0.1 effort 단위 재정의

본 프로젝트의 `Estimated Effort` 필드(schema 강제 — 0.5d/1d/2d/3d 4단)는 *일반 시니어 개발자의 실시간 day 단위가 아니라* **AI 페어 가속 환산 단위**로 사용한다.

| effort 값 | 환산 실시간 | 적용 예 |
|---|---|---|
| 0.5d | ~30~45분 | 스캐폴딩, 모델 1개, seed 스크립트, 1 PR 머지 |
| 1d | ~1~1.5h | 서비스 모듈 1개 + 단위 테스트, 인증 화면 + store |
| 2d | ~2.5~3.5h | 라우트 5개 + 통합 테스트, 화면 4종 + 골든패스 |
| 3d | (본 프로젝트 미사용) | — |

이유: 학습 컨텍스트 + AI 페어 코드 생성 + 사용자가 RFP·게이트 A·B·C 산출을 사전 완료한 상태 → 구현 단계에서 *결정·설계 비용이 거의 0*. effort 합 ~10d ÷ ~1.6h/d ≈ 16h.

### 0.2 Sprint 시간 분배

| Sprint | 일자 | 순 작업 시간 | effort 합 | 목표 |
|---|---|---|---|---|
| Sprint 1 | 2026-05-21 (Day 1) | 8h (09:00~18:00, 점심 1h 제외) | 4.5d ≈ 7~7.5h | backend 완료 — 인증·게시글 CRUD·통합 테스트·100건 시드 |
| Sprint 2 | 2026-05-22 (Day 2) | 8h (09:00~18:00, 점심 1h 제외) | 5d ≈ 7.5~8h | 댓글 + React SPA 6 화면 + 골든패스 E2E + PR 머지 |

각 sprint 마지막 30분은 *마일스톤 점검 + 컷 후보 결정*에 할당 (15-risk §3.1).

### 0.3 P2 컷 후보 (시간 박스 초과 시)

다음 순서로 컷 (우선순위 낮은 것부터):

1. **I-05 (시드 + p95 측정)** — Sprint 1 종료 30분 전에 미시작이면 컷. R-N-01 측정은 후속 학습 과제로
2. **I-09 안의 R-F-12 ProfilePage** — Sprint 2 14:00에 게시판 화면 진행 중이면 컷. *내 글 목록* 메뉴 자체 미노출
3. **I-09 안의 댓글 수정 UI (R-F-13의 FE 측)** — Sprint 2 16:00에 댓글 작성·삭제 미완이면 컷. backend API는 유지
4. **I-09 안의 골든패스 7→5단계 압축** — Sprint 2 17:00에 골든패스 진입 못하면 5단계로 (가입→로그인→글 작성→댓글 작성→글 삭제)
5. **모바일 반응형 검증** — 처음부터 best-effort. 별 cut decision 없음

위 컷은 *기능 제거*이고, 14-wbs §4 추적성 매트릭스의 R-/F-ID 매핑은 그대로 유지 (이슈에 "본 사이클 미완, 후속 과제" 라벨 추가).

### 0.4 의존성

모든 이슈가 *순차 + 일부 병렬*. 의존성 그래프는 §3 참조. 1인 작업이라 *실제* 병렬은 불가, 다만 영역 분리(I-06 backend ↔ I-07 frontend)로 컨텍스트 스위칭 부담 분산.

## 1. 스프린트 일람

| Sprint | 기간 | 목표(Outcome) | 주요 R-ID/F-ID | 이슈 수 |
|---|---|---|---|---|
| Sprint 1 | 2026-05-21 (Day 1, ~8h) | backend FastAPI 인증·게시글 CRUD 완료. 통합 테스트 green. SQLite + 100건 시드 + p95 측정 가능 | F-01, F-02 (R-F-01~R-F-08, R-F-12, R-N-01, R-N-03, R-N-04, R-N-05, R-N-06) | 5 |
| Sprint 2 | 2026-05-22 (Day 2, ~8h) | 댓글 backend + React SPA 6 화면 + 골든패스 E2E + 회귀 + PR 머지 | F-03, F-04 (R-F-09~R-F-11, R-F-13, R-N-02, R-N-05) | 5 |

## 2. 스프린트 상세

### Sprint 1 — backend 완성 (2026-05-21)

**Outcome**: backend FastAPI 앱 부팅 + 모든 API 라우트 통합 테스트 green + 게시글 100건 시드 + R-N-01 p95 < 200ms 측정 완료.

##### Issue: I-01 backend 스캐폴딩 + DB + 환경설정

- **유형**: chore
- **영역**: backend
- **우선순위**: P0
- **Estimated Effort**: 0.5d
- **Acceptance Criteria**: Given fresh checkout When `(cd backend && uv sync && uv run alembic upgrade head && uv run uvicorn realworld.main:app --reload)` 실행 Then 서버가 8000번 포트에 부팅되고 `GET /docs`에서 Swagger UI 표시
- **Contract**:
  - **Contract Before**: 빈 `backend/` 디렉토리. 의존성·구조 없음
  - **Contract After**: `backend/realworld/` 패키지 + `pyproject.toml` + `alembic/` + `.env.example` + FastAPI 앱 인스턴스 1개. 빈 라우트(`GET /api/health` 200) 1개 동작
- **DoD Checklist**:
  - [ ] `uv sync` 성공 + `uv.lock` 생성
  - [ ] `alembic init alembic` + 빈 init revision 생성
  - [ ] `realworld/main.py`에 FastAPI 앱 + health check 라우트
  - [ ] `realworld/config.py`에 pydantic-settings Settings 클래스
  - [ ] `realworld/db.py`에 AsyncEngine + AsyncSession factory
  - [ ] `backend/.env.example` 작성 (DATABASE_URL, JWT_SECRET 등)
  - [ ] LOCAL.md §3.1 명령 실제 실행 가능 확인
  - [ ] pre-commit 훅 설치 (ruff, black)

##### Issue: I-02 User 모델 + 마이그레이션 + UserRepo

- **유형**: feature
- **영역**: backend
- **우선순위**: P0
- **Estimated Effort**: 0.5d
- **Acceptance Criteria**: Given Alembic upgrade 실행 후 When DB users 테이블 조회 Then `id, username UNIQUE, email UNIQUE, password_hash, created_at` 컬럼 존재 + UserRepo.find_by_email / find_by_username / create 단위 테스트 PASS
- **Contract**:
  - **Contract Before**: I-01 완료. users 테이블 없음. UserRepo 없음
  - **Contract After**: SQLAlchemy `User` 모델 + Alembic revision `users` + `repositories/user.py` 3 메서드 + 단위 테스트 3건
- **DoD Checklist**:
  - [ ] `models/user.py` declarative 클래스
  - [ ] `alembic revision --autogenerate -m "users"` + 마이그레이션 파일 commit
  - [ ] `repositories/user.py` (find_by_email, find_by_username, create)
  - [ ] `tests/unit/test_user_repo.py` 3 케이스
  - [ ] `alembic upgrade head` 실행 후 DB 스키마 확인

##### Issue: I-03 AuthService + bcrypt + JWT util + Auth Middleware

- **유형**: feature
- **영역**: backend
- **우선순위**: P0
- **Estimated Effort**: 1d
- **Acceptance Criteria**: Given AuthService.register(dto) When 신규 사용자로 호출 Then User 반환 + DB password_hash가 `$2b$`로 시작 (bcrypt). Given require_auth dependency + 유효 JWT When 진입 Then current_user 주입 / Given 만료 JWT Then 401 한글 메시지
- **Contract**:
  - **Contract Before**: I-02 완료. AuthService·JWT util·require_auth 없음
  - **Contract After**: `services/auth.py` (register/authenticate/get_current_user) + `utils/security.py` (bcrypt) + `utils/jwt.py` (python-jose) + `deps/auth.py` (require_auth, require_author) + 단위 테스트 8건
- **DoD Checklist**:
  - [ ] `utils/security.py` hash_password / verify_password
  - [ ] `utils/jwt.py` encode / decode (HS256)
  - [ ] `services/auth.py` 3 메서드
  - [ ] `deps/auth.py` require_auth (FastAPI Depends)
  - [ ] `errors.py` 도메인 예외 클래스 (DuplicateEmail/Username, InvalidCredentials, InvalidToken, ExpiredToken, Forbidden, NotFound)
  - [ ] 단위 테스트 — `test_auth_service.py` (register 3 / authenticate 2 / get_current_user 3)
  - [ ] R-N-03·R-N-04 단위 검증 (bcrypt 마커 + JWT secret 누락 시 부팅 실패)

##### Issue: I-04 users router + articles router + 통합 테스트

- **유형**: feature
- **영역**: backend
- **우선순위**: P0
- **Estimated Effort**: 2d
- **Acceptance Criteria**: Given backend 부팅 When `POST /api/users`, `POST /api/users/login`, `GET /api/user`, `GET /api/articles` 5종 + `POST/PUT/DELETE /api/articles/{slug}` Then 09-api-spec 명세대로 동작. 통합 테스트 14건+ PASS + 작성자/타인 권한 거부 케이스 포함
- **Contract**:
  - **Contract Before**: I-03 완료. users router·articles router 없음. Article 모델 없음
  - **Contract After**: `models/article.py` + Alembic revision + `repositories/article.py` + `services/article.py` (5 메서드 + slug util) + `routers/users.py`, `routers/articles.py` + Pydantic 스키마 + 통합 테스트
- **DoD Checklist**:
  - [ ] `models/article.py` + `models/tag.py` (declarative + 인덱스 + UNIQUE slug)
  - [ ] `alembic revision --autogenerate -m "articles_tags"`
  - [ ] `utils/slug.py` (kebab-case + 숫자 suffix)
  - [ ] `repositories/article.py` (selectinload으로 N+1 회피)
  - [ ] `services/article.py` (list/get_by_slug/create/update/delete + 작성자 검증)
  - [ ] `schemas/user.py` + `schemas/article.py` (Pydantic — RealWorld spec 래핑 형식)
  - [ ] `routers/users.py` (3 라우트) + `routers/articles.py` (5 라우트)
  - [ ] `errors.py`에 exception_handlers 등록 — 422 한글 에러 매핑
  - [ ] 단위 테스트 — `test_article_service.py` (list/get/create/update/delete/slug 충돌 — 8건+)
  - [ ] 통합 테스트 — `test_users_routes.py` (3 라우트 × happy/failure) + `test_articles_routes.py` (5 라우트 × happy/failure)
  - [ ] R-F-12 author 필터 (`?author=X`) 통합 테스트 1건

##### Issue: I-05 seed 스크립트 + R-N-01 p95 통합 테스트

- **유형**: test
- **영역**: backend
- **우선순위**: P1
- **Estimated Effort**: 0.5d
- **Acceptance Criteria**: Given `(cd backend && uv run python -m scripts.seed_articles)` 실행 Then DB에 게시글 100건 + 사용자 10명 생성. Given `pytest tests/integration/test_performance.py` 실행 Then GET /api/articles?limit=20 100회 호출 p95 < 200ms 측정 PASS
- **Contract**:
  - **Contract Before**: I-04 완료. seed 스크립트·성능 테스트 없음
  - **Contract After**: `scripts/seed_articles.py` (100건 시드) + `tests/integration/test_performance.py` (p95 측정)
- **DoD Checklist**:
  - [ ] `scripts/seed_articles.py` — User 10명 + Article 100건 + Tag 5종 생성
  - [ ] 멱등 — 재실행 시 truncate 후 재시드
  - [ ] `tests/integration/test_performance.py::test_articles_list_p95`
  - [ ] 측정값 stdout 출력 (PR description 첨부 가능하게)
  - [ ] P2 컷 후보 표시 — 시간 부족 시 본 이슈 Sprint 2로 미루기 가능

### Sprint 2 — 댓글 + frontend SPA + 골든패스 (2026-05-22)

**Outcome**: 댓글 backend + React SPA 6 화면 + 골든패스 E2E 7단계 PASS + PR squash merge.

##### Issue: I-06 Comment 모델·서비스·라우터 + 통합 테스트

- **유형**: feature
- **영역**: backend
- **우선순위**: P0
- **Estimated Effort**: 1d
- **Acceptance Criteria**: Given backend 부팅 When `POST/GET/PUT/DELETE /api/articles/{slug}/comments` 4종 호출 Then 09-api-spec 동작. Given 작성자 본인 글 DELETE Then 204 + 관련 댓글 모두 CASCADE 삭제 (DB 직접 조회로 검증)
- **Contract**:
  - **Contract Before**: I-04 완료. Comment 모델·서비스·라우터 없음
  - **Contract After**: `models/comment.py` (FK ondelete=CASCADE) + Alembic revision + `repositories/comment.py` + `services/comment.py` (4 메서드) + `routers/comments.py` + `schemas/comment.py` + 단위·통합 테스트
- **DoD Checklist**:
  - [ ] `models/comment.py` — `article_id FK ondelete=CASCADE`
  - [ ] `alembic revision --autogenerate -m "comments"`
  - [ ] `repositories/comment.py`
  - [ ] `services/comment.py` (create/list_by_article/update/delete + 작성자 검증)
  - [ ] `schemas/comment.py`
  - [ ] `routers/comments.py` (4 라우트, R-F-13 PUT 비표준 신설 포함)
  - [ ] 단위 테스트 — `test_comment_service.py` (4 메서드 × happy/failure, 8건+)
  - [ ] 통합 테스트 — `test_comments_routes.py` (4 라우트) + `test_articles_routes.py::test_delete_cascades_comments` CASCADE 검증

##### Issue: I-07 frontend SPA 스캐폴딩 + 라우터 + Tailwind

- **유형**: chore
- **영역**: frontend
- **우선순위**: P0
- **Estimated Effort**: 0.5d
- **Acceptance Criteria**: Given fresh checkout When `(cd frontend && pnpm install --frozen-lockfile && pnpm dev)` 실행 Then Vite dev server가 5173 포트에 부팅 + 빈 SPA 6 라우트(`/`, `/article/:slug`, `/editor`, `/login`, `/register`, `/profile/:username`)가 placeholder로 동작 + Tailwind 클래스 1개 이상 적용 확인
- **Contract**:
  - **Contract Before**: 빈 `frontend/` 디렉토리
  - **Contract After**: Vite + React + TS + Tailwind + react-router-dom + zustand 설치. 6 페이지 placeholder + 공통 Header
- **DoD Checklist**:
  - [ ] `pnpm create vite frontend --template react-ts` 또는 수동 구성
  - [ ] `pnpm-lock.yaml` commit
  - [ ] `tailwind.config.js` + `postcss.config.js` + `index.css` 3 directive
  - [ ] `main.tsx`에서 `import './index.css'`
  - [ ] `App.tsx`에 react-router-dom 라우트 6개 placeholder
  - [ ] `components/Header.tsx` (로고 + 메뉴, 로그인 상태 미적용 placeholder)
  - [ ] `api/client.ts` fetch 래퍼 (Authorization 헤더 첨부)
  - [ ] `store/auth.ts` zustand store placeholder
  - [ ] `vite.config.ts` proxy 설정 `/api → http://localhost:8000`
  - [ ] `frontend/.env.example` (`VITE_API_BASE_URL=/api`)
  - [ ] 8000 backend + 5173 frontend 동시 부팅 후 브라우저에서 6 라우트 진입 가능 확인

##### Issue: I-08 인증 화면 (S-04 Login + S-05 Register) + AuthStore 동작

- **유형**: feature
- **영역**: frontend
- **우선순위**: P0
- **Estimated Effort**: 1d
- **Acceptance Criteria**: Given `/register` 진입 When 정상 폼 제출 Then 201 + JWT가 localStorage 저장 + 헤더가 로그인 상태로 전환 + `/` 이동. Given 중복 email Then 422 한글 에러 인라인 표시. Given `/login` 정상 자격증명 Then 200 + JWT 저장 + 헤더 전환
- **Contract**:
  - **Contract Before**: I-07 완료. S-04·S-05는 placeholder
  - **Contract After**: `pages/LoginPage.tsx` + `pages/RegisterPage.tsx` 폼 동작. `store/auth.ts` 완전 구현 (login/logout/loadFromStorage). `Header.tsx`가 store 구독해 로그인 상태 반영
- **DoD Checklist**:
  - [ ] `pages/LoginPage.tsx` — 폼 + 검증 + 422 에러 인라인 표시
  - [ ] `pages/RegisterPage.tsx` — username·email·password 3 필드
  - [ ] `store/auth.ts` — user·token state + actions (login/logout/loadFromStorage on mount)
  - [ ] `api/client.ts` — Authorization 헤더 자동 첨부 + 401 시 logout + redirect
  - [ ] `Header.tsx` — 로그인 시 [Home/Editor/Profile/Logout], 비로그인 시 [Login/Register]
  - [ ] 한글 에러 메시지 노출 — 폼 필드별
  - [ ] 모바일 Chrome에서 깨짐 없이 렌더링 (수동 확인)

##### Issue: I-09 게시판 화면 (S-01 Home + S-02 Article + S-03 Editor) + 댓글 UI + 골든패스 E2E

- **유형**: feature
- **영역**: frontend
- **우선순위**: P0
- **Estimated Effort**: 2d
- **Acceptance Criteria**: Given `/` 진입 When 100건 시드 상태 Then 최신순 카드 목록 + 페이지네이션 표시. Given 카드 클릭 → S-02 진입 Then 본문 + 댓글 + (로그인 시) 댓글 폼 표시. Given 작성자 본인 → [수정][삭제] 노출. Given 골든패스 7단계(가입→로그인→글 작성→댓글 작성→댓글 수정→글 수정→글 삭제) When gstack `/qa` 실행 Then 모든 단계 PASS + 스크린샷 7장 저장
- **Contract**:
  - **Contract Before**: I-08 완료. S-01·S-02·S-03·S-06은 placeholder. 댓글 UI 없음
  - **Contract After**: `pages/HomePage.tsx`, `pages/ArticlePage.tsx`, `pages/EditorPage.tsx`, `pages/ProfilePage.tsx`, `components/ArticleCard.tsx`, `components/CommentItem.tsx`, `components/Modal.tsx` (삭제 확인). gstack `/qa` 골든패스 통과 + 스크린샷
- **DoD Checklist**:
  - [ ] `pages/HomePage.tsx` — 게시글 카드 목록 + 페이지네이션 + loading/empty/error 상태
  - [ ] `pages/ArticlePage.tsx` — 본문 + 댓글 영역 + 작성자만 [수정][삭제] 노출
  - [ ] `pages/EditorPage.tsx` — 새 글(`/editor`) + 수정(`/editor/:slug`) 같은 컴포넌트, 제출 시 POST/PUT
  - [ ] `pages/ProfilePage.tsx` — 본인/타인 글 목록 (R-F-12, P2 컷 후보)
  - [ ] `components/ArticleCard.tsx`, `CommentItem.tsx` (수정/삭제 아이콘), `Modal.tsx` (삭제 확인)
  - [ ] 댓글 인라인 편집 폼 — `CommentItem.tsx` 내 state로 토글
  - [ ] 골든패스 7단계 gstack `/qa` 실행 + 스크린샷 `docs/features/realworld-py/screenshots/` 저장
  - [ ] FCP 측정 (R-N-02) — gstack Performance 트레이스 1회, < 1500ms 확인
  - [ ] XSS payload 1회 시도 (R-N-05) — `<script>alert(1)</script>` 본문 작성 후 상세에서 alert 미발화 확인

##### Issue: I-10 보안 점검 + 회귀 + README + docs-update + PR 머지

- **유형**: chore
- **영역**: docs
- **우선순위**: P0
- **Estimated Effort**: 0.5d
- **Acceptance Criteria**: Given Sprint 1·2 commit history When `/cso` 보안 점검 실행 Then 시크릿 평문 0건 확인. Given fresh checkout (`git worktree`) When LOCAL.md §3.1 명령 실행 Then 부팅 ≤ 5분 충족 확인. Given main으로 squash merge PR When 머지 Then CI green + AI 게이트 6축 모두 PASS
- **Contract**:
  - **Contract Before**: Sprint 1·2의 commit들 + I-09까지 모두 완료
  - **Contract After**: README.md 작성 + CHANGELOG.md 1회 갱신 + `/cso` 보고서 PR description 첨부 + main에 squash merge된 PR 1건
- **DoD Checklist**:
  - [ ] `/cso` 1회 실행 — secret 평문·취약 라이브러리·CORS=`*` 등 점검
  - [ ] git grep으로 `JWT_SECRET=eyJ...` 류 0건 확인
  - [ ] `git worktree add ../realworld-py-fresh main` + LOCAL.md §3.1 명령 그대로 실행 → 부팅 ≤ 5분 확인
  - [ ] README.md — 프로젝트 개요 + LOCAL.md 링크 + 기술 스택 1단락
  - [ ] CHANGELOG.md — v0.1.0 first release 노트
  - [ ] `/retro` 1회 실행 — `docs/planning/retro/2026-05-22-cycle.md` 생성
  - [ ] PR description에 AI 게이트 6축 체크리스트 + 골든패스 스크린샷 7장 + `/cso` 보고서 인용
  - [ ] main 머지 (squash and merge)
  - [ ] 본 이슈로 사이클 종료

## 3. 의존성 그래프

```
Sprint 1:
  I-01 ─→ I-02 ─→ I-03 ─→ I-04 ─→ I-05
                                      │
                                      ▼
Sprint 2:                          (Sprint 1 종료 마일스톤)
  I-06 (backend Comment) ──┐
  I-07 (frontend 스캐폴딩) ─┤
                            ├─→ I-08 (auth UI) ─→ I-09 (게시판 + 골든패스) ─→ I-10 (회귀·PR)
                            │
  I-06과 I-07은 병렬 가능 (다른 영역)
```

DAG 순환 없음. 일부 병렬:
- I-06 (backend Comment)과 I-07 (frontend 스캐폴딩)은 *영역이 다르므로* 같은 시간대 작업 가능. 1인 작업이므로 실제로는 순차지만 *blocker 부재*.
- I-04 통합 테스트가 green 안 되면 I-05·I-06 등 모두 블록 — Sprint 1 마일스톤이 critical path.

## 4. 추적성 매트릭스

| R-ID | F-ID | Sprint | Issue Slug |
|---|---|---|---|
| R-F-01 (회원가입) | F-01 | Sprint 1 | I-03 (AuthService.register), I-04 (POST /api/users) |
| R-F-02 (로그인) | F-01 | Sprint 1 | I-03 (AuthService.authenticate), I-04 (POST /api/users/login), I-08 (Login UI) |
| R-F-03 (현재 사용자) | F-01 | Sprint 1 | I-03 (require_auth), I-04 (GET /api/user) |
| R-F-04 (게시글 목록) | F-02 | Sprint 1 | I-04 (GET /api/articles), I-09 (HomePage) |
| R-F-05 (게시글 상세) | F-02 | Sprint 1 | I-04 (GET /api/articles/{slug}), I-09 (ArticlePage) |
| R-F-06 (게시글 작성) | F-02 | Sprint 1 | I-04 (POST /api/articles + slug util), I-09 (EditorPage 새 글) |
| R-F-07 (게시글 수정) | F-02 | Sprint 1 | I-04 (PUT /api/articles/{slug}), I-09 (EditorPage 수정) |
| R-F-08 (hard delete) | F-02 | Sprint 1 | I-04 (DELETE), I-06 (CASCADE 검증), I-09 (삭제 모달) |
| R-F-09 (댓글 작성) | F-03 | Sprint 2 | I-06 (POST /api/articles/{slug}/comments), I-09 (댓글 폼) |
| R-F-10 (댓글 목록) | F-03 | Sprint 2 | I-06 (GET ...comments), I-09 (댓글 목록 렌더링) |
| R-F-11 (댓글 삭제) | F-03 | Sprint 2 | I-06 (DELETE ...comments/{id}), I-09 (댓글 삭제 아이콘) |
| R-F-12 (내 글 목록) | F-02 | Sprint 1 | I-04 (`?author=` 필터), I-09 (ProfilePage, P2 컷 후보) |
| R-F-13 (댓글 수정) | F-03 | Sprint 2 | I-06 (PUT ...comments/{id} 비표준), I-09 (댓글 인라인 편집) |
| R-N-01 (API p95) | (모두) | Sprint 1 | I-04 (selectinload), I-05 (시드 + p95 측정) |
| R-N-02 (FCP) | F-04 | Sprint 2 | I-09 (gstack Performance 트레이스) |
| R-N-03 (bcrypt) | F-01 | Sprint 1 | I-03 (utils/security + 단위 테스트 마커 검증) |
| R-N-04 (시크릿) | (모두) | Sprint 1 | I-01 (Settings + .env.example), I-03 (JWT_SECRET) |
| R-N-05 (XSS/SQLi) | F-02·F-03·F-04 | Sprint 2 | I-09 (XSS payload 1회 시도), I-10 (`/cso` 점검) |
| R-N-06 (커버리지) | (모두) | Sprint 2 | I-10 (pytest --cov 확인, --cov-fail-under=80) |
| (전체) | F-01 | — | I-03·I-04·I-08 합 |
| (전체) | F-02 | — | I-04·I-09 합 |
| (전체) | F-03 | — | I-06·I-09 합 |
| (전체) | F-04 | — | I-07·I-08·I-09 합 |

> R-ID 19종 × F-ID 4종 모두 1개 이상 이슈에 매핑됨. *누락 0건* 확인.

## 5. 리스크 매핑

| 15-risk Risk-ID | 영향 받는 Sprint/Issue | 대응 이슈 |
|---|---|---|
| RISK-01 (일정) | Sprint 1·2 전반 | I-05·I-09 P2 컷 후보 명시. Sprint 1 종료 시점 마일스톤 |
| RISK-02 (보안) | I-02·I-03·I-04·I-10 | I-03 단위 테스트(bcrypt 마커 + JWT 검증) + I-10 `/cso` |
| RISK-03 (SQLAlchemy async) | I-01·I-03·I-04·I-06 | I-01 진입 직전 30분 사전 학습. conftest.py 1곳 fixture 집중 |
| RISK-04 (F-04 회귀 안전망) | I-09 | 골든패스 7단계 스크린샷 강제 + Sprint 2 마지막 `/qa` 재실행 |
| RISK-05 (산출물 매몰) | Sprint 1·2 전반 | 게이트 C 이후 산출 추가 안 함 — PR description + change-contract만 |
| RISK-06 (gstack 가용성) | I-09 | Sprint 1 종료 시점에 `/qa` dry-run 1회로 환경 사전 점검 |
| RISK-07 (성능 미달) | I-05·I-09 | I-05에서 측정값 stdout 출력 + I-09 FCP 트레이스 |
| RISK-08 (부팅 자산 동기) | I-10 | I-10 fresh checkout 시뮬레이션(`git worktree`) |

## 6. 일정

**총 16h** (2일 × 8h, 점심 1h 제외 순 작업 시간). 0.5d effort = ~30~45분, 1d = ~1~1.5h, 2d = ~2.5~3.5h (§0.1 환산).

### Day 1 (2026-05-21, Sprint 1, 8h)

| 시간대 | 시간 | Issue | 누적 |
|---|---|---|---|
| 09:00~09:45 | 0.75h | I-01 backend 스캐폴딩 (effort 0.5d) | 0.75h |
| 09:45~10:15 | 0.5h | I-02 User 모델 + Repo (effort 0.5d) | 1.25h |
| 10:15~11:45 | 1.5h | I-03 AuthService + JWT + Middleware (effort 1d) | 2.75h |
| 11:45~12:00 | 0.25h | I-04 users router 시작 (effort 2d 전반부) | 3h |
| 12:00~13:00 | — | 점심 (작업 시간 외) | — |
| 13:00~15:30 | 2.5h | I-04 articles router + 통합 테스트 (effort 2d 후반부) | 5.5h |
| 15:30~16:30 | 1h | I-04 통합 테스트 디버깅 + 권한 거부 케이스 보강 | 6.5h |
| 16:30~17:15 | 0.75h | I-05 seed + p95 측정 (effort 0.5d, **P2 컷 후보**) | 7.25h |
| 17:15~17:45 | 0.5h | gstack `/qa` dry-run (RISK-06 사전 점검) | 7.75h |
| 17:45~18:00 | 0.25h | Sprint 1 마일스톤 점검 + Day 2 컷 결정 | 8h |
| **마일스톤** | — | backend 5 라우트 통합 green + `/qa` dry-run 도구 환경 확인 | — |

### Day 2 (2026-05-22, Sprint 2, 8h)

| 시간대 | 시간 | Issue | 누적 |
|---|---|---|---|
| 09:00~10:30 | 1.5h | I-06 Comment 모듈 + 라우터 + CASCADE 통합 (effort 1d) | 1.5h |
| 10:30~11:15 | 0.75h | I-07 frontend 스캐폴딩 + Tailwind (effort 0.5d) | 2.25h |
| 11:15~12:00 | 0.75h | I-08 LoginPage + AuthStore 시작 (effort 1d 전반부) | 3h |
| 12:00~13:00 | — | 점심 | — |
| 13:00~13:45 | 0.75h | I-08 RegisterPage + Header 로그인 상태 + 422 에러 인라인 | 3.75h |
| 13:45~14:45 | 1h | I-09 HomePage + ArticleCard (S-01) (effort 2d 1/3) | 4.75h |
| 14:45~15:45 | 1h | I-09 ArticlePage + CommentItem + 댓글 작성/삭제 UI (S-02) | 5.75h |
| 15:45~16:30 | 0.75h | I-09 EditorPage (S-03 새 글 + 수정) + 삭제 모달 | 6.5h |
| 16:30~17:00 | 0.5h | I-09 댓글 수정 인라인 편집 (R-F-13의 FE, **P2 컷 후보**) | 7h |
| 17:00~17:30 | 0.5h | I-09 골든패스 7단계 gstack `/qa` + 스크린샷 + FCP·XSS 측정 | 7.5h |
| 17:30~17:50 | ~0.33h | I-10 `/cso` 보안 점검 + fresh checkout(`git worktree`) 부팅 확인 | 7.83h |
| 17:50~18:00 | ~0.17h | I-10 README + CHANGELOG + PR squash merge + `/retro` | 8h |
| **마감** | — | main 머지 + `/retro` → 사이클 완주 | — |

### 6.1 시간 박스 컷 결정 시점

| 결정 시점 | 조건 | 컷 대상 |
|---|---|---|
| Day 1, 16:30 | I-04 통합 테스트 미완 | I-05 즉시 컷 → I-04 마무리에 시간 재배분 |
| Day 1, 18:00 | backend 5 라우트 통합 미통과 | Day 2 시작 30분에 backend 마무리 → Sprint 2의 I-09 일부 컷 (R-F-12 ProfilePage 우선) |
| Day 2, 14:00 | I-08 인증 화면 미완 | I-09의 R-F-12 ProfilePage 컷 — 헤더 메뉴 자체 미노출 |
| Day 2, 16:00 | I-09 게시판 + 댓글 작성·삭제 UI 미완 | 댓글 수정 UI(R-F-13의 FE) 컷 — backend API는 유지 |
| Day 2, 17:00 | 골든패스 7단계 진입 못함 | 5단계 압축 (가입→로그인→글 작성→댓글 작성→글 삭제) |
| Day 2, 17:50 | I-10 미완 | PR description 간소화 + `/retro`는 다음날 또는 회고 메모로 |

각 시점의 컷 결정은 *15분 timer*로 명확히 — "16:30에 I-04 통합 green이 안 되면 즉시 I-05 컷". 결정 지연이 *가장 큰* 시간 낭비.

## 7. sprint-bootstrap 입력

```yaml
project:
  name: realworld-py
  repo: <GitHub 저장소 URL — flow-bootstrap 시 결정>
  default_branch: main
  labels_namespace:
    - status:todo
    - status:in-progress
    - status:in-review
    - status:blocked
    - priority:high
    - priority:medium
    - priority:low
    - type:feature
    - type:bug
    - type:chore
    - type:docs
    - type:test
    - area:backend
    - area:frontend
    - area:docs
    - area:infra

sprints:
  - name: "Sprint 1"
    milestone: "Sprint 1"
    description: "backend FastAPI 인증·게시글 CRUD 완료. 통합 테스트 green. 100건 시드 + p95 측정."
    due: "2026-05-21"
    due_date: "2026-05-21"
    issues:
      - title: "chore(backend): I-01 스캐폴딩 + DB + 환경설정"
        labels: [type:chore, area:backend, priority:P0]
        body: |
          ## 매핑
          R-ID: (전체 기반)
          F-ID: -

          ## 유형 / 영역 / 우선순위
          - 유형: chore
          - 영역: backend
          - 우선순위: P0
          - Estimated Effort: 0.5d

          ## Acceptance Criteria
          Given fresh checkout When `(cd backend && uv sync && uv run alembic upgrade head && uv run uvicorn realworld.main:app --reload)` 실행 Then 서버가 8000번 포트에 부팅되고 `GET /docs`에서 Swagger UI 표시

          ## Contract
          - 변경 전: 빈 `backend/` 디렉토리. 의존성·구조 없음
          - 변경 후: `backend/realworld/` 패키지 + `pyproject.toml` + `alembic/` + `.env.example` + FastAPI 앱 인스턴스 1개 + health check 1개

          ## DoD Checklist
          - [ ] `uv sync` 성공 + `uv.lock` 생성
          - [ ] `alembic init alembic` + 빈 init revision
          - [ ] `realworld/main.py` FastAPI 앱
          - [ ] `realworld/config.py` pydantic-settings Settings
          - [ ] `realworld/db.py` AsyncEngine + Session factory
          - [ ] `backend/.env.example` 작성
          - [ ] LOCAL.md §3.1 명령 실제 실행 가능
          - [ ] pre-commit 훅 설치

          ## 테스트 시나리오
          - 단위: N/A (스캐폴딩)
          - 통합: 부팅 + health check 1건
          - E2E: N/A

          ## 의존성
          - Blocked-by: (없음 — 첫 이슈)
          - Blocks: I-02

          ---
          상세: {{WBS_URL}} (14-wbs §2 Sprint 1)

      - title: "feat(backend): I-02 User 모델 + 마이그레이션 + UserRepo"
        labels: [type:feature, area:backend, priority:P0]
        body: |
          ## 매핑
          R-ID: R-F-01, R-N-03, R-N-04
          F-ID: F-01

          ## 유형 / 영역 / 우선순위
          - 유형: feature
          - 영역: backend
          - 우선순위: P0
          - Estimated Effort: 0.5d

          ## Acceptance Criteria
          Given Alembic upgrade 실행 후 When DB users 테이블 조회 Then `id, username UNIQUE, email UNIQUE, password_hash, created_at` 컬럼 존재 + UserRepo 3 메서드 단위 테스트 PASS

          ## Contract
          - 변경 전: I-01 완료. users 테이블 없음
          - 변경 후: SQLAlchemy `User` 모델 + Alembic revision + `repositories/user.py` 3 메서드 + 단위 테스트 3건

          ## DoD Checklist
          - [ ] `models/user.py` declarative
          - [ ] `alembic revision --autogenerate -m "users"` + 마이그레이션 commit
          - [ ] `repositories/user.py` (find_by_email, find_by_username, create)
          - [ ] `tests/unit/test_user_repo.py` 3 케이스
          - [ ] `alembic upgrade head` 실행 확인

          ## 테스트 시나리오
          - 단위: ✅ UserRepo 3 메서드
          - 통합: N/A (다음 이슈에서)
          - E2E: N/A

          ## 의존성
          - Blocked-by: I-01
          - Blocks: I-03

          ---
          상세: {{WBS_URL}} (14-wbs §2 Sprint 1)

      - title: "feat(backend): I-03 AuthService + bcrypt + JWT util + Auth Middleware"
        labels: [type:feature, area:backend, priority:P0]
        body: |
          ## 매핑
          R-ID: R-F-01, R-F-02, R-F-03, R-N-03, R-N-04
          F-ID: F-01

          ## 유형 / 영역 / 우선순위
          - 유형: feature
          - 영역: backend
          - 우선순위: P0
          - Estimated Effort: 1d

          ## Acceptance Criteria
          Given AuthService.register(dto) When 신규 사용자로 호출 Then User 반환 + DB password_hash가 `$2b$`로 시작. Given require_auth + 유효 JWT Then current_user 주입 / 만료 JWT Then 401 한글 메시지

          ## Contract
          - 변경 전: I-02 완료. AuthService·JWT util·require_auth 없음
          - 변경 후: `services/auth.py` (register/authenticate/get_current_user) + `utils/security.py` + `utils/jwt.py` + `deps/auth.py` + `errors.py` + 단위 테스트 8건

          ## DoD Checklist
          - [ ] `utils/security.py` (passlib bcrypt)
          - [ ] `utils/jwt.py` (python-jose HS256)
          - [ ] `services/auth.py` 3 메서드
          - [ ] `deps/auth.py` require_auth + require_author
          - [ ] `errors.py` 도메인 예외 클래스
          - [ ] 단위 테스트 8건 (register 3 / authenticate 2 / get_current_user 3)
          - [ ] R-N-03·R-N-04 검증 케이스 포함

          ## 테스트 시나리오
          - 단위: ✅ AuthService + utils (8건+)
          - 통합: N/A (다음 이슈)
          - E2E: N/A

          ## 의존성
          - Blocked-by: I-02
          - Blocks: I-04

          ---
          상세: {{WBS_URL}} (14-wbs §2 Sprint 1)

      - title: "feat(backend): I-04 users router + articles router + 통합 테스트"
        labels: [type:feature, area:backend, priority:P0]
        body: |
          ## 매핑
          R-ID: R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-12, R-N-01, R-N-05
          F-ID: F-01, F-02

          ## 유형 / 영역 / 우선순위
          - 유형: feature
          - 영역: backend
          - 우선순위: P0
          - Estimated Effort: 2d

          ## Acceptance Criteria
          Given backend 부팅 When users 3 라우트 + articles 5 라우트 호출 Then 09-api-spec 명세대로 동작 + 통합 테스트 14건+ PASS + 권한 거부(403)·미존재(404)·검증(422) 케이스 포함

          ## Contract
          - 변경 전: I-03 완료. Article 모델·router 없음
          - 변경 후: `models/article.py` + Alembic + `repositories/article.py` + `services/article.py` (5 메서드 + slug) + `routers/users.py`·`routers/articles.py` + Pydantic 스키마 + 통합 테스트

          ## DoD Checklist
          - [ ] `models/article.py` + `models/tag.py`
          - [ ] `alembic revision --autogenerate -m "articles_tags"`
          - [ ] `utils/slug.py` (kebab-case + 숫자 suffix)
          - [ ] `repositories/article.py` (selectinload)
          - [ ] `services/article.py` (5 메서드)
          - [ ] `schemas/user.py` + `schemas/article.py`
          - [ ] `routers/users.py` (3) + `routers/articles.py` (5)
          - [ ] `errors.py` exception_handlers (422 한글)
          - [ ] 단위 테스트 8건+ + 통합 테스트 14건+
          - [ ] R-F-12 `?author=` 필터 통합 1건

          ## 테스트 시나리오
          - 단위: ✅ ArticleService + slug util
          - 통합: ✅ users 3 + articles 5 라우트
          - E2E: N/A (Sprint 2)

          ## 의존성
          - Blocked-by: I-03
          - Blocks: I-05, I-06

          ---
          상세: {{WBS_URL}} (14-wbs §2 Sprint 1)

      - title: "test(backend): I-05 seed 스크립트 + R-N-01 p95 통합 테스트"
        labels: [type:test, area:backend, priority:P1]
        body: |
          ## 매핑
          R-ID: R-N-01
          F-ID: F-02

          ## 유형 / 영역 / 우선순위
          - 유형: test
          - 영역: backend
          - 우선순위: P1
          - Estimated Effort: 0.5d

          ## Acceptance Criteria
          Given `(cd backend && uv run python -m scripts.seed_articles)` 실행 Then DB에 게시글 100건 + 사용자 10명 + 태그 5종 생성. Given `pytest tests/integration/test_performance.py` Then GET /api/articles?limit=20 100회 p95 < 200ms PASS

          ## Contract
          - 변경 전: I-04 완료. seed·성능 테스트 없음
          - 변경 후: `scripts/seed_articles.py` + `tests/integration/test_performance.py`

          ## DoD Checklist
          - [ ] `scripts/seed_articles.py` (User 10 + Article 100 + Tag 5)
          - [ ] 멱등 — 재실행 시 truncate 후 재시드
          - [ ] `tests/integration/test_performance.py::test_articles_list_p95`
          - [ ] 측정값 stdout 출력
          - [ ] P2 컷 후보 표시 — 시간 부족 시 Sprint 2로 미루기 가능

          ## 테스트 시나리오
          - 단위: N/A
          - 통합: ✅ p95 측정
          - E2E: N/A

          ## 의존성
          - Blocked-by: I-04
          - Blocks: (없음 — Sprint 1 마지막)

          ---
          상세: {{WBS_URL}} (14-wbs §2 Sprint 1)

  - name: "Sprint 2"
    milestone: "Sprint 2"
    description: "댓글 backend + React SPA 6 화면 + 골든패스 E2E + 회귀 + PR 머지."
    due: "2026-05-22"
    due_date: "2026-05-22"
    issues:
      - title: "feat(backend): I-06 Comment 모델·서비스·라우터 + CASCADE 검증"
        labels: [type:feature, area:backend, priority:P0]
        body: |
          ## 매핑
          R-ID: R-F-09, R-F-10, R-F-11, R-F-13, R-F-08
          F-ID: F-03

          ## 유형 / 영역 / 우선순위
          - 유형: feature
          - 영역: backend
          - 우선순위: P0
          - Estimated Effort: 1d

          ## Acceptance Criteria
          Given backend 부팅 When comments 4 라우트(POST/GET/PUT/DELETE) 호출 Then 09-api-spec 동작. Given 작성자 본인 글 DELETE Then 204 + 관련 댓글 CASCADE 삭제 (DB 직접 조회 검증)

          ## Contract
          - 변경 전: I-04 완료. Comment 모델·라우터 없음
          - 변경 후: `models/comment.py` (FK CASCADE) + Alembic + `repositories/comment.py` + `services/comment.py` (4 메서드) + `routers/comments.py` + `schemas/comment.py` + 단위·통합 테스트

          ## DoD Checklist
          - [ ] `models/comment.py` — article_id FK ondelete=CASCADE
          - [ ] `alembic revision --autogenerate -m "comments"`
          - [ ] `repositories/comment.py`
          - [ ] `services/comment.py` 4 메서드
          - [ ] `schemas/comment.py`
          - [ ] `routers/comments.py` 4 라우트 (R-F-13 PUT 비표준 포함)
          - [ ] 단위 테스트 8건+
          - [ ] `test_articles_routes.py::test_delete_cascades_comments` CASCADE 검증

          ## 테스트 시나리오
          - 단위: ✅ CommentService 4 메서드
          - 통합: ✅ 4 라우트 + CASCADE 검증
          - E2E: N/A (I-09에서)

          ## 의존성
          - Blocked-by: I-04
          - Blocks: I-09

          ---
          상세: {{WBS_URL}} (14-wbs §2 Sprint 2)

      - title: "chore(frontend): I-07 SPA 스캐폴딩 + 라우터 + Tailwind"
        labels: [type:chore, area:frontend, priority:P0]
        body: |
          ## 매핑
          R-ID: -
          F-ID: F-04

          ## 유형 / 영역 / 우선순위
          - 유형: chore
          - 영역: frontend
          - 우선순위: P0
          - Estimated Effort: 0.5d

          ## Acceptance Criteria
          Given fresh checkout When `(cd frontend && pnpm install --frozen-lockfile && pnpm dev)` Then 5173 포트 부팅 + 6 라우트 placeholder 동작 + Tailwind 클래스 1개 이상 적용 확인

          ## Contract
          - 변경 전: 빈 `frontend/`
          - 변경 후: Vite + React + TS + Tailwind + react-router-dom + zustand. 6 페이지 placeholder + Header

          ## DoD Checklist
          - [ ] `pnpm create vite frontend --template react-ts` 또는 수동
          - [ ] `pnpm-lock.yaml` commit
          - [ ] tailwind.config.js + postcss.config.js + index.css 3 directive
          - [ ] main.tsx에서 stylesheet import
          - [ ] App.tsx 6 라우트 placeholder
          - [ ] Header.tsx 공통
          - [ ] api/client.ts fetch 래퍼
          - [ ] store/auth.ts zustand placeholder
          - [ ] vite.config.ts proxy `/api → :8000`
          - [ ] frontend/.env.example

          ## 테스트 시나리오
          - 단위: N/A
          - 통합: N/A
          - E2E: N/A (I-09 골든패스에 포함)

          ## 의존성
          - Blocked-by: (없음 — backend 부팅과 독립)
          - Blocks: I-08

          ---
          상세: {{WBS_URL}} (14-wbs §2 Sprint 2)

      - title: "feat(frontend): I-08 인증 화면 (S-04 Login + S-05 Register) + AuthStore"
        labels: [type:feature, area:frontend, priority:P0]
        body: |
          ## 매핑
          R-ID: R-F-01, R-F-02, R-F-03
          F-ID: F-01, F-04

          ## 유형 / 영역 / 우선순위
          - 유형: feature
          - 영역: frontend
          - 우선순위: P0
          - Estimated Effort: 1d

          ## Acceptance Criteria
          Given `/register` 진입 When 정상 폼 제출 Then 201 + JWT localStorage 저장 + 헤더 전환 + `/` 이동. Given 중복 email Then 422 한글 에러 인라인. Given `/login` 정상 자격증명 Then 200 + JWT 저장

          ## Contract
          - 변경 전: I-07 완료. S-04·S-05 placeholder, AuthStore 미구현
          - 변경 후: LoginPage·RegisterPage 폼 동작 + AuthStore 완전 구현 + Header 로그인 상태 반영

          ## DoD Checklist
          - [ ] pages/LoginPage.tsx
          - [ ] pages/RegisterPage.tsx
          - [ ] store/auth.ts (login/logout/loadFromStorage)
          - [ ] api/client.ts Authorization 헤더 자동 첨부 + 401 → logout
          - [ ] Header.tsx 로그인 상태 반영
          - [ ] 한글 에러 메시지 인라인
          - [ ] 모바일 Chrome 깨짐 없이 렌더링

          ## 테스트 시나리오
          - 단위: N/A (F-04 UI 단위/통합 N/A 결정)
          - 통합: N/A
          - E2E: ✅ I-09 골든패스에 포함

          ## 의존성
          - Blocked-by: I-07, I-04 (backend 인증 라우트)
          - Blocks: I-09

          ---
          상세: {{WBS_URL}} (14-wbs §2 Sprint 2)

      - title: "feat(frontend): I-09 게시판 화면 (Home/Article/Editor/Profile) + 댓글 UI + 골든패스 E2E"
        labels: [type:feature, area:frontend, priority:P0]
        body: |
          ## 매핑
          R-ID: R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-09, R-F-10, R-F-11, R-F-12, R-F-13, R-N-02, R-N-05
          F-ID: F-02, F-03, F-04

          ## 유형 / 영역 / 우선순위
          - 유형: feature
          - 영역: frontend
          - 우선순위: P0
          - Estimated Effort: 2d

          ## Acceptance Criteria
          Given `/` 진입 + 100건 시드 Then 최신순 카드 목록 + 페이지네이션. Given 카드 클릭 → S-02 Then 본문 + 댓글 + (로그인 시) 댓글 폼. Given 작성자 본인 Then [수정][삭제] 노출. Given 골든패스 7단계(가입→로그인→글 작성→댓글 작성→댓글 수정→글 수정→글 삭제) When gstack `/qa` 실행 Then 모든 단계 PASS + 스크린샷 7장 저장

          ## Contract
          - 변경 전: I-08 완료. S-01·S-02·S-03·S-06 placeholder. 댓글 UI 없음
          - 변경 후: 6 화면 동작 + 댓글 인라인 편집 + 삭제 모달 + gstack `/qa` 골든패스 통과 + 스크린샷

          ## DoD Checklist
          - [ ] pages/HomePage.tsx (목록 + 페이지네이션 + 상태 4종)
          - [ ] pages/ArticlePage.tsx (본문 + 댓글 + 작성자 액션)
          - [ ] pages/EditorPage.tsx (새 글 + 수정 같은 컴포넌트)
          - [ ] pages/ProfilePage.tsx (R-F-12, P2 컷 후보)
          - [ ] components/ArticleCard.tsx, CommentItem.tsx, Modal.tsx
          - [ ] 댓글 인라인 편집 + 삭제 확인 모달
          - [ ] gstack `/qa` 골든패스 7단계 + 스크린샷 `docs/features/realworld-py/screenshots/`
          - [ ] FCP 측정 (R-N-02) < 1500ms 확인
          - [ ] XSS payload 1회 시도 (R-N-05) — alert 미발화 확인

          ## 테스트 시나리오
          - 단위: N/A (F-04 결정)
          - 통합: N/A
          - E2E: ✅ 골든패스 7단계 + FCP + XSS

          ## 의존성
          - Blocked-by: I-06, I-08
          - Blocks: I-10

          ---
          상세: {{WBS_URL}} (14-wbs §2 Sprint 2)

      - title: "chore(docs): I-10 보안 점검 + 회귀 + README + docs-update + PR 머지"
        labels: [type:chore, area:docs, priority:P0]
        body: |
          ## 매핑
          R-ID: R-N-05, R-N-06
          F-ID: (전체)

          ## 유형 / 영역 / 우선순위
          - 유형: chore
          - 영역: docs
          - 우선순위: P0
          - Estimated Effort: 0.5d

          ## Acceptance Criteria
          Given Sprint 1·2 commit history When `/cso` 보안 점검 Then 시크릿 평문 0건 확인. Given fresh checkout (`git worktree`) When LOCAL.md §3.1 명령 Then 부팅 ≤ 5분 충족. Given main으로 squash merge PR When 머지 Then CI green + AI 게이트 6축 모두 PASS

          ## Contract
          - 변경 전: Sprint 1·2 commit들 + I-09까지 모두 완료
          - 변경 후: README.md 작성 + CHANGELOG.md 갱신 + `/cso` 보고서 PR description 첨부 + main squash merge 1건

          ## DoD Checklist
          - [ ] `/cso` 보안 점검 1회 (secret 평문·취약 라이브러리·CORS=`*`)
          - [ ] git grep으로 secret 평문 0건 확인
          - [ ] `git worktree add ../realworld-py-fresh main` + LOCAL.md §3.1 부팅 ≤ 5분
          - [ ] README.md 작성
          - [ ] CHANGELOG.md v0.1.0 release notes
          - [ ] `/retro` 실행 → `docs/planning/retro/2026-05-22-cycle.md`
          - [ ] PR description AI 게이트 6축 체크리스트 + 골든패스 스크린샷 7장 + `/cso` 보고서
          - [ ] main 머지 (squash and merge)
          - [ ] pytest --cov 적용 범위 ≥ 80% (R-N-06)

          ## 테스트 시나리오
          - 단위: N/A
          - 통합: ✅ pytest 전체 회귀
          - E2E: ✅ 골든패스 1회 재실행

          ## 의존성
          - Blocked-by: I-09
          - Blocks: (없음 — 사이클 종료)

          ---
          상세: {{WBS_URL}} (14-wbs §2 Sprint 2)
```

## 8. Open Questions

1. **GitHub 저장소 URL** — `flow-bootstrap` Phase 4/4 시점에 사용자가 결정 (개인 repo / 회사 organization 중). 본 §7 YAML의 `project.repo`는 placeholder.
2. **GitHub Projects v2 보드 사용 여부** — Issues + Milestones은 sprint-bootstrap이 자동 등록. Projects v2 view는 옵션. 단일 sprint × 2일 컨텍스트라 미사용 가능.
3. **이슈 라벨 — `priority:*`와 우선순위 P0/P1/P2 동기** — 본 §7은 라벨에 `priority:high/medium/low` 채택. PRD `priority:high → P0+P1`, `medium → P2`, `low → P3` 매핑 가정. sprint-bootstrap 시 일관 적용.
4. **`due_date`가 GitHub Milestone에 그대로 반영되는지** — sprint-bootstrap 동작 검증 필요. flow-bootstrap에서 dry-run으로 확인.
