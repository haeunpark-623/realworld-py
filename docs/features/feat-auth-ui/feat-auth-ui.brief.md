---
doc_type: feature-brief
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

# feat-auth-ui — Feature Brief

> Sprint 2 세 번째 이슈 (I-08). LoginPage·RegisterPage 실 폼 + AuthStore 실 구현 + Header 로그인 상태 분기.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — mode=add 자동 결정. ui_changed=true. Login/Register 폼 + 422 한글 에러 인라인 + AuthStore localStorage + Header 분기 |

## 1. 한 줄 의도

I-07 placeholder였던 LoginPage·RegisterPage에 실 폼(react controlled inputs) + 백엔드 `POST /api/users` (R-F-01)·`POST /api/users/login` (R-F-02) 호출 + 422 한글 에러 인라인 + AuthStore login/logout + Header가 store 구독해 로그인 상태 [Home/Editor/{username}/Logout] vs [Sign in/Sign up] 분기.

## 2. 사용자 가치

- **신규 가입 사용자**: `/register`에서 정상 폼 제출 → 201 + JWT localStorage 저장 + Header 로그인 전환 → `/` 이동 (UC-01). 중복 email 시 422 한글 에러 ("이미 사용 중인 이메일입니다") 인라인
- **기존 사용자**: `/login`에서 정상 자격 → 200 + JWT 저장 + Header 전환. 422 시 한글 메시지
- **새로고침 후 로그인 유지**: `App` mount 시 `loadFromStorage()` 자동 호출 → localStorage 토큰 복원 → Header 로그인 상태 유지 (token 보유 = 로그인 가정. `GET /api/user` 검증은 I-09)
- **로그아웃**: Header [Logout] 클릭 → `useAuthStore.logout()` + `/login` 이동
- **자동 로그아웃**: 401 응답(만료·변조) 시 호출자가 catch + logout (plan §5 simple 패턴)

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 (I-07) | 변경 후 (I-08) |
| --- | --- | --- |
| `pages/LoginPage.tsx` | placeholder text only | 실 폼: email + password controlled inputs + `<form onSubmit>` + `apiFetch('/users/login', POST)` + 응답 시 `useAuthStore.login()` + `useNavigate('/')` + 422 시 errors.body 한글 메시지 인라인 |
| `pages/RegisterPage.tsx` | placeholder text only | 실 폼: username + email + password 3 필드 + POST `/users` + 422 시 메시지 인라인 |
| `store/auth.ts` | zustand placeholder (이미 login/logout/loadFromStorage 메서드 완비) | 무수정 — I-07에서 이미 실 동작 가능. App.tsx mount hook 추가는 별 컴포넌트 변경 |
| `api/client.ts` | placeholder `apiFetch<T>` | 무수정 — ApiError throw 패턴 그대로. 401 처리는 호출자 catch (plan §5 simple, interceptor 회피) |
| `components/Header.tsx` | 4 메뉴 고정 (Home/New Article/Sign in/Sign up) | useAuthStore 구독 → logged-in: [Home / New Article / {username} / Logout] / logged-out: [Sign in / Sign up] |
| `App.tsx` | mount 시 store load 없음 | `useEffect(() => { useAuthStore.getState().loadFromStorage(); }, [])` 추가 |
| 통합 동작 | 6 라우트 placeholder | end-to-end: register → JWT 저장 → Header 전환 → `/` 이동 + 로그아웃 → 다시 `/login` (UC-01) |
| 테스트 | 0건 | 0건 (WBS DoD N/A. E2E 검증은 I-09 골든패스) |

## 4. 모드 자동 감지 결과

**mode = add** (자동 결정, ADR-0032 규칙 4).

- 부정 시그널 0건: `type:bug` 라벨 없음 / UI 변경 키워드(다크모드/리브랜딩/token) 없음 / 기존 placeholder는 *대체*가 아닌 *실 구현으로 채움* (modify 시그널 아님)
- 라벨: `type:feature` + `area:frontend`
- 자동 결정 trace: 규칙 4 발동 → add 진행

**ui_changed=true** — 실 UI 동작 도입. LoginPage·RegisterPage·Header 시각 변화 + 폼 인터랙션 + 에러 메시지 인라인. ADR-0011 5번째 축 검증 — Manual verification에 스크린샷 4장(login·register·logged-in header·422 error) 첨부 명시.

## 5. 영향 범위

**touched_areas**: 1 영역 (frontend) — 단일 영역.

- `frontend/src/pages/LoginPage.tsx` — 실 구현
- `frontend/src/pages/RegisterPage.tsx` — 실 구현
- `frontend/src/components/Header.tsx` — useAuthStore 구독 + 분기
- `frontend/src/App.tsx` — useEffect loadFromStorage 1 hook 추가
- (선택) `frontend/src/types/api.ts` — ErrorBody narrow 타입 추가
- `docs/planning/14-wbs/14-wbs.md` v0.10 → v0.11 (I-08 in-review, P13)
- `docs/planning/INDEX.md` v0.11 → v0.12 (P13)

backend 영향: 0 (Issue #4 라우트 무수정 사용).

## 6. 비목표

- **모바일 햄버거 메뉴**: out of scope (10-lld-screen-design §5 Open Q 1)
- **소셜 로그인 (OAuth)**: out of scope (RFP §5)
- **비밀번호 reset / forgot / 이메일 인증**: out of scope (RFP)
- **GET /api/user 호출로 token 검증**: I-09에서 진입 — 본 이슈는 token 보유 = 로그인 가정
- **단위/통합 테스트**: WBS DoD N/A. E2E는 I-09 골든패스
- **Button·Input 컴포넌트 추출**: I-09에서 결정 — 본 이슈는 폼 직접 + Tailwind utility
- **api/client.ts 401 인터셉터 자동화**: simple catch 패턴 채택 (plan §5)

## 7. Open Questions

- **errors body 타입 narrow**: backend는 `{errors:{body:["..."]}}`. `ApiError.body`는 `unknown`. 폼 컴포넌트에서 narrow 헬퍼 함수 (`extractErrorMessage(e: ApiError): string`) 도입 vs 인라인 type guard. 결정: types/api.ts에 헬퍼 추가
