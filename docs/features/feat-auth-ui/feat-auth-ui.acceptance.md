---
doc_type: feature-acceptance
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

# feat-auth-ui — Acceptance Criteria

> P6. WBS Issue #8 DoD Checklist 7건 매핑 + 5 AC.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 5 AC + 7 DoD (D-08-1~7) + Manual verification 스크린샷 4장 |

## 1. 인수 기준 (Given/When/Then)

| ID | Given | When | Then | 출처 |
| --- | --- | --- | --- | --- |
| AC-01 | backend 부팅(:8000) + frontend 부팅(:5173) + 신규 사용자 | `/register` → username=jane, email=jane@example.com, password=supersecret 입력 → submit | 201 Created + JWT localStorage `realworld.token` 저장 + Header [Home/New Article/jane/Logout] 분기 + `/` 자동 이동 (R-F-01, UC-01) | WBS I-08 AC + 09-api-spec §3 |
| AC-02 | 가입 사용자 + 같은 email로 재시도 | `/register` → 동일 email 입력 → submit | 422 + `errors.body[0]` "이미 사용 중인 이메일입니다" 인라인 표시 (h1 아래 빨강 박스) (R-F-01) | 09-api-spec §3 |
| AC-03 | 가입 사용자 + 로그아웃 상태 | `/login` → email + password 입력 → submit | 200 + JWT 저장 + Header 전환 + `/` 이동 (R-F-02) | 09-api-spec §3 |
| AC-04 | 가입 사용자 + Header [Logout] 가시 | Logout 클릭 | localStorage 키 2개 삭제 + Header [Sign in/Sign up] 분기 + `/login` 이동 | 09-api-spec / contract §1 |
| AC-05 | 가입 사용자 + 페이지 새로고침 | 어느 라우트에서 F5 | App mount useEffect → loadFromStorage → localStorage 토큰 복원 → Header 로그인 상태 유지 (R-F-03 token 보유 가정. 검증은 I-09) | contract §2 |

## 2. Definition of Done (D-06)

WBS I-08 DoD Checklist 7건 매핑 — D-08-N 명명 (PR body 미체크, ADR-0046 §2.3):

- [ ] D-08-1 `pages/LoginPage.tsx` — email + password controlled inputs + submit + 422 에러 인라인
- [ ] D-08-2 `pages/RegisterPage.tsx` — username + email + password 3 필드 + 422 인라인
- [ ] D-08-3 `store/auth.ts` — I-07 시그니처 그대로 사용 (login/logout/loadFromStorage). 본 PR 무수정
- [ ] D-08-4 `api/client.ts` Authorization 헤더 자동 첨부 + 401 → logout (simple catch 패턴, 호출자 책임 — plan §5)
- [ ] D-08-5 `Header.tsx` — useAuthStore 구독 + logged-in/out 메뉴 분기
- [ ] D-08-6 한글 에러 메시지 인라인 — `extractErrorMessage` 헬퍼 + 빨강 박스 표시
- [ ] D-08-7 모바일 Chrome 깨짐 없이 렌더링 — Tailwind 기본 반응형(`max-w-sm`) + viewport meta. Manual verification 1회

## 3. 비기능 인수

- **R-N-02 (FCP)**: 본 PR은 폼 추가 — Vite HMR 영향 최소. 실 측정은 I-09 골든패스
- **R-N-04 (시크릿)**: JWT는 localStorage 평문 저장 (RealWorld spec 동일). `.env.example`·코드·로그에 평문 시크릿 노출 0
- **R-N-05 (XSS)**: React JSX escape 활용. `dangerouslySetInnerHTML` 0. backend Pydantic + RealWorld 형식 응답이라 input sanitization은 client 측 별도 불필요
- **R-N-06 (커버리지)**: backend 영향 0 → 80% 유지

## 4. 회귀 인수

- backend pytest **77 passed** 무영향 (backend 미수정)
- frontend 6 라우트 — Home/Article/Editor/Profile placeholder 무변경 (Login·Register만 실 폼)
- I-07 placeholder 시그니처(store·api) 무수정 — 외부 인터페이스 호환
- `npm run build` exit 0 — TS strict + Vite 산출 정합
- `npm run dev` ready in <500ms — HMR 무영향
