---
doc_type: feature-code-review
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

# feat-auth-ui — Code Review

> P9 self-review. 4 코드 커밋(C1·C2·C3·C4). PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — PASS, 6 OX 모두 PASS. build 57 modules + CSS 8.08KB (+1.76KB) + dev 608ms |

## 0. Verdict

**PASS** — 4 코드 커밋 contract §2 6행 매핑. build/dev 양쪽 PASS. NEEDS-WORK 0건.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (AI self-review)
- [review_at]: 2026-05-21

## 1. 컨트랙트 충실도

| Before/After | Before | After 구현 |
|---|---|---|
| `frontend/src/types/api.ts` | 6 type aliases | C1 — + ErrorBody + isErrorBody + extractErrorMessage (fallback "알 수 없는 오류가 발생했습니다") |
| `frontend/src/pages/LoginPage.tsx` | placeholder | C2 — controlled inputs (email/password) + handleSubmit + apiFetch('/users/login', POST) + login store + navigate('/') + ApiError catch → extractErrorMessage 인라인 |
| `frontend/src/pages/RegisterPage.tsx` | placeholder | C3 — 3 controlled inputs (username/email/password) + POST '/users' + 동일 catch 패턴. HTML5 required + minLength/maxLength로 422 round-trip 최소화 |
| `frontend/src/components/Header.tsx` | 4 메뉴 고정 | C4 — useAuthStore(state => state.user) 구독 + ternary 분기 ([Home/New Article/{username}/Logout] vs [Sign in/Sign up]) + handleLogout |
| `frontend/src/App.tsx` | mount load 없음 | C4 — useEffect(loadFromStorage, []) hook 추가 |
| `frontend/src/store/auth.ts` | I-07 placeholder | 무수정 ✅ — 시그니처 그대로 사용 |

contract §3 Call Sites:
- ✅ apiFetch — fetch 래퍼 그대로 (I-07 시그니처)
- ✅ useAuthStore — selector 패턴 (login·logout·user) 사용
- ✅ backend Issue #4 라우트 — 무수정 호출
- ✅ CORS 5173 origin — 정착

contract §4 BC neutral, §5 Rollback 1-commit revert 모두 정합.

## 2. 테스트 커버리지

WBS DoD N/A — 자동 테스트 0건. 수동 검증:

- **build**: 57 modules transformed in 1.52s. dist/ CSS 8.08KB gzip 2.16KB / JS 175.68KB gzip 56.92KB. I-07 대비 16 modules + CSS 1.76KB 추가 (Tailwind utility 실 추출)
- **dev**: Vite ready in 608ms (5173 점유로 5174 fallback). HMR 정상
- **TS strict**: `tsc -b` 통과. noUnusedLocals + noUnusedParameters + strict 모두 통과
- **backend 회귀**: backend 미수정 → pytest 77 passed 회귀 N/A

## 3. 보안 / 시크릿

- JWT localStorage 평문 저장 — RealWorld spec 동일 패턴 (학습 컨텍스트 acceptable, 15-risk RISK-02 인지)
- 신규 환경변수 0 — `.env` 변경 없음
- XSS: React JSX 기본 escape + `dangerouslySetInnerHTML` 0 + error message는 `{errorMessage}` text node 렌더링
- input 검증: HTML5 required + min/max length (backend Pydantic과 1:1) + email type
- autoComplete: `email/current-password/username/new-password` — 브라우저 패스워드 매니저 호환
- API 호출: `apiFetch` JSON body — SQL injection 영향 0 (백엔드 ORM)
- `Content-Security-Policy` / `X-Frame-Options`: 본 PR scope out — Vite dev 서버 기본값 그대로

`/cso` 점검 대상 0. R-N-04·R-N-05 위반 0.

## 4. 가독성 / 단순성

- LoginPage 89줄 / RegisterPage 109줄 — controlled inputs + form submit + catch 패턴 직선
- 두 페이지 *거의 동일 패턴* — DRY 위반 우려 있지만 *2개뿐 + 폼 필드 다름*이라 별도 추상화 안 함 (3건 이상 시 폼 컴포넌트 추출 검토)
- Header ternary 분기 — JSX fragment로 logged-in/out 그룹 분리. 가독성 명확
- 주석 minimal — 각 페이지 첫 line `// S-NN (R-F-XX). Issue #8 실 구현.` 만
- Tailwind utility 직접 사용 — Button/Input 컴포넌트 추출은 plan §5 (3) 결정으로 over-engineering 회피

## 5. 발견 사항 (3축 OX 분류)

| 발견 | in_scope | blocks_merge | same_area | 처리 |
|---|---|---|---|---|
| F1: LoginPage·RegisterPage 폼 패턴 거의 동일 — DRY 위반 | ⭕ | ❌ | ⭕ | INFO. 2건뿐이라 추상화 비용이 더 큼. I-09에서 3개 이상 폼 추가 시 재검토 |
| F2: extractErrorMessage가 fallback "알 수 없는 오류가 발생했습니다" — 사용자에게 비표준 에러 디버깅 정보 0 | ⭕ | ❌ | ⭕ | 의도. RealWorldError 형식 통일이라 fallback 발현 가능성 낮음. F-RISK-03 명시 |
| F3: App.tsx useEffect deps `[]` — React strict mode dev에서 2번 호출 | ⭕ | ❌ | ⭕ | INFO. zustand getState() 사용으로 정적 호출 + state 변경 후 같은 결과 (idempotent) — 무한 루프 0 |
| F4: Header user.username Link → /profile/{username} — ProfilePage placeholder 그대로 (P2 컷 후보) | ⭕ | ❌ | ⭕ | 의도. 14-wbs §0.3 P2 컷 후보. Link 노출만 + ProfilePage 본문은 I-09 결정 |
| F5: ui_changed=true — ADR-0011 스크린샷 검증 사람 책임 위임 | ⭕ | ❌ | ⭕ | 의도. ai-qa-report §6에 명시 |
| F6: handleLogout이 logout() 후 navigate('/login') — 순서 의존성 | ⭕ | ❌ | ⭕ | INFO. zustand set이 동기 + navigate는 React Router 비동기 effect라 순서 정합 |

NEEDS-WORK 0건.

## 6. NEEDS-WORK 항목

(없음) — 6 OX 모두 PASS. P10 ai-qa-report 진입 허용.
