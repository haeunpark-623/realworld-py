---
doc_type: feature-contract
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

# bug-auth-ux-gap — Change Contract

> P3 (ADR-0018). mode=bug — PRD §3 F-01 실패 path 3건 acceptance gap closure.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-22 | woosung.ahn@bespinglobal.com | 초안 — §0 5행 + §2 8행 + §3 4행 + BC neutral(시그니처 호환) + Rollback 1-commit revert |

## 0. 참조 정본 ID (Referenced-IDs)

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| SRS | `docs/planning/04-srs/04-srs.md` §6.1 R-F-01·02·03 | R-F-01, R-F-02, R-F-03 |
| PRD | `docs/planning/05-prd/05-prd.md` §3 F-01 실패-3 (JWT 만료) + F-04 §5 한글 메시지 원칙 | F-01, F-04 |
| LLD-Screen | `docs/planning/10-lld-screen-design/10-lld-screen-design.md` §1.1 헤더 일관성 + §4 a11y(에러 메시지) | (none) |
| ADR | `policies/branch-strategy.md` ADR-0044 mode=bug branch `bug/<slug>-issue-<N>` | (none) |
| Test Catalog | N/A — WBS DoD frontend 자동 테스트 N/A 정착 (I-09) | (none) |

## 1. 변경 의도

PRD §3 F-01 실패 path 3건이 본 사이클(PR #11~#20)에서 미달 또는 부분 미달. 본 follow-up PR로 3건 동시 fix:
- **A 비로그인 `/editor` 차단**: PRD §3 F-02 실패-2("비로그인 글쓰기 시도 → 401 + 로그인 페이지 이동")
- **B 빈 폼 한글 에러**: F-04 §5 "에러 메시지 한글" 원칙 (브라우저 default tooltip은 영문 시스템 locale)
- **D JWT 만료 자동 logout**: PRD §3 F-01 실패-3("JWT 만료 후 API 호출 → 401 + 로그인 페이지로 자동 이동")

**중앙 인터셉터 회귀 결정 (brief §7 Open Q)**: I-08 plan §5 (1) "simple catch 패턴"은 호출자가 401 분기를 작성하는 책임이었으나 실제로는 호출자 0곳에 분기 작성 → I-08의 결정이 실효성 없었음. 호출자 7곳 중복 회피 위해 본 PR에서 api/client.ts apiFetch에 401 분기 1곳으로 회귀.

## 2. Before / After

| 항목 | Before | After |
| --- | --- | --- |
| `frontend/src/components/RequireAuth.tsx` | 없음 | 신규 — props `{ children }`. useAuthStore token 0 시 `<Navigate to="/login" replace />` |
| `frontend/src/App.tsx` | 7 라우트 직접 | `/editor`·`/editor/:slug`·`/profile/:username` 3 라우트를 `<RequireAuth>`로 wrap (HomePage·ArticlePage·LoginPage·RegisterPage는 비로그인 접근 가능 유지) |
| `frontend/src/pages/LoginPage.tsx` | required + minLength 만 | + `onInvalid={e => e.currentTarget.setCustomValidity("...")}` + `onInput={e => e.currentTarget.setCustomValidity("")}` — email·password 2 필드 |
| `frontend/src/pages/RegisterPage.tsx` | required + minLength | + onInvalid 핸들러 — username·email·password 3 필드 |
| `frontend/src/pages/EditorPage.tsx` | required | + onInvalid 핸들러 — title·body 2 필드 |
| `frontend/src/components/CommentItem.tsx` | required | + onInvalid — body textarea |
| `frontend/src/api/client.ts` | `if (!response.ok) throw new ApiError(...)` | + 401 분기: `if (response.status === 401) { useAuthStore.getState().logout(); window.location.assign("/login"); }` (위치: 401 case는 store 호출 후 throw — 호출자가 finally·error state로 복원하기 전에 redirect) |
| `frontend/src/store/auth.ts` | 무수정 | 무수정 ✅ (getState로 정적 호출, hook 의존 없음) |

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| App.tsx routes — 3 라우트 wrap | 비로그인 진입 자동 차단 | RequireAuth import + wrap |
| 모든 페이지 apiFetch 호출 | 401 시 자동 logout (인터셉터 회귀) | 호출자 catch 분기 추가 0 — 중앙 1곳만 |
| useAuthStore.getState | api/client.ts에서 정적 호출 | hook 의존 0 — 순환 의존 회피 |
| 4 폼 input onInvalid | 한글 메시지 설정 | 신규 핸들러 추가 |

## 4. Backward Compatibility

**BC neutral** — 모든 외부 인터페이스 무수정:
- apiFetch 시그니처 그대로
- useAuthStore 시그니처 그대로
- 6 페이지 props 그대로
- 라우트 path 그대로

기존 동작 변경: 비로그인 `/editor` 진입 시 *폼 노출*에서 *즉시 리다이렉트*로 변경 — UX 개선 방향이라 deprecation 경로 불필요.

## 5. Rollback 전략

**1-commit revert로 충분**:
- RequireAuth.tsx 삭제 + App.tsx 3 라우트 unwrap
- 4 폼 onInvalid 핸들러 제거
- api/client.ts 401 분기 제거

squash merge 단일 commit 자동 revert. 데이터 영향 0.

## 6. 비목표

- **GoBack 패턴**: login 후 원래 URL 복귀는 out of scope — 단순 `/`로 이동
- **JWT refresh 토큰**: out of scope (RFP §3)
- **react-router loader / data API**: out of scope — 단순 `<Navigate>` 사용
- **Vitest 단위 테스트**: out of scope (frontend WBS DoD N/A 정책 유지)