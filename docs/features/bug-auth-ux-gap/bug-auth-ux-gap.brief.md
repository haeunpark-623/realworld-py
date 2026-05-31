---
doc_type: feature-brief
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

# bug-auth-ux-gap — Feature Brief

> Sprint 2 완주 후 follow-up bug fix (Issue #21). PRD §3 F-01 실패 path 3건 acceptance gap closure. mode=bug.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-22 | woosung.ahn@bespinglobal.com | 초안 — mode=bug 자동 결정. PRD §3 F-01 실패-3 + F-04 §5 한글 메시지 + 시나리오 1 비로그인 차단 3건 동시 fix |

## 1. 한 줄 의도

PRD §3 F-01 실패 path 중 본 사이클에서 미달했던 3건 — (A) 비로그인 `/editor` 진입 자동 차단 + `/login` 리다이렉트 / (B) 빈 폼 submit 시 한글 에러 메시지 / (D) JWT 만료 후 401 자동 logout + 리다이렉트 — 을 `RequireAuth` 컴포넌트 + `onInvalid setCustomValidity` + api/client.ts 401 catch 패턴으로 닫는다.

## 2. 사용자 가치

- **신규/기존 사용자**: 비로그인 상태에서 `/editor` URL 직접 진입해도 혼란 없이 `/login`으로 자연스러운 흐름 (A)
- **모든 폼 사용자**: 빈 필드 submit 시 영문 브라우저 default 대신 한글 안내 — UX 일관성 (B). F-04 §5 "에러 메시지 한글" 원칙 충족
- **장기 사용자**: 7일 JWT 만료 후 API 호출 시 무한 "네트워크 오류" 메시지 대신 즉시 logout + 재로그인 흐름으로 복귀 (D)

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 (PR #20 완주 후) | 변경 후 |
| --- | --- | --- |
| 비로그인 `/editor` 진입 | 폼 노출 → submit 시점에 "로그인이 필요합니다" 인라인 (혼란) | `RequireAuth` 래퍼가 token 0 시 `<Navigate to="/login" replace />` 즉시 차단 |
| 빈 필드 submit | 브라우저 default tooltip (영문 시스템 locale) | `onInvalid` 핸들러 + `setCustomValidity("이메일을 입력해 주세요")` 한글 + `onInput` clear |
| JWT 만료 401 | catch → "네트워크 오류" 또는 "API 401" 표시 (사용자 수동 logout 필요) | api/client.ts apiFetch에서 401 감지 → `useAuthStore.getState().logout()` + `window.location.assign("/login")` |
| 신규 컴포넌트 | (없음) | `components/RequireAuth.tsx` 신규 |
| 수정 파일 | (없음) | App.tsx wrap 3 라우트 / 4 폼 onInvalid / api/client.ts 401 분기 |

## 4. 모드 자동 감지 결과

**mode = bug** (자동 결정 — `type:bug` 라벨 + PRD acceptance gap 보강 시그널).

- 부정 시그널 1건: type:bug 라벨 → 규칙 1 발동
- 자동 결정 trace: PRD §3 F-01 실패-1·실패-2·실패-3 acceptance가 본 사이클에서 부분 미달 → bug fix
- debug-investigator 단계: 본 brief에 3 케이스 모두 재현 시나리오 명시 (위 §3) — 별도 investigation.md 생성 불필요

## 5. 영향 범위

**touched_areas**: 1 영역 (frontend).

- `frontend/src/components/RequireAuth.tsx` — 신규
- `frontend/src/App.tsx` — 3 라우트 wrap
- `frontend/src/pages/LoginPage.tsx` — onInvalid 핸들러
- `frontend/src/pages/RegisterPage.tsx` — onInvalid 핸들러
- `frontend/src/pages/EditorPage.tsx` — onInvalid 핸들러
- `frontend/src/components/CommentItem.tsx` — onInvalid 핸들러
- `frontend/src/api/client.ts` — 401 catch 분기
- `docs/planning/INDEX.md` — v0.14 → v0.15 (P13)

backend 영향: 0.

## 6. 비목표

- **회귀 테스트 추가**: 본 follow-up은 frontend WBS DoD N/A 정책 유지. E2E 자동화는 다음 사이클 (Vitest 도입 검토)
- **JWT refresh 토큰**: out of scope — 만료 후 재로그인 패턴 유지 (RFP §3)
- **Protected Route SSR/loader 기반**: out of scope — 단순 token 검증
- **GoBack 패턴 (login 후 원래 URL 복귀)**: out of scope — 단순 `/` 또는 `/login` 이동

## 7. Open Questions

- **401 catch 위치 — api/client.ts vs 호출자 catch (I-08 plan §5 (1) 결정 회귀)**: I-08은 simple catch 채택했으나 본 PR에서 *중앙 인터셉터로 회귀* 결정. 이유: 호출자 7곳(LoginPage·RegisterPage·EditorPage·ArticlePage·HomePage·ProfilePage·CommentItem)에 같은 분기 7중복은 명백한 DRY 위반. 본 contract §1에서 결정 trace