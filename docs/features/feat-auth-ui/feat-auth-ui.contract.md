---
doc_type: feature-contract
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-01, R-F-02, R-F-03]
  F-ID: [F-01, F-04]
  supersedes: null
---

# feat-auth-ui — Change Contract

> P3 (ADR-0018). §0 Referenced-IDs로 선택적 정본 진입. mode=add — I-07 placeholder를 실 동작으로 채움.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — §0 6행 + §2 Before/After 6행 + §3 Call Sites 4행 + BC neutral + Rollback 1-commit revert |

## 0. 참조 정본 ID (Referenced-IDs)

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| SRS | `docs/planning/04-srs/04-srs.md` §6.1 R-F-01 회원가입 + §6.1 R-F-02 로그인 + §6.1 R-F-03 현재 사용자 | R-F-01, R-F-02, R-F-03 |
| PRD | `docs/planning/05-prd/05-prd.md` §3 F-01 Auth + F-04 UI 모듈 | F-01, F-04 |
| LLD-Screen | `docs/planning/10-lld-screen-design/10-lld-screen-design.md` §2 S-04 Login + S-05 Register + §1.1 공통 레이아웃 Header | (none) |
| LLD-API | `docs/planning/09-lld-api-spec/09-lld-api-spec.md` §3 POST /api/users + POST /api/users/login + GET /api/user | (none) |
| Scaffolding | `docs/planning/12-scaffolding/python.md` §1 frontend 트리 (I-07 도입 상태) | (none) |
| Test Catalog | N/A — WBS I-08 DoD에 단위/통합 N/A 명시. E2E는 I-09 골든패스 | (none) |

## 1. 변경 의도

I-07 placeholder LoginPage·RegisterPage·Header를 실 동작으로 채운다. backend Issue #4 라우트(`POST /api/users[/login]` + `GET /api/user`)와 연결해 회원가입·로그인·로그아웃 + Header 로그인 상태 분기 + 로그인 유지(localStorage 복원). 422 한글 에러 인라인 표시 (R-N-05 a11y + UX).

**simple catch 패턴 채택** — api/client.ts 인터셉터 자동화 회피. 호출자(LoginPage 등)에서 `try {} catch(e: ApiError)`로 401·422 분기 (plan §5).

## 2. Before / After

| 항목 | Before (I-07) | After (I-08) |
| --- | --- | --- |
| `frontend/src/pages/LoginPage.tsx` | placeholder text + Tailwind | 실 폼 — email·password controlled inputs + `<form onSubmit>` + `apiFetch('/users/login', POST, body={user:{email, password}})` + 200 시 `useAuthStore.login(user, token)` + `useNavigate('/')` + 422 catch → `errors.body[0]` 인라인 (h1 아래 빨강 박스) |
| `frontend/src/pages/RegisterPage.tsx` | placeholder text + Tailwind | 실 폼 — username·email·password 3 controlled inputs + POST `/users` body={user:{username,email,password}} + 201 시 login + `/` 이동 + 422 catch → 한글 메시지 인라인 |
| `frontend/src/components/Header.tsx` | 4 메뉴 고정 | useAuthStore 구독: `const { user } = useAuthStore()`. logged-in (user != null): [Home / New Article / {user.username} → /profile/{username} / Logout(button)]. logged-out: [Sign in / Sign up] |
| `frontend/src/App.tsx` | mount load 없음 | `useEffect(() => useAuthStore.getState().loadFromStorage(), [])` hook 1줄 추가 |
| `frontend/src/types/api.ts` | 6 type aliases | + `ErrorBody = { errors: { body: string[] } }` + `extractErrorMessage(unknown): string` 헬퍼 함수 |
| `frontend/src/store/auth.ts` | placeholder (login/logout/loadFromStorage 메서드 이미 완비) | **무수정** — I-07 시그니처 그대로 사용 |

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| `frontend/src/pages/LoginPage·RegisterPage` → `apiFetch<UserResponse>(path, {method:'POST', body:JSON.stringify(...)})` | I-07 api/client.ts 시그니처 그대로 호출 | 무수정 — fetch 래퍼 재사용 |
| `frontend/src/components/Header` + LoginPage/RegisterPage → `useAuthStore` hook | zustand selector 패턴 사용 | I-07 store/auth.ts 시그니처 그대로 |
| backend `POST /api/users[/login]` + `GET /api/user` | 무수정 — Issue #4 라우트 그대로 | proxy 통과 (`/api/*` → :8000) |
| backend CORS 허용 origin :5173 | 무수정 (I-01 정착) | I-08 폼 호출 시 CORS preflight 통과 검증 |

## 4. Backward Compatibility

**BC neutral** — frontend src/ 파일 *내용 변경*이지만 외부 인터페이스(store/auth.ts 시그니처·api/client.ts 시그니처) 무수정. backend 영향 0.

- I-07 시점의 zustand store 시그니처 그대로 — Header·LoginPage·RegisterPage 인터페이스 호환
- I-07 `apiFetch<T>` 시그니처 그대로
- 기존 6 라우트 그대로 — 라우팅 무변경
- backend Issue #4 라우트 무수정 — pytest 77 passed 회귀 N/A
- CI: backend-ci `paths: backend/**` 한정 — frontend 변경에 미트리거

## 5. Rollback 전략

**1-commit revert로 충분** — squash merge 단일 commit.

- 코드 revert: 4개 파일(LoginPage·RegisterPage·Header·App.tsx) + 1 helper(types/api.ts ErrorBody) 자동 revert
- store/auth.ts·api/client.ts·routing 무수정 → 부수 영향 0
- 데이터 영속성: localStorage `realworld.token`·`realworld.user` 키 — revert 후 잔존하면 사용자가 브라우저 DevTools로 수동 제거 (단일 환경 운영 + 학습 컨텍스트 acceptable)

리스크 등급 Low — risk.md에서 4건 식별.

## 6. 비목표

- **Forgot password / 이메일 인증**: out of scope (RFP §5)
- **OAuth / 소셜 로그인**: out of scope
- **자동 토큰 갱신**: out of scope — backend JWT 7일 expiry로 충분
- **api/client.ts 401 인터셉터 자동화**: simple catch 패턴 채택 (plan §5). over-engineering 회피
- **Button·Input 컴포넌트 추출**: out of scope — I-09 결정
- **모바일 햄버거 메뉴**: out of scope (10-lld-screen-design §5 Open Q 1)
