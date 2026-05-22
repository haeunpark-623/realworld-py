---
doc_type: feature-eng-review
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

# bug-auth-ux-gap — Engineering Review

> P5 plan-eng-review. PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-22 | woosung.ahn@bespinglobal.com | 초안 — PASS, 6 OX 모두 PASS |

## 0. Verdict

**PASS** — contract §0 5행·§2 8행 + plan 4 commit DAG. I-08 simple catch 패턴 회귀 결정 명시. P8 진입 허용.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (self-review)
- [review_at]: 2026-05-22

## 1. Contract 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| §0 Referenced-IDs 5행 | ✅ | SRS R-F-01·02·03 / PRD F-01·F-04 / 10-lld-screen §1.1·§4 / ADR-0044 / Test catalog N/A |
| §1 변경 의도 | ✅ | 3건 동시 fix + I-08 simple catch 회귀 결정 trace |
| §2 Before/After 8행 | ✅ | RequireAuth + App wrap + 4 폼 onInvalid + api 401 + store 무수정 |
| §3 Call Sites 4행 | ✅ | App routes / apiFetch / store getState / 4 폼 |
| §4 BC neutral | ✅ | 시그니처 모두 무수정. 비로그인 /editor 진입은 UX 개선 방향 |
| §5 Rollback 1-commit revert | ✅ | squash merge 자동 revert |

## 2. Plan 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| §1 4 commit DAG | ✅ | C1 api 401 → C2 RequireAuth → C3 onInvalid → C4 docs |
| §2 의존성 그래프 | ✅ | 순환 0, 3 코드 commit 독립 |
| §3 테스트 매핑 N/A | ✅ | 수동 검증으로 갈음 |
| §4 빌드·실행 검증 | ✅ | build + 동시 부팅 + 3 시나리오 + 회귀 |
| §5 점진 합의 5건 | ✅ | I-08 회귀·window.location·fallback·wrap·preventDefault |

## 3. UX 검토

- 10-lld-screen-design §1.1 헤더 일관성 — Header.tsx 무수정, RequireAuth는 라우트 가드 (헤더는 그대로 표시)
- §4 a11y — onInvalid 한글 메시지는 시각+텍스트 동시 (브라우저 native validation tooltip 그대로 사용)
- F-04 §5 "에러 메시지 한글" 원칙 — 본 PR로 충족

## 4. 6단계 폴더링 충족

- `docs/features/bug-auth-ux-gap/*.md` — **bug-** 접두 (mode=bug, ADR-0044 정합)
- branch: `bug/auth-ux-gap-issue-21` 정합

## 5. frontmatter / Manifest 검증

- 8 산출 doc_type 정합, R-ID 3·F-ID 2 정합, date=2026-05-22

## 6. 발견 사항 (3축 OX)

| Q | 답 | 처리 |
| --- | --- | --- |
| F1: I-08 simple catch 패턴 회귀 — ADR 미작성 | ⭕ in_scope / ❌ no / ⭕ same_area | INFO. contract §1 + plan §5 (1) trace로 충분. simple catch 결정이 실효성 없었음(호출자 0곳 실 구현)을 인정 |
| F2: `window.location.assign` 전체 새로고침 — Vite HMR state 손실 | ⭕ / ❌ / ⭕ | INFO. logout 시점이라 state reset이 의도된 동작. UX 일관성 |
| F3: RequireAuth 비로그인 `/profile/:username` wrap — 비회원도 타인 프로필 볼 수 있어야 하지 않나? | ⭕ / ❌ / ⭕ | 결정. PRD §3 F-02 R-F-12 "내 글 목록" 한정 — 비회원 타인 프로필 조회는 RFP §5 Out of Scope. 본 PR도 wrap 유지 |
| F4: onInvalid 메시지가 한국어 고정 — 다국어 i18n? | ⭕ / ❌ / ⭕ | 의도. 10-lld §5 Open Q 4 다국어 Out of Scope |
| F5: api/client 401 분기 후 throw 여부 | ⭕ / ❌ / ⭕ | 결정. throw 유지 — 호출자 finally·setLoading(false) 정상 동작 보장. redirect는 별도 부수 효과 |
| F6: HomePage·ArticlePage·LoginPage·RegisterPage는 wrap 안 함 — 의도 | ⭕ / ❌ / ⭕ | 의도. 비로그인 진입 가능 라우트 (PRD §3 R-F-04·R-F-05 비회원 접근 가능) |

NEEDS-WORK 0건.

## 7. NEEDS-WORK 항목

(없음)