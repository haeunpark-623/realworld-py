---
doc_type: feature-plan
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

# bug-auth-ux-gap — Implementation Plan

> P4. 4 commit DAG: C1 api/client 401 → C2 RequireAuth + App.tsx → C3 4 폼 onInvalid → C4 docs.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-22 | woosung.ahn@bespinglobal.com | 초안 — 4 commit DAG + ADR-0021 통과 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `fix(frontend): apiFetch 401 자동 logout + /login 리다이렉트 (#21)` | `frontend/src/api/client.ts` | (없음) | 0 — 신규 분기 추가만 |
| C2 | `fix(frontend): RequireAuth 컴포넌트 + 3 라우트 비로그인 차단 (#21)` | `frontend/src/components/RequireAuth.tsx` 신규 + `frontend/src/App.tsx` wrap | (없음) | 0 — login/register/home/article 진입 무영향 |
| C3 | `fix(frontend): 4 폼 onInvalid 한글 에러 메시지 (#21)` | `frontend/src/pages/LoginPage.tsx` + `RegisterPage.tsx` + `EditorPage.tsx` + `frontend/src/components/CommentItem.tsx` | (없음) | 0 — onInvalid/onInput 핸들러만 추가 |
| C4 | `docs(plan): bug-auth-ux-gap 8 산출 + INDEX v0.15 (#21)` | feature docs 8 + INDEX | (없음) | 0 — docs only |

ADR-0021 통과: fix(frontend) 3 + docs(plan) 1.

## 2. 의존성 그래프

```
C1 (api/client 401) ─┐
                     ├─→ C4 (docs)
C2 (RequireAuth) ────┤
                     │
C3 (4 폼 onInvalid)──┘
```

- C1·C2·C3 모두 독립 — 어느 순서로도 가능. C4가 docs sync로 마지막
- C1을 먼저: api/client 401 분기가 가장 중요 (사이드 이펙트 핵심)
- C2 다음: 라우트 가드 가시화
- C3 마지막: UX polish

## 3. 테스트 매핑

WBS DoD frontend 자동 테스트 N/A. 수동 검증:

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C1 | (없음) | DevTools에서 `localStorage.clear()` → 새로고침 → `/editor` 작성 후 submit → 401 발생 → 자동 logout + /login 이동 확인 |
| C2 | (없음) | 비로그인 상태에서 `/editor` URL 직접 입력 → 즉시 /login 리다이렉트. HomePage/ArticlePage는 비로그인 진입 가능 유지 (회귀 0) |
| C3 | (없음) | 4 폼 각각에서 빈 필드 submit → 한글 "○○을 입력해 주세요" 표시 + 입력 시 메시지 사라짐 |
| C4 | (validate-doc.sh) | 8 산출 + INDEX schema PASS |

> backend 회귀 N/A (미수정). pytest 77 passed 유지.

## 4. 빌드·실행 검증 단계

```bash
# 1) TS strict + Vite build
cd frontend && npm run build
# expect: 60+ modules + dist/ + 에러 0

# 2) 동시 부팅
cd backend && uv run uvicorn realworld.main:app --port 8000 &
cd frontend && npm run dev

# 3) 수동 검증 (3 시나리오)
# A. 로그아웃 상태에서 /editor URL → 즉시 /login으로 이동
# B. /login에서 빈 폼 submit → "이메일을 입력해 주세요" 한글
# D. 로그인 후 DevTools Application > Local Storage > realworld.token 수정 (무효값)
#    → 새 글 작성 시도 → 401 발생 → 자동 logout + /login

# 4) 회귀
cd backend && uv run pytest -v
# expect: 77 passed
```

## 5. 점진 합의 / 결정 발생 항목

- **(1) I-08 simple catch 패턴 회귀 결정**: api/client.ts 중앙 401 분기로 전환. contract §1 + brief §7 trace
- **(2) `window.location.assign` vs `useNavigate`**: api/client는 hook 외부라 useNavigate 사용 불가. `window.location.assign("/login")`은 전체 페이지 새로고침이지만 user-facing UX는 동일 — store reset도 확실
- **(3) RequireAuth fallback 화면**: token 0이면 즉시 `<Navigate replace>` — 별도 로딩 화면 0 (즉각 분기)
- **(4) `/editor/:slug` 도 wrap**: 수정 모드도 인증 필요. App.tsx routes에서 일괄 wrap
- **(5) onInvalid `e.preventDefault()` 호출 안 함**: 브라우저 default tooltip 자체는 한글 메시지로 *대체*만 — UX 좋게 유지