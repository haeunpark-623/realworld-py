---
doc_type: feature-acceptance
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-09, R-F-10, R-F-11, R-F-12, R-F-13, R-N-02, R-N-05]
  F-ID: [F-02, F-03, F-04]
  supersedes: null
---

# feat-board-ui — Acceptance Criteria

> P6. WBS I-09 DoD 9건 + 골든패스 7단계 + FCP + XSS.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 7 AC + 9 DoD (D-09-1~9) |

## 1. 인수 기준 (Given/When/Then)

| ID | Given | When | Then | 출처 |
| --- | --- | --- | --- | --- |
| AC-01 | seed 100건 + `/` 진입 | 페이지 로드 | 최신순 카드 20개 + 페이지네이션(`< 1 [2] 3 4 5 >`) + ArticleCard별 title/description/author/createdAt/tagList 표시 (R-F-04) | WBS I-09 AC |
| AC-02 | ArticleCard 클릭 → S-02 진입 | 페이지 로드 | 본문 + 작성자 메타 + 댓글 목록 + (비로그인 시 댓글 폼 미노출) (R-F-05·R-F-10) | WBS / 10-lld §2 |
| AC-03 | 로그인 + 작성자 본인 글 S-02 | [수정] 클릭 | `/editor/{slug}` 이동 + 폼 채움 + 수정 후 PUT → `/article/{slug}` (R-F-07) | 10-lld §2 |
| AC-04 | 로그인 + 작성자 본인 글 S-02 | [삭제] 클릭 → Modal 확인 | 204 + `/` 이동 + 카드 목록에서 제거 (R-F-08) | WBS / 10-lld §2 |
| AC-05 | 로그인 + ArticlePage | 댓글 작성 폼 submit | 201 + 새 댓글 목록 상단 표시 (R-F-09). 댓글 작성자 본인 [수정][삭제] 노출 (R-F-11·R-F-13) | 10-lld §2 |
| AC-06 | 골든패스 7단계 | gstack `/qa` 실행 (또는 수동) | 가입→로그인→글 작성→댓글 작성→댓글 수정→글 수정→글 삭제 모두 PASS + 스크린샷 7장 `docs/features/feat-board-ui/screenshots/` 저장 (UC-01 골든패스) | WBS I-09 AC |
| AC-07 | 비로그인 + `/article/{slug}` | 댓글 영역 확인 | 댓글 목록만 표시 + 댓글 작성 폼 미노출 (R-F-09 인증 필수) | 10-lld §2 |

## 2. Definition of Done (D-06)

WBS I-09 DoD 9건 매핑 — D-09-N 명명:

- [ ] D-09-1 `pages/HomePage.tsx` — 게시글 카드 목록 + 페이지네이션 + loading/empty/error 상태
- [ ] D-09-2 `pages/ArticlePage.tsx` — 본문 + 댓글 영역 + 작성자만 [수정][삭제]
- [ ] D-09-3 `pages/EditorPage.tsx` — 새 글(`/editor`) + 수정(`/editor/:slug`) 같은 컴포넌트
- [ ] D-09-4 `pages/ProfilePage.tsx` — 본인/타인 글 목록 (R-F-12, P2 컷 후보 — 시간 박스로 결정 가능)
- [ ] D-09-5 `components/ArticleCard.tsx`, `CommentItem.tsx`, `Modal.tsx` 신규
- [ ] D-09-6 댓글 인라인 편집 폼 — `CommentItem.tsx` editing state 토글 (R-F-13 P2 컷 후보)
- [ ] D-09-7 골든패스 7단계 gstack `/qa` 실행 + 스크린샷 `docs/features/feat-board-ui/screenshots/` 저장
- [ ] D-09-8 FCP 측정 (R-N-02) — Chrome DevTools Performance 트레이스 1회, `< 1500ms` 확인
- [ ] D-09-9 XSS payload 1회 시도 (R-N-05) — `<script>alert(1)</script>` 본문 작성 후 ArticlePage에서 alert 미발화 확인

## 3. 비기능 인수

- **R-N-02 (FCP)**: Chrome DevTools Performance 트레이스 < 1500ms. AI 자동 N/A → Manual verification
- **R-N-05 (XSS)**: React JSX 자동 escape. `<script>` 본문은 텍스트 노드로 렌더링 → 미발화. Manual verification에서 시도 확인
- **R-N-01 (API p95)**: I-05 측정 PASS 유지 (backend 무수정)
- **R-N-04 (시크릿)**: localStorage JWT 평문 — I-08 정착 + RealWorld spec 동일. 본 PR 무영향
- **R-N-06 (커버리지)**: backend 80% 유지 (backend 미수정)

## 4. 회귀 인수

- backend pytest 77 passed 무영향 (backend 미수정)
- frontend 6 라우트 placeholder → 4 화면 실 동작 + I-08 Login/Register 무수정
- I-07 store/auth.ts·api/client.ts·types/api.ts 시그니처 그대로
- `npm run build` 통과 (70+ modules 예상)
- backend dev 8000 + frontend dev 5173 동시 부팅 회귀 N/A
