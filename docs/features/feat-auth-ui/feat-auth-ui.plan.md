---
doc_type: feature-plan
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

# feat-auth-ui — Implementation Plan

> P4 (ADR-0018). 5 commit DAG: C1 ErrorBody 헬퍼 → C2 LoginPage → C3 RegisterPage → C4 Header + App mount hook → C5 docs sync.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 5 commit DAG + ADR-0021 정규식 통과 (feat/docs) + 빌드·부팅·골든패스 시도 검증 + 점진 합의 5건 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `feat(frontend): I-08 ErrorBody 타입 + extractErrorMessage 헬퍼 (#8)` | `frontend/src/types/api.ts` | (없음 — WBS DoD N/A) | 0 — 신규 export만 |
| C2 | `feat(frontend): I-08 LoginPage 실 폼 + 422 한글 에러 인라인 (#8)` | `frontend/src/pages/LoginPage.tsx` | (없음) | 0 — placeholder 대체, 라우팅 변경 없음 |
| C3 | `feat(frontend): I-08 RegisterPage 실 폼 + 422 한글 에러 인라인 (#8)` | `frontend/src/pages/RegisterPage.tsx` | (없음) | 0 |
| C4 | `feat(frontend): I-08 Header 로그인 상태 분기 + App mount loadFromStorage (#8)` | `frontend/src/components/Header.tsx` + `frontend/src/App.tsx` | (없음) | 0 — 라우팅 무변경, useAuthStore 구독 추가만 |
| C5 | `docs(plan): feat-auth-ui + 14-wbs v0.11 + INDEX v0.12 (#8)` | feature docs 8 + 14-wbs + INDEX | (없음) | 0 — docs만 |

ADR-0021 정규식 통과 검증: `feat(frontend):` 4 / `docs(plan):` 1 모두 OK.

## 2. 의존성 그래프

```
C1 (ErrorBody 타입 + helper) ─→ C2 (LoginPage)
                                    │
                                    ▼
                              C3 (RegisterPage)
                                    │
                                    ▼
                              C4 (Header + App mount)
                                    │
                                    ▼
                              C5 (docs sync)
```

- **C1 → C2**: LoginPage가 `extractErrorMessage`를 import해 사용
- **C2 → C3**: RegisterPage가 LoginPage 패턴 reuse (같은 헬퍼 + 같은 ApiError catch 구조)
- **C3 → C4**: Header가 user state 분기 — Login/Register로 도착 가능해야 의미. App mount hook도 같은 커밋에 묶음
- **C4 → C5**: 모든 코드 동작 후 docs sync

순환 없음.

## 3. 테스트 매핑

WBS I-08 DoD에 단위/통합 N/A 명시. E2E는 I-09 골든패스로 위임. 본 PR 검증은 *수동 부팅 + 시도*로 대체:

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C1 | (없음 — 타입만, tsc strict로 검증) | `npm run build` → tsc -b 통과 |
| C2 | (없음 — 수동 브라우저) | `/login` 진입 → email/password 입력 → 정상 자격 시 `/` 이동 + Header 전환. 422 시 한글 메시지 인라인 |
| C3 | (없음 — 수동) | `/register` 진입 → 3 필드 입력 → 201 시 `/` + Header 전환. 중복 email 시 "이미 사용 중인 이메일입니다" |
| C4 | (없음 — 수동) | 새로고침 후 Header 로그인 상태 유지. Logout 클릭 시 `/login` + 로그아웃 메뉴 노출 |
| C5 | (없음 — validate-doc.sh) | 모든 산출 schema PASS |

> backend pytest 77 passed 회귀: N/A (backend 미수정).

## 4. 빌드·실행 검증 단계

```bash
# 1) frontend 빌드 (TS strict + Vite build)
cd frontend && npm run build
# expect: 41+ modules + dist/ 생성 + 에러 0

# 2) backend 동시 부팅 (실 API 검증 필수)
# 터미널 1
cd backend && uv run alembic upgrade head && uv run uvicorn realworld.main:app --port 8000

# 터미널 2
cd frontend && npm run dev
# expect: VITE ready @ 5173

# 3) 브라우저 골든패스 시도 (UC-01 일부)
# (a) /register → username=jane, email=jane@example.com, password=supersecret → 201 + /로 이동 + Header [Home/New Article/jane/Logout]
# (b) 새로고침 → Header 로그인 상태 유지
# (c) /register 재진입 → email 동일 시도 → 422 + "이미 사용 중인 이메일입니다" 인라인
# (d) Logout → /login + [Sign in/Sign up]
# (e) /login → 정상 → 200 + Header 전환

# 4) 백엔드 회귀
cd backend && uv run pytest -v
# expect: 77 passed (변경 0)
```

## 5. 점진 합의 / 결정 발생 항목

- **(1) api/client.ts 401 인터셉터 vs 호출자 catch**: simple catch 패턴 채택. interceptor는 zustand store 직접 import → 순환 의존 위험. 호출자에서 `try/catch (ApiError) { if (e.status === 401) { logout(); nav('/login') }`. 본 PR에서는 LoginPage·RegisterPage에 401 케이스 거의 없음(post 인증 0) — 422 catch만 명시
- **(2) localStorage 키 prefix**: `realworld.token` + `realworld.user` (I-07 정착). 단일 환경 + 학습 컨텍스트라 더 안전한 prefix(예: app name) 불필요
- **(3) Button/Input 컴포넌트 추출**: I-09 결정. 본 PR은 폼 직접 작성 + Tailwind utility(`px-3 py-2 border rounded`)로 충분. 4 폼 필드 + 2 submit button = ~30줄 직접 작성이 over-engineering 회피
- **(4) errors body 한글 메시지 첫 행만 표시**: backend `{errors:{body:["..."]}}`는 list. 본 PR은 list 첫 행만(`body[0]`) 인라인 표시. 다중 에러는 후속 결정 (I-09 폼 검증 강화 시)
- **(5) loadFromStorage 호출 위치**: `App.tsx` mount useEffect 1회 — 가장 simple. zustand 자체 persist 미들웨어 도입은 over-engineering (학습 부담)
