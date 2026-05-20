---
doc_type: srs
version: v0.2 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: B
related:
  R-ID: []
  F-ID: []
  supersedes: null
---

# realworld-py — SRS

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.2 | 2026-05-20 | woosung.ahn@bespinglobal.com | 게이트 B 결정 반영 — R-F-06 slug 숫자 suffix 명확화 / R-F-08 hard delete 명시 / R-F-13 댓글 수정 신규 / R-N-06 적용 범위 명시 / §6 Open Q 결정 |
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-init` Phase 1/4, RFP §3·§4 흡수, R-F-01~R-F-12 + R-N-01~R-N-06) |

## 1. 범위 / 가정

- **범위**: RFP §3에 명시된 MVP — Auth(F-01), Article(F-02), Comment(F-03), 최소 UI(F-04). RealWorld spec 중 follow·favorite·tag feed는 Out of Scope.
- **가정 1**: 백엔드 언어는 Python (RFP §NFR-01 강제). 프레임워크는 게이트 C 결정.
- **가정 2**: 단일 환경 운영 — dev 1 profile만 (RFP §NFR-06). dev/stg/prod 3 profile은 N/A.
- **가정 3**: 로컬 부팅만 필수 — 클라우드 배포 Out of Scope. CI는 GitHub Actions pytest 1개로 충분.
- **가정 4**: 페이지네이션은 limit/offset (RealWorld spec 일치). cursor 기반 Out of Scope.
- **가정 5**: 동시 사용자 부하 학습 컨텍스트 — 1~5명 수준. 부하·확장성 시나리오는 본 SRS 범위 밖.
- **가정 6**: 외부 시스템 의존 0건 (이메일·SMS·결제·푸시 등 모두 Out of Scope).
- **가정 7 (v0.2 결정)**: 백엔드 프레임워크는 **FastAPI**, 프론트엔드는 **SPA (React + Vite)**. 게이트 B 사전 결정 — `/flow-design`에서 ADR로 정식화. DB·스타일링 솔루션은 게이트 C 결정.
- **가정 8 (v0.2 결정)**: 게시글 삭제 = **hard delete** (DB row 영구 제거 + 댓글 FK CASCADE). slug 충돌 = **숫자 suffix** (`my-post-2`, `my-post-3` …). 댓글 수정 = MVP 포함(R-F-13).

## 2. 기능 요구사항

### R-F-01: 회원가입

- **우선순위**: P0
- **설명**: 비회원이 username·email·password 세 필드로 새 계정을 만들 수 있다. 비밀번호는 bcrypt 해시로 저장. 가입 즉시 JWT 발급.
- **관련 UC**: UC-01
- **관련 NFR**: NFR-04 (bcrypt, JWT secret 환경변수), NFR-03 (한글 에러 메시지)
- **Acceptance** (Given/When/Then):
  - Given 미등록 이메일·username·8자 이상 비밀번호 When POST /api/users Then 201 + 사용자 객체(JWT 포함) 응답
  - Given 이미 등록된 이메일 When POST /api/users Then 422 + "이미 사용 중인 이메일입니다"
- **테스트 시나리오**:
  - 단위: ✅ (UserService.register — bcrypt 해시 적용, 중복 검사)
  - 통합: ✅ (POST /api/users 라우트 → DB 사용자 row 생성 확인)
  - E2E: ✅ (회원가입 폼 → 가입 완료 → 홈 이동)
- **Happy path**: 정상 가입 — 신규 이메일·username 입력 → 201 + JWT 반환 → DB에 bcrypt 해시 저장 확인
- **Failure path**:
  - 실패-1: 중복 이메일 → 422 (에러 메시지 한글)
  - 실패-2: password 8자 미만 → 422 (한글 에러)
  - 실패-3: 잘못된 이메일 형식 → 400

### R-F-02: 로그인

- **우선순위**: P0
- **설명**: 가입 사용자가 email·password로 로그인하면 서버는 bcrypt 검증 후 JWT를 발급한다.
- **관련 UC**: UC-02
- **관련 NFR**: NFR-04 (bcrypt 비교, 토큰 secret 환경변수)
- **Acceptance**:
  - Given 가입된 사용자의 정확한 비밀번호 When POST /api/users/login Then 200 + JWT 응답
  - Given 잘못된 비밀번호 When POST /api/users/login Then 422 + "이메일 또는 비밀번호가 올바르지 않습니다"
- **테스트 시나리오**:
  - 단위: ✅ (AuthService.authenticate — bcrypt 비교, JWT 발급)
  - 통합: ✅ (POST /api/users/login → DB 조회 + JWT 검증)
  - E2E: ✅ (로그인 폼 → 성공 시 홈 이동, JWT 저장)
- **Happy path**: 정상 자격증명 → 200 + JWT 반환, 클라이언트 로컬 스토리지에 토큰 저장
- **Failure path**:
  - 실패-1: 비밀번호 불일치 → 422 (에러 메시지가 어느 쪽이 틀렸는지 누설하지 않음 — 정보 유출 방지)
  - 실패-2: 미등록 이메일 → 422 (동일 메시지)
  - 실패-3: 5회 연속 실패 → (Out of Scope, 학습 범위 외) 추후 ADR 검토 가능

### R-F-03: 현재 사용자 조회

- **우선순위**: P0
- **설명**: 클라이언트가 보유한 JWT가 유효한지 확인하고, 현재 로그인된 사용자 정보를 반환한다.
- **관련 UC**: UC-02 (사후 토큰 검증), UC-10 부분
- **관련 NFR**: NFR-04 (JWT 검증)
- **Acceptance**:
  - Given 유효한 JWT When GET /api/user Then 200 + 사용자 객체
  - Given 만료된/위조된 JWT When GET /api/user Then 401
- **테스트 시나리오**:
  - 단위: ✅ (JWTService.verify — 서명·만료 검증)
  - 통합: ✅ (GET /api/user — 토큰 헤더 파싱 + DB 조회)
  - E2E: N/A (라우트 가드 동작은 UC-05~UC-09 흐름에 포함)
- **Happy path**: 정상 JWT → 200 + 본인 정보
- **Failure path**:
  - 실패-1: JWT 없음 → 401
  - 실패-2: JWT 만료 → 401 + 클라이언트에서 로그인 페이지로 이동

### R-F-04: 게시글 목록 조회

- **우선순위**: P0
- **설명**: limit/offset 파라미터로 게시글 목록을 페이지네이션 조회한다. 기본 limit=20.
- **관련 UC**: UC-03
- **관련 NFR**: NFR-02 (p95 < 200ms @ 100건)
- **Acceptance**:
  - Given 게시글 N건 존재 When GET /api/articles?limit=20&offset=0 Then 200 + 최신순 20건 + 총 개수
  - Given limit=10&offset=20 When GET /api/articles Then 21~30번째 글 반환
- **테스트 시나리오**:
  - 단위: ✅ (ArticleService.list — 정렬·페이지네이션 로직)
  - 통합: ✅ (GET /api/articles — DB 쿼리, eager loading N+1 방어 검증)
  - E2E: ✅ (홈 진입 시 목록 카드 표시 + 페이지 이동)
- **Happy path**: 정상 호출 → 최신순 20건 + 총 개수 반환
- **Failure path**:
  - 실패-1: limit > 100 → 400 (학습 범위에서 안전상 상한 부과)
  - 실패-2: offset 음수 → 400

### R-F-05: 게시글 상세 조회

- **우선순위**: P0
- **설명**: slug로 단일 게시글 본문과 메타데이터를 조회한다.
- **관련 UC**: UC-04
- **관련 NFR**: NFR-04 (XSS — 응답은 ORM/템플릿이 escape)
- **Acceptance**:
  - Given 존재하는 slug When GET /api/articles/{slug} Then 200 + 게시글 객체
  - Given 미존재 slug When GET /api/articles/{slug} Then 404
- **테스트 시나리오**:
  - 단위: ✅ (ArticleService.get_by_slug)
  - 통합: ✅ (GET /api/articles/{slug} — DB 단일 조회)
  - E2E: ✅ (글 카드 클릭 → 상세 페이지 본문·댓글 렌더)
- **Happy path**: 정상 slug → 200 + 본문 + 메타 + 작성자 정보
- **Failure path**:
  - 실패-1: 미존재 slug → 404 (404 페이지 렌더)
  - 실패-2: slug 형식 위반 (특수문자 등) → 400 또는 404 (게이트 C 결정)

### R-F-06: 게시글 작성

- **우선순위**: P0
- **설명**: 로그인 사용자가 제목·설명·본문·태그(선택)로 새 글을 작성한다. 서버가 slug 자동 생성 (title → kebab-case). 충돌 시 **숫자 suffix 부여** (예: `my-post`가 있으면 `my-post-2`, 다시 있으면 `my-post-3`). v0.2 결정.
- **관련 UC**: UC-05
- **관련 NFR**: NFR-04 (JWT 인증), NFR-03 (한글 에러)
- **Acceptance**:
  - Given 로그인 + 필수 필드 채움 When POST /api/articles Then 201 + 새 글 + slug
  - Given JWT 누락/만료 When POST /api/articles Then 401
- **테스트 시나리오**:
  - 단위: ✅ (ArticleService.create — slug 생성 + 충돌 회피 + DB 저장)
  - 통합: ✅ (POST /api/articles — 인증 미들웨어 + DB row + 응답)
  - E2E: ✅ (글쓰기 폼 → 제출 → 새 글 상세로 이동)
- **Happy path**: 정상 제출 → 201 + slug 응답 → /article/{slug}로 이동
- **Failure path**:
  - 실패-1: JWT 만료 → 401 + 로그인 페이지로 이동
  - 실패-2: 제목·본문 누락 → 422 + 한글 에러
  - 실패-3: 동일 제목 작성 → slug 자동 suffix(예: `my-post-2`) 부여로 회피(에러 아님)

### R-F-07: 게시글 수정 (작성자 한정)

- **우선순위**: P1
- **설명**: 본인이 작성한 글의 제목·설명·본문·태그를 수정한다.
- **관련 UC**: UC-06
- **관련 NFR**: NFR-04 (작성자 검증)
- **Acceptance**:
  - Given 작성자 본인의 JWT When PUT /api/articles/{slug} Then 200 + 갱신된 글
  - Given 타인의 JWT When PUT /api/articles/{slug} Then 403
- **테스트 시나리오**:
  - 단위: ✅ (ArticleService.update — 작성자 검증 + 부분 갱신)
  - 통합: ✅ (PUT /api/articles/{slug} — 권한 거부 케이스 포함)
  - E2E: ✅ (수정 폼 → 갱신 → 본문 변경 확인)
- **Happy path**: 작성자 본인 → 200 + 갱신된 글 응답
- **Failure path**:
  - 실패-1: 타인 시도 → 403 (예외 메시지 "권한이 없습니다")
  - 실패-2: 비로그인 → 401
  - 실패-3: 미존재 slug → 404

### R-F-08: 게시글 삭제 (작성자 한정)

- **우선순위**: P1
- **설명**: 본인이 작성한 글을 **hard delete** 한다. DB row를 영구 제거하며, 댓글은 FK CASCADE로 함께 삭제 (v0.2 결정). 복구 기능은 Out of Scope.
- **관련 UC**: UC-07
- **관련 NFR**: NFR-04 (작성자 검증)
- **Acceptance**:
  - Given 작성자 본인의 JWT + 댓글 N개 달린 글 When DELETE /api/articles/{slug} Then 204 + DB에 article row 없음 + 관련 comment row 모두 삭제
  - Given 타인 JWT When DELETE /api/articles/{slug} Then 403
- **테스트 시나리오**:
  - 단위: ✅ (ArticleService.delete — 작성자 검증)
  - 통합: ✅ (DELETE /api/articles/{slug} — 권한 + article row 제거 + 댓글 CASCADE 삭제 검증)
  - E2E: ✅ (삭제 버튼 → 확인 모달 → 홈으로 리다이렉트)
- **Happy path**: 작성자 본인 → 204, 홈에서 더 이상 해당 글 보이지 않음, DB 직접 조회 시 article·comment 모두 부재
- **Failure path**:
  - 실패-1: 타인 시도 → 403
  - 실패-2: 이미 삭제된 글 재삭제 → 404 (예외 메시지 "이미 삭제된 글입니다")
  - 실패-3: 비로그인 → 401

### R-F-09: 댓글 작성

- **우선순위**: P1
- **설명**: 로그인 사용자가 게시글에 댓글을 작성한다. body 텍스트만.
- **관련 UC**: UC-08
- **관련 NFR**: NFR-04 (JWT 인증, XSS escape)
- **Acceptance**:
  - Given 로그인 + body 채움 When POST /api/articles/{slug}/comments Then 201 + 댓글 객체
  - Given JWT 누락 When POST /api/articles/{slug}/comments Then 401
- **테스트 시나리오**:
  - 단위: ✅ (CommentService.create — body 검증 + DB 저장)
  - 통합: ✅ (POST /api/articles/{slug}/comments — 인증 + DB row)
  - E2E: ✅ (상세 페이지 댓글 폼 → 작성 → 목록 상단에 추가)
- **Happy path**: 정상 작성 → 201, 화면 댓글 목록 갱신
- **Failure path**:
  - 실패-1: 비로그인 → 401
  - 실패-2: body 빈 문자열 → 422 + 한글 에러
  - 실패-3: 미존재 글 slug → 404

### R-F-10: 댓글 목록 조회

- **우선순위**: P1
- **설명**: 게시글에 달린 댓글을 최신순으로 반환한다.
- **관련 UC**: UC-04 (상세 페이지에서 함께 호출)
- **관련 NFR**: NFR-02 (N+1 쿼리 금지)
- **Acceptance**:
  - Given 존재하는 글 slug When GET /api/articles/{slug}/comments Then 200 + 댓글 배열 (최신순)
  - Given 미존재 글 slug When GET /api/articles/{slug}/comments Then 404
- **테스트 시나리오**:
  - 단위: ✅ (CommentService.list_by_article — 정렬 + eager loading)
  - 통합: ✅ (GET /api/articles/{slug}/comments — N+1 쿼리 미발생 검증)
  - E2E: ✅ (상세 페이지 진입 시 댓글 영역 렌더링)
- **Happy path**: 정상 호출 → 200 + 댓글 배열
- **Failure path**:
  - 실패-1: 미존재 글 → 404
  - 실패-2: 댓글 0건 → 200 + 빈 배열 (에러 아님)

### R-F-11: 댓글 삭제 (작성자 한정)

- **우선순위**: P1
- **설명**: 본인이 작성한 댓글을 삭제한다.
- **관련 UC**: UC-09
- **관련 NFR**: NFR-04 (작성자 검증)
- **Acceptance**:
  - Given 작성자 본인 JWT When DELETE /api/articles/{slug}/comments/{id} Then 204
  - Given 타인 JWT When DELETE /api/articles/{slug}/comments/{id} Then 403
- **테스트 시나리오**:
  - 단위: ✅ (CommentService.delete — 작성자 검증)
  - 통합: ✅ (DELETE 라우트 — 권한 거부 케이스 포함)
  - E2E: ✅ (댓글 옆 삭제 아이콘 → 확인 → 목록에서 제거)
- **Happy path**: 작성자 본인 → 204
- **Failure path**:
  - 실패-1: 타인 시도 → 403
  - 실패-2: 이미 삭제된 댓글 → 404 + 에러 메시지

### R-F-12: 내 글 목록 (프로필)

- **우선순위**: P2
- **설명**: 로그인 사용자가 본인이 작성한 글 목록을 본다. RealWorld spec의 `?author={username}` 필터 활용.
- **관련 UC**: UC-11
- **관련 NFR**: NFR-02 (페이지네이션)
- **Acceptance**:
  - Given 로그인 상태 When GET /api/articles?author={본인 username} Then 200 + 본인 글 배열
  - Given 비로그인 When 프로필 메뉴 클릭 Then 헤더에 메뉴 미노출 (서버 응답 단계 이전)
- **테스트 시나리오**:
  - 단위: ✅ (ArticleService.list with author filter)
  - 통합: ✅ (GET /api/articles?author=X — 필터 동작)
  - E2E: ✅ (프로필 메뉴 → 내 글만 표시)
- **Happy path**: 정상 호출 → 본인 글 배열
- **Failure path**:
  - 실패-1: 잘못된 username 파라미터 → 200 + 빈 배열 (에러 아님)
  - 실패-2: 비로그인 → 헤더에 메뉴 자체 미노출(클라이언트 가드)

### R-F-13: 댓글 수정 (작성자 한정)

- **우선순위**: P1
- **설명**: 본인이 작성한 댓글의 body를 수정한다. v0.2 결정으로 MVP 포함. RealWorld spec엔 PUT comment 엔드포인트가 표준은 아니지만 본 프로젝트에서 `PUT /api/articles/{slug}/comments/{id}` 형식으로 신설한다.
- **관련 UC**: UC-12
- **관련 NFR**: NFR-04 (작성자 검증), NFR-05 (XSS escape)
- **Acceptance**:
  - Given 작성자 본인 JWT + 비어있지 않은 body When PUT /api/articles/{slug}/comments/{id} Then 200 + 갱신된 댓글 객체
  - Given 타인 JWT When PUT /api/articles/{slug}/comments/{id} Then 403
- **테스트 시나리오**:
  - 단위: ✅ (CommentService.update — 작성자 검증 + body 갱신)
  - 통합: ✅ (PUT /api/articles/{slug}/comments/{id} — 권한 거부 케이스 포함)
  - E2E: ✅ (상세 페이지에서 본인 댓글 [수정] → 인라인 편집 → 저장 → 댓글 본문 갱신)
- **Happy path**: 작성자 본인 → 200 + 갱신된 댓글 객체. 화면 즉시 갱신.
- **Failure path**:
  - 실패-1: 타인 수정 시도 → 403 (예외 메시지 "권한이 없습니다")
  - 실패-2: 비로그인 → 401
  - 실패-3: body 빈 문자열 → 422 + 한글 에러
  - 실패-4: 이미 삭제된 댓글 → 404 + "이미 삭제된 댓글입니다"

## 3. 비기능 요구사항

### R-N-01: 퍼포먼스 — API 응답시간

- **우선순위**: P1
- **설명**: 게시글 100건 시드 상태에서 게시글 목록 API p95가 200ms 미만이어야 한다.
- **관련 UC**: UC-03
- **Acceptance**:
  - Given 100건 시드 When GET /api/articles?limit=20을 100회 호출 Then p95 < 200ms (로컬 측정)
- **테스트 시나리오**:
  - 단위: N/A (성능은 통합 레벨에서 측정)
  - 통합: ✅ (pytest + httpx로 100회 호출 후 p95 측정)
  - E2E: N/A
- **Happy path**: 정상 측정 → p95 < 200ms
- **Failure path**:
  - 실패-1: N+1 쿼리 발생 → 측정값 200ms 초과 → 게이트 C에서 eager loading 추가

### R-N-02: 퍼포먼스 — FCP

- **우선순위**: P2
- **설명**: 게시글 목록 페이지의 First Contentful Paint가 1.5초 미만이어야 한다 (로컬 dev 서버 기준).
- **관련 UC**: UC-03
- **Acceptance**:
  - Given dev 서버 + 100건 시드 When 게시글 목록 페이지를 Chrome DevTools Performance로 측정 Then FCP < 1.5s
- **테스트 시나리오**:
  - 단위: N/A
  - 통합: N/A
  - E2E: ✅ (gstack `/qa` Performance 트레이스로 1회 측정)
- **Happy path**: 정상 측정 → FCP < 1.5s
- **Failure path**:
  - 실패-1: SPA 채택 시 초기 번들이 커지면 미달 가능 → 게이트 C에서 코드 스플리팅·SSR 검토

### R-N-03: 보안 — 비밀번호 저장

- **우선순위**: P0
- **설명**: 사용자 비밀번호는 bcrypt(또는 동급 단방향 해시)로만 저장한다. 평문/역가역 해시(MD5/SHA256 단독) 금지.
- **관련 UC**: UC-01, UC-02
- **Acceptance**:
  - Given 회원가입 직후 When DB의 user.password 컬럼 조회 Then `$2b$` 등 bcrypt 마커로 시작
- **테스트 시나리오**:
  - 단위: ✅ (UserService.register — 저장 형식 검증)
  - 통합: ✅ (DB 직접 조회로 형식 확인)
  - E2E: N/A
- **Happy path**: 정상 저장 → bcrypt 해시 형식
- **Failure path**:
  - 실패-1: 평문 저장 발견 → /cso 보안 점검 단계에서 BLOCK, 즉시 패치 (회복 불가능한 보안 결함이므로 마이그레이션 + 강제 재로그인)

### R-N-04: 보안 — 시크릿 관리

- **우선순위**: P0
- **설명**: JWT secret, DB 자격증명 등 모든 시크릿은 환경변수로만 로드한다. 코드·저장소·로그·PR 본문에 평문 노출 금지 (CLAUDE.md 보안 절대 규칙).
- **관련 UC**: 전체
- **Acceptance**:
  - Given 서버 부팅 When `JWT_SECRET` 환경변수 미설정 Then 서버가 명시적 에러 메시지로 종료
  - Given git diff/log When grep으로 secret-like 패턴 검색 Then 0건
- **테스트 시나리오**:
  - 단위: ✅ (config loader — 환경변수 미설정 시 명시적 예외 발생)
  - 통합: ✅ (서버 부팅 시 시크릿 없음 → 명시적 종료)
  - E2E: N/A
- **Happy path**: 정상 부팅 → 시크릿 환경변수 로드 성공
- **Failure path**:
  - 실패-1: 시크릿 환경변수 누락 → 부팅 단계에서 명확한 한글 에러 (예: "JWT_SECRET 환경변수가 설정되지 않았습니다")
  - 실패-2: 시크릿 .env에 작성 → .env는 .gitignore되어 커밋되지 않음 + PreToolUse 훅이 보안 파일 Write 차단

### R-N-05: 보안 — XSS / SQL Injection

- **우선순위**: P0
- **설명**: 사용자 입력은 ORM 파라미터 바인딩으로 처리 (raw SQL 금지). 출력은 템플릿 escape 기본값 신뢰. 서버 렌더링 채택 시 CSRF 토큰 적용.
- **관련 UC**: UC-04, UC-05, UC-08
- **Acceptance**:
  - Given 본문 `<script>alert(1)</script>` 작성 When 상세 페이지 렌더링 Then alert 발화 없음, 텍스트로 escape 표시
  - Given `'; DROP TABLE articles; --` 같은 입력 When 검색/조회 Then DB 무결성 영향 없음
- **테스트 시나리오**:
  - 단위: ✅ (입력 sanitize 또는 template escape 검증)
  - 통합: ✅ (실제 요청 → 응답에서 escape 확인)
  - E2E: ✅ (gstack `/qa`로 XSS 페이로드 1회 시도 → alert 안 뜸 확인)
- **Happy path**: 악성 페이로드 정상 escape → 일반 텍스트로 표시
- **Failure path**:
  - 실패-1: escape 누락 → /cso 보안 점검에서 BLOCK, 템플릿 설정 점검 후 패치

### R-N-06: 품질 — 단위 테스트 커버리지

- **우선순위**: P1
- **설명**: ADR-0015 §2.3 정책값(≥ 80%, v0.2 결정 채택)을 다음 *적용 범위*에 대해 만족한다.
  - **적용 범위**: `UserService` (회원가입·인증), `ArticleService` (목록·상세·작성·수정·삭제·slug 생성), `CommentService` (작성·목록·수정·삭제), 권한 검증 미들웨어 (`require_auth`, `require_author`).
  - **제외 범위**: 라우트 핸들러·API 스키마(Pydantic)·DB 마이그레이션·UI 컴포넌트·설정 로더 — 통합/E2E 테스트로 커버.
- **관련 UC**: 전체
- **관련 NFR**: NFR-05
- **Acceptance**:
  - Given pytest --cov 실행 + 적용 범위 모듈만 측정 When 측정 종료 Then 커버리지 ≥ 80%
  - Given 적용 범위 외 모듈 When 측정 Then 강제 없음 (보고는 함)
- **테스트 시나리오**:
  - 단위: ✅ (각 서비스 모듈마다 단위 테스트 작성, pytest-cov로 정량 측정)
  - 통합: N/A (커버리지 정의상 단위 레벨)
  - E2E: N/A
- **Happy path**: pytest --cov 결과 적용 범위 ≥ 80% → AI 게이트 통과
- **Failure path**:
  - 실패-1: 일부 모듈 미달 → 누락 케이스에 단위 테스트 추가
  - 실패-2: 적용 범위 외 모듈 미달 → 강제 안 함 (학습 부담 회피)

## 4. 인터페이스 요구사항

- **HTTP API** — RealWorld spec 준수 (`/api/users`, `/api/users/login`, `/api/user`, `/api/articles`, `/api/articles/{slug}`, `/api/articles/{slug}/comments`, `/api/articles/{slug}/comments/{id}`). 상세 스펙은 게이트 C `09-api-spec`에서 OpenAPI로 확정.
- **인증 헤더** — `Authorization: Token <JWT>` (RealWorld spec 관례). 일반적인 `Bearer <JWT>`와 다름에 유의.
- **응답 포맷** — JSON (`Content-Type: application/json`). RealWorld spec의 `{ user: {...} }` / `{ article: {...} }` 등 래핑 객체 형식 준수.
- **에러 응답** — `{ errors: { field: ["메시지"] } }` 형식 (RealWorld spec 권고). 메시지는 한글 (NFR-03).
- **CORS** — 단일 환경 운영이므로 동일 출처. SPA 채택 시에만 CORS 설정 필요 (게이트 C 결정).
- **DB 인터페이스** — ORM (SQLAlchemy 또는 Django ORM, 게이트 C 결정). raw SQL 금지 (R-N-05).
- **로그** — stdout으로 간단 로깅. 외부 로깅 시스템 연동 Out of Scope.

## 5. 도메인 모델

```
User (id, username UNIQUE, email UNIQUE, password_hash, created_at)
  ├── 1:N → Article
  └── 1:N → Comment

Article (id, slug UNIQUE, title, description, body, author_id FK→User, created_at, updated_at)
  ├── N:M ↔ Tag (taglist, MVP는 단순 join table)
  └── 1:N → Comment

Comment (id, body, article_id FK→Article, author_id FK→User, created_at)

Tag (id, name UNIQUE)  -- MVP에선 태그 입력만 허용, 태그별 피드는 Out of Scope
```

> 상세 컬럼 타입·인덱스·제약은 게이트 C `08-lld-module-spec` 데이터 모델 절에서 확정.

## 6. Open Questions

1. ~~R-N-06 적용 범위~~ — **결정 (v0.2)**: ADR-0015 정책값 ≥ 80% 채택, 적용 범위는 *UserService·ArticleService·CommentService·권한 미들웨어* 한정. R-N-06 본문에 명시.
2. ~~slug 충돌 규칙~~ — **결정 (v0.2)**: 숫자 suffix(`-2`, `-3` …) 채택. R-F-06 본문 갱신.
3. ~~게시글 삭제 soft vs hard~~ — **결정 (v0.2)**: hard delete + 댓글 FK CASCADE. R-F-08 본문 갱신.
4. **R-N-02 FCP 측정 방법** — gstack `/qa` Performance 트레이스로 가능하지만 1회 측정만 강제할지, 자동화할지. 게이트 C `13-test-design`에서 확정.
5. **R-F-12 우선순위** — P2이므로 시간 부족 시 가장 먼저 컷 후보. WBS에서 명시.
6. **R-F-13 PUT comment 엔드포인트 형식** — RealWorld spec 표준엔 없음. `PUT /api/articles/{slug}/comments/{id}` 채택 가정. 게이트 C `09-api-spec`에서 OpenAPI로 정식화.
