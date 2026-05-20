---
doc_type: prd
version: v0.2 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: B
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-09, R-F-10, R-F-11, R-F-12, R-F-13]
  F-ID: []
  supersedes: null
---

# realworld-py — PRD

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.2 | 2026-05-20 | woosung.ahn@bespinglobal.com | 게이트 B 결정 반영 — F-03 댓글 수정 MVP 포함 (R-F-13 매핑) / F-02 hard delete + slug 숫자 suffix 명시 / §1 기술 스택 사전 결정 / §7 Open Q 결정 |
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-init` Phase 1/4, RFP §3·§6 + 04-srs R-F-01~R-F-12 흡수) |

## 1. 제품 개요

realworld-py는 RealWorld(Conduit) 스펙을 베이스로 한 **Python 게시판 웹 애플리케이션**이다. 학습 목적의 1차 산출물로, 다음 4개 기능 영역을 MVP로 제공한다.

- **F-01 인증** — 회원가입·로그인·현재 사용자 조회
- **F-02 게시글** — 목록·상세·작성·수정·삭제 (hard delete)
- **F-03 댓글** — 작성·목록·수정·삭제
- **F-04 UI** — 비회원/가입 사용자가 위 기능을 브라우저에서 사용할 수 있는 최소 SPA

부가 기능(팔로우·즐겨찾기·태그 피드 등)은 Out of Scope.

### 1.1 기술 스택 (게이트 B 사전 결정, v0.2)

| 영역 | 결정 | 사유 |
|---|---|---|
| 백엔드 프레임워크 | **FastAPI** | Pydantic 검증, OpenAPI 자동 생성, SPA REST 친화 |
| 프론트엔드 | **React + Vite (SPA)** | FastAPI REST와 자연 결합. ADR-0038 스타일링 솔루션 게이트 C 확정 |
| 데이터베이스 | SQLite / PostgreSQL 중 1 (게이트 C 결정) | — |
| 인증 | JWT + bcrypt | `passlib[bcrypt]`, `pyjwt` 등. R-N-03·R-N-04 강제 |
| 테스트 | pytest + pytest-cov | 적용 범위는 04-srs §R-N-06 본문 명시 |

`/flow-design`에서 위 결정을 ADR로 정식화한다 (ADR 후보 #1·#2).

## 2. 사용자 가치

| 사용자 | 가치 |
|---|---|
| 비회원 방문자 | 로그인 없이 게시글·댓글을 읽으며 사이트를 둘러본다 |
| 가입 사용자 | 회원가입 후 자기 글·댓글을 자유롭게 작성·관리한다 |
| 학습자(본인) | agent-toolkit 풀 사이클을 1회 완주하며 14종 산출물 작성·AI 게이트 6축 통과 경험을 얻는다 |
| 멘토·리뷰어 | 사이클 산출물(01~15 + ADR + PR)을 통해 학습 진척도를 검토한다 |

## 3. 기능

### F-01: 사용자 인증 (Auth)

- **MVP Cut**: 포함 ✅
- **우선순위**: P0
- **사용자 스토리**: As a 게시판 사용자 I want to 회원가입과 로그인을 통해 자신의 글을 작성할 수 있도록 인증된 세션을 갖기 so that 작성한 글의 소유권이 보호되고 권한 분기가 가능하다.
- **R-ID 매핑**: R-F-01 (회원가입), R-F-02 (로그인), R-F-03 (현재 사용자 조회). 비기능: R-N-03 (bcrypt), R-N-04 (시크릿).
- **Acceptance**:
  - Given 미가입 사용자 When 회원가입 폼을 정상 제출 Then 201 + JWT가 반환되어 로그인 상태로 전환
  - Given 가입 사용자 When 정확한 자격증명으로 로그인 Then 200 + JWT 반환 후 헤더가 로그인 상태 UI로 전환
- **테스트 시나리오**:
  - 단위: ✅ (UserService.register / AuthService.authenticate / JWTService.verify)
  - 통합: ✅ (POST /api/users, POST /api/users/login, GET /api/user)
  - E2E: ✅ (회원가입 → 로그인 → 헤더 상태 확인)
- **Happy path**: 정상 회원가입 → 자동 로그인 → 헤더에 사용자 이름 노출
- **Failure path**:
  - 실패-1: 중복 이메일 회원가입 → 422 한글 에러 메시지
  - 실패-2: 비밀번호 불일치 로그인 → 422 (어느 쪽이 틀렸는지 누설 않음, 보안 정신)
  - 실패-3: JWT 만료 후 API 호출 → 401 + 로그인 페이지로 자동 이동

### F-02: 게시글 (Article)

- **MVP Cut**: 포함 ✅
- **우선순위**: P0
- **사용자 스토리**: As a 게시판 사용자 I want to 게시글을 목록·상세로 읽고, 가입 후엔 직접 글을 쓰고 수정·삭제 so that RealWorld spec의 핵심 CRUD 흐름을 학습한다.
- **R-ID 매핑**: R-F-04 (목록), R-F-05 (상세), R-F-06 (작성, slug 숫자 suffix), R-F-07 (수정), R-F-08 (hard delete + 댓글 CASCADE), R-F-12 (내 글 목록). 비기능: R-N-01 (퍼포먼스), R-N-02 (FCP), R-N-05 (XSS).
- **Acceptance**:
  - Given 게시글 100건 시드 When GET /api/articles?limit=20&offset=0 Then 200 + 최신순 20건 + 총 개수
  - Given 작성자 본인 JWT When PUT /api/articles/{slug} Then 200 + 갱신된 글
  - Given 작성자 본인 JWT + 댓글 N개 달린 글 When DELETE /api/articles/{slug} Then 204 + DB에 article·comment 모두 부재 (hard delete + CASCADE)
  - Given 같은 제목으로 두 번째 글 작성 When POST /api/articles Then 201 + slug에 `-2` 숫자 suffix 부여
  - Given 타인 JWT When DELETE /api/articles/{slug} Then 403
- **테스트 시나리오**:
  - 단위: ✅ (ArticleService.list / get_by_slug / create / update / delete — 작성자 검증·페이지네이션·slug 충돌 회피)
  - 통합: ✅ (각 라우트 + 권한 거부 케이스, N+1 쿼리 미발생 검증, hard delete 후 댓글 CASCADE 확인)
  - E2E: ✅ (홈 목록 → 상세 → 글쓰기 → 수정 → 삭제 골든패스)
- **Happy path**: 정상 작성·수정·삭제 흐름 성공, 목록은 최신순 페이지네이션 동작, 동명 제목은 숫자 suffix로 회피
- **Failure path**:
  - 실패-1: 타인의 글 수정·삭제 시도 → 403 한글 에러 메시지
  - 실패-2: 비로그인 상태 글쓰기 시도 → 401 + 로그인 페이지 이동
  - 실패-3: 미존재 slug 상세 → 404 페이지

### F-03: 댓글 (Comment)

- **MVP Cut**: 포함 ✅
- **우선순위**: P1
- **사용자 스토리**: As a 가입 사용자 I want to 게시글에 댓글을 달고 내 댓글을 *수정·삭제* 할 수 있도록 so that 단순 토론·반응 + 오타 정정이 가능하다.
- **R-ID 매핑**: R-F-09 (작성), R-F-10 (목록), R-F-11 (삭제), **R-F-13 (수정, v0.2 신규)**. 비기능: R-N-05 (XSS).
- **Acceptance**:
  - Given 로그인 + body 채움 When POST /api/articles/{slug}/comments Then 201 + 댓글 객체
  - Given 작성자 본인 JWT + 비어있지 않은 body When PUT /api/articles/{slug}/comments/{id} Then 200 + 갱신된 댓글
  - Given 작성자 본인 JWT When DELETE /api/articles/{slug}/comments/{id} Then 204
  - Given 존재하는 글 slug When GET /api/articles/{slug}/comments Then 200 + 최신순 댓글 배열
- **테스트 시나리오**:
  - 단위: ✅ (CommentService.create / list_by_article / update / delete — 작성자 검증)
  - 통합: ✅ (POST·GET·PUT·DELETE 라우트 + 권한 거부)
  - E2E: ✅ (상세 페이지에서 댓글 작성 → 수정 → 목록 갱신 → 삭제)
- **Happy path**: 정상 댓글 작성 → 인라인 편집으로 수정 → 본인 댓글 삭제 가능
- **Failure path**:
  - 실패-1: 타인의 댓글 수정·삭제 시도 → 403
  - 실패-2: 빈 body 댓글 (작성·수정) → 422 한글 에러
  - 실패-3: 미존재 글 slug에 댓글 → 404

### F-04: UI / 화면

- **MVP Cut**: 포함 ✅
- **우선순위**: P1
- **사용자 스토리**: As a 게시판 사용자 I want to 홈·상세·글쓰기·로그인·회원가입·프로필 화면을 React SPA로 사용 so that gstack `/qa` 골든패스가 통과한다.
- **R-ID 매핑**: F-01·F-02·F-03 모든 R-ID와 매핑됨 (R-F-13 댓글 수정 포함). 화면 자체는 UI 결정 사항으로 R-ID를 추가하지 않고 게이트 C `10-lld-screen-design`에서 LLD로 작성.
- **Acceptance**:
  - Given dev 서버 부팅 When 비회원이 홈 진입 Then 게시글 목록이 1.5초 미만에 표시 (NFR-02)
  - Given 회원가입 → 로그인 → 글쓰기 → 댓글 작성 → 댓글 수정 → 글 수정 → 글 삭제 골든패스 When gstack `/qa` 실행 Then 모든 단계 PASS + 스크린샷 저장
- **테스트 시나리오**:
  - 단위: N/A (v0.2 결정 — UI 컴포넌트 단위 테스트는 학습 범위 외. E2E 1회로 대체)
  - 통합: N/A (SPA + REST API 분리. UI 통합 테스트는 학습 범위 외)
  - E2E: ✅ (gstack `/qa` 골든패스 1회 통과 — DoD §3)
- **Happy path**: 골든패스 7단계(가입→로그인→글 작성→댓글 작성→댓글 수정→글 수정→글 삭제) 모두 PASS, 화면 캡처가 `docs/features/<slug>/screenshots/`에 저장
- **Failure path**:
  - 실패-1: 폼 유효성 누락 시 한글 에러 메시지 노출 안 됨 → /ui-design-review에서 BLOCK
  - 실패-2: 모바일 Chrome에서 레이아웃 깨짐 → 게이트 C에서 styling 솔루션 확정 후 재검증 (ADR-0038)
  - 실패-3: FCP 1.5초 초과 → 측정 결과로 게이트 C에서 코드 스플리팅 또는 React.lazy 도입 결정

## 4. MVP Cut 요약

| F-ID | MVP | 비고 |
|---|---|---|
| F-01 | ✅ 포함 | P0. 회원가입·로그인·현재 사용자 조회. 비밀번호 찾기·이메일 검증은 Out of Scope |
| F-02 | ✅ 포함 | P0. CRUD 전체. hard delete + slug 숫자 suffix (v0.2 결정). 즐겨찾기·태그 피드는 Out of Scope |
| F-03 | ✅ 포함 | P1. 작성·목록·**수정 (R-F-13, v0.2 신규)**·삭제 |
| F-04 | ✅ 포함 | P1. React SPA — 홈·상세·글쓰기·로그인·회원가입·프로필 최소 화면. 단위/통합 테스트 N/A 확정 (v0.2). 다크모드·다국어 Out of Scope |
| F-FOLLOW (가칭) | ❌ 제외 | RFP §3 Out of Scope. 시간 남으면 별도 이슈로 진행 가능 |
| F-FAVORITE (가칭) | ❌ 제외 | RFP §3 Out of Scope |
| F-TAG-FEED (가칭) | ❌ 제외 | RFP §3 Out of Scope |
| F-IMG-UPLOAD (가칭) | ❌ 제외 | RFP §3 Out of Scope |

## 5. UX 원칙 / 화면 구성 큰 그림

- **최소 6개 화면** — 홈(목록), 게시글 상세, 글쓰기/수정 폼, 로그인, 회원가입, 내 프로필
- **헤더 일관** — 로고 + 홈·글쓰기·내 프로필(로그인 시)·로그아웃·로그인/가입(비로그인 시)
- **모바일 호환** — 반응형까지는 강제 아니지만 모바일 Chrome에서 깨짐 없이 렌더링 (NFR-03)
- **에러 메시지 한글** — 모든 폼 유효성 메시지·서버 에러 메시지는 한글 (NFR-03)
- **로딩 표시** — 페이지 이동·API 호출 중 단순 스피너 또는 disabled 버튼 (깜빡임 방지)
- **상세 화면 구조** — 본문 영역 + 댓글 영역(로그인 시 댓글 폼 노출). 추가 시각 요소(공유 버튼 등)는 Out of Scope
- **스타일링 솔루션** — 게이트 C `12-scaffolding §8`에서 1개 채택 (Tailwind / CSS Modules / styled-components 중). ADR-0038 강제 — plain HTML 머지 차단

> 화면 와이어프레임·상태 다이어그램·디자인 토큰은 게이트 C `10-lld-screen-design`에서 작성.

## 6. 의존성 / 외부 시스템

- **외부 API**: 없음 (RFP §5 제약)
- **DB**: SQLite 또는 PostgreSQL 중 1개 (게이트 C 결정, ADR 후보)
- **이메일·SMS·결제·푸시**: 모두 Out of Scope
- **파일 저장소(S3 등)**: 프로필 이미지 업로드 Out of Scope → 불필요
- **인증 외부 ID(OAuth)**: Out of Scope. 자체 JWT만
- **CI/CD**: GitHub Actions 1개 워크플로 (pytest). 클라우드 배포 Out of Scope
- **로컬 의존**: Python 3.11+ (게이트 C 확정), `uv`(Astral) 권장, Docker는 선택
- **브라우저**: Chrome 데스크톱·모바일 최소. 다른 브라우저는 best-effort

## 7. Open Questions

1. ~~백엔드 프레임워크~~ — **결정 (v0.2)**: **FastAPI**. §1.1 기술 스택 표 명시. `/flow-design` ADR로 정식화.
2. ~~프론트엔드 렌더링 방식~~ — **결정 (v0.2)**: **SPA (React + Vite)**. §1.1 기술 스택 표 명시.
3. ~~F-03 댓글 수정~~ — **결정 (v0.2)**: **MVP 포함** (R-F-13 신규). F-03 본문·매핑·테스트 시나리오에 반영. UC-12 신설.
4. ~~F-04 단위 테스트 N/A~~ — **결정 (v0.2)**: N/A 확정. F-04 테스트 시나리오에 명시.
5. ~~R-N-06 커버리지 정량값~~ — **결정 (v0.2)**: ADR-0015 §2.3 정책값(≥ 80%) 채택, 적용 범위는 04-srs §R-N-06 본문 명시.
6. **잔여 결정 (게이트 C)** — 데이터베이스 (SQLite vs PostgreSQL), 스타일링 솔루션 (ADR-0038), 세부 라이브러리 조합, 테스트 fixture 도구.
