---
doc_type: feature-acceptance
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-22
gate: feature
related:
  R-ID: [R-F-01, R-F-02, R-F-03]
  F-ID: [F-01, F-04]
  supersedes: null
---

# bug-auth-ux-gap — Acceptance Criteria

> P6. 6 AC + 6 DoD.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-22 | woosung.ahn@bespinglobal.com | 초안 — 6 AC + 6 DoD |

## 1. 인수 기준 (Given/When/Then)

| ID | Given | When | Then | 출처 |
| --- | --- | --- | --- | --- |
| AC-01 | 비로그인 사용자 + 브라우저 | URL bar에 `/editor` 직접 입력 | 즉시 `/login`으로 리다이렉트. 폼 노출 0건 (A) | PRD §3 F-02 실패-2 |
| AC-02 | 비로그인 사용자 | `/editor/{slug}` 또는 `/profile/{username}` 직접 입력 | 즉시 `/login` 리다이렉트 | contract §1 (A) |
| AC-03 | LoginPage / RegisterPage / EditorPage / CommentItem 4 폼 | 빈 필드(또는 minLength 미달) submit | 한글 메시지 "○○을 입력해 주세요" 또는 "8자 이상 입력해 주세요" 브라우저 tooltip 노출. 입력 시 메시지 사라짐 (B) | F-04 §5 |
| AC-04 | 로그인 상태 + localStorage 토큰 무효화(예: DevTools clear) | 새 글 작성 PUT/POST 시도 (또는 댓글 수정) | 401 응답 → 자동 logout (store user/token null) + `/login` 리다이렉트 (D) | PRD §3 F-01 실패-3 |
| AC-05 | 로그인 상태 | `/` 또는 `/article/{slug}` 또는 `/login` 진입 | 정상 진입 (회귀 0 — RequireAuth wrap 안 됨) | contract §3 |
| AC-06 | 로그인 상태 + Vite dev hot reload | 4 폼 진입 + 정상 입력 후 submit | 회귀 0 — POST/PUT 정상 동작 | contract §4 |

## 2. Definition of Done (D-06)

본 follow-up Issue DoD 6건:

- [ ] D-21-1 `components/RequireAuth.tsx` 신규 — token 0 시 `<Navigate to="/login" replace />`
- [ ] D-21-2 `App.tsx` — `/editor`·`/editor/:slug`·`/profile/:username` 3 라우트 wrap
- [ ] D-21-3 LoginPage·RegisterPage·EditorPage·CommentItem 4 폼 — onInvalid 한글 메시지 + onInput clear
- [ ] D-21-4 `api/client.ts` — 401 분기 (useAuthStore.getState().logout + window.location.assign)
- [ ] D-21-5 backend pytest **77 passed** 회귀 유지 (backend 미수정)
- [ ] D-21-6 frontend `npm run build` TS strict 통과

## 3. 비기능 인수

- **R-N-04 (시크릿)**: 본 PR 시크릿 변경 0
- **R-N-05 (XSS)**: setCustomValidity 메시지는 한글 문자열 상수 — XSS 영향 0
- **R-N-06 (커버리지)**: backend 무영향 → 80% 유지

## 4. 회귀 인수

- backend pytest 77 passed 유지
- HomePage·ArticlePage·LoginPage·RegisterPage 비로그인 진입 가능 (회귀 0)
- 4 폼 정상 입력 시 submit 동작 (onInvalid 핸들러는 빈/잘못된 입력에만 발현)
- Vite build 60+ modules + TS strict