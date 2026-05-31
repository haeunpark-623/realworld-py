---
doc_type: feature-code-review
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

# bug-auth-ux-gap — Code Review

> P9 self-review. 3 코드 커밋. PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-22 | woosung.ahn@bespinglobal.com | 초안 — PASS. build 61 modules + CSS 10.91KB(변경 0) |

## 0. Verdict

**PASS** — 3 코드 커밋(C1·C2·C3) contract §2 8행 매핑. NEEDS-WORK 0건.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (AI self-review)
- [review_at]: 2026-05-22

## 1. 컨트랙트 충실도

| Before/After | Before | After 구현 |
|---|---|---|
| api/client.ts | 401 catch 0 | C1 — status === 401 + token 보유 → store.logout + window.location.assign("/login"). 이미 /login이면 skip(무한 루프 회피) |
| components/RequireAuth.tsx | 없음 | C2 — token 검증 + `<Navigate to="/login" replace />` |
| App.tsx | 7 라우트 직접 | C2 — /editor·/editor/:slug·/profile/:username 3 라우트 `<RequireAuth>` wrap |
| LoginPage | required + minLength | C3 — onInvalid: valueMissing("이메일을 입력해 주세요") + typeMismatch("이메일 형식이 올바르지 않습니다") + password valueMissing |
| RegisterPage | required + minLength | C3 — 3 필드 모두 onInvalid + tooShort("비밀번호는 최소 8자 이상이어야 합니다") |
| EditorPage | required | C3 — title·body onInvalid |
| CommentItem | required 없음 | C3 — button onClick 패턴이라 validation state로 인라인 "댓글 내용을 입력해 주세요" 표시 |
| store/auth.ts | I-08 시그니처 | 무수정 ✅ — getState() 정적 호출 |

## 2. 테스트 커버리지

WBS DoD frontend N/A. 검증:
- TS strict `tsc -b` 통과
- Vite build **61 modules in 1.23s** (60 + RequireAuth)
- CSS 10.91KB 유지 (한글 메시지는 string 변경만, utility 추가 0)
- backend pytest 77 passed 회귀 N/A

## 3. 보안 / 시크릿

- 401 인터셉터 — token 보유 시에만 logout 발현 (token 없으면 noop). XSS·CSRF 영향 0
- RequireAuth — client-side guard만. backend API는 별도 require_auth 강제(I-03)라 2중 방어
- setCustomValidity 메시지 — 한글 string 상수, 변수 보간 없음 — XSS 0

## 4. 가독성 / 단순성

- RequireAuth 17줄 — 단일 책임
- App.tsx wrap pattern — `<RequireAuth><EditorPage /></RequireAuth>` 인라인. wrap 함수 추출은 over-engineering(3 라우트뿐)
- 4 폼 onInvalid 패턴 일관 — `e.currentTarget.validity.valueMissing` 분기 + onInput clear

## 5. 발견 사항 (3축 OX 분류)

| 발견 | in_scope | blocks_merge | same_area | 처리 |
|---|---|---|---|---|
| F1: I-08 simple catch 패턴 회귀 — 학습 회고 메모 | ⭕ | ❌ | ⭕ | retro 2026-05-21 §개선점에 명시. 본 PR이 closure |
| F2: window.location.assign 전체 새로고침 | ⭕ | ❌ | ⭕ | F-RISK-02 의도 |
| F3: CommentItem만 패턴 다름 (state vs setCustomValidity) | ⭕ | ❌ | ⭕ | 의도 — button onClick이라 HTML5 validation 미발현 |
| F4: onInvalid 한글 메시지 hardcoded — i18n N/A | ⭕ | ❌ | ⭕ | 의도. 10-lld §5 Open Q 4 다국어 Out of Scope |
| F5: ProfilePage RequireAuth wrap — 비회원 타인 프로필 차단 | ⭕ | ❌ | ⭕ | 의도. RFP §5 비회원 타인 프로필 Out of Scope |
| F6: 라우트 wrap이 inline `<RequireAuth>`로 3회 반복 — 헬퍼 추출? | ⭕ | ❌ | ⭕ | INFO. 3 라우트 한정이라 over-engineering |

NEEDS-WORK 0건.

## 6. NEEDS-WORK 항목

(없음)
