---
doc_type: feature-code-review
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

# feat-board-ui — Code Review

> P9 self-review. 5 코드 커밋(C1·C2·C3·C4·C5). PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — PASS. 6 OX 모두 PASS. build 60 modules + CSS +2.83KB |

## 0. Verdict

**PASS** — 5 코드 커밋 contract §2 11행 매핑. P2 컷 후보 3종 모두 본 PR 구현(시간 박스 fit). NEEDS-WORK 0건.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (AI self-review)
- [review_at]: 2026-05-21

## 1. 컨트랙트 충실도

| Before/After | Before | After 구현 |
|---|---|---|
| ArticleCard.tsx | 없음 | C1 — props { article: ArticleView }, Link to /article/{slug}, formatDate ko-KR |
| CommentItem.tsx | 없음 | C1 — editing state 토글(R-F-13) + isAuthor 분기 + 인라인 textarea |
| Modal.tsx | 없음 | C1 — role='dialog'·aria-modal·ESC + overlay 클릭 닫기, first focus to confirm |
| HomePage.tsx | placeholder | C2 — useEffect + apiFetch + 페이지네이션(< 1 [N] >) + 4 상태(loading/error/empty/default) |
| ArticlePage.tsx | placeholder | C3 — Promise.all([article, comments]) + comments fallback 빈 배열 + 댓글 작성/수정/삭제 + 삭제 Modal + 작성자 액션 |
| EditorPage.tsx | placeholder | C4 — useParams slug → isEditMode 분기. 새 글/수정 같은 컴포넌트. 4 controlled inputs + tagList split |
| ProfilePage.tsx | placeholder | C5 — author 필터 + ArticleCard 재사용 |
| api/client.ts·store/auth.ts·types/api.ts | I-08 시그니처 | 무수정 ✅ |

contract §3 Call Sites 5 — apiFetch list/detail/comments/create/update/delete 모두 사용. useAuthStore.token 4 mutation 라우트에 전달.

contract §4 BC neutral, §5 Rollback 1-commit revert 정합.

## 2. 테스트 커버리지

WBS DoD N/A. 검증:

- **build**: 60 modules transformed in 1.14s. CSS **10.91KB gzip 2.70KB** (I-08 8.08KB → +2.83KB Tailwind utility 신규 추출 — ArticleCard·CommentItem·Modal·페이지네이션·폼)
- **TS strict**: `tsc -b` 통과
- **backend 회귀**: 미수정 → 77 passed 유지
- **수동 골든패스**: Manual verification 7단계 사람 책임 (gstack `/qa` 또는 수동 + 스크린샷)

## 3. 보안 / 시크릿

- localStorage JWT 평문(I-08 정착)
- R-N-05 XSS: React JSX 자동 escape — ArticlePage 본문은 `whitespace-pre-wrap` text node로 렌더링. `<script>` payload는 텍스트로만 표시. `dangerouslySetInnerHTML` 0
- 신규 환경변수 0
- SQLi 영향 0 (backend ORM)
- `encodeURIComponent` ProfilePage author 파라미터에 적용

## 4. 가독성 / 단순성

- HomePage 102줄 / ArticlePage 229줄(가장 큼, 댓글 UI 포함) / EditorPage 163줄 / ProfilePage 51줄
- ArticlePage 큰 컴포넌트 — 4 callback(comment submit/update/delete + article delete) + Modal + 폼. 추출 검토 후 *단일 화면 + 단일 책임*이라 그대로 유지 (Article의 컨텍스트 모두 한 파일)
- formatDate 헬퍼 ArticleCard + ArticlePage + CommentItem 각각 정의(3중복) — DRY 위반 INFO. utils/date.ts 추출 검토 후 *3 줄 함수 + 3 케이스*라 INFO 처리
- 모든 페이지 동일 패턴: useEffect cancelled flag + setLoading + setError. AbortController 미도입(simple)

## 5. 발견 사항 (3축 OX 분류)

| 발견 | in_scope | blocks_merge | same_area | 처리 |
|---|---|---|---|---|
| F1: formatDate 헬퍼 3중복 (ArticleCard·ArticlePage·CommentItem) | ⭕ | ❌ | ⭕ | INFO. 3줄 함수라 utils/date.ts 추출 비용 더 큼. 4중복 시 재검토 |
| F2: ArticlePage 229줄 — 큰 컴포넌트 | ⭕ | ❌ | ⭕ | INFO. 단일 화면 단일 책임. 4 callback 추출은 prop drilling 비용 더 큼 |
| F3: Promise.all comments catch → 빈 배열 fallback — 사용자에게 "댓글 없음"으로만 보임 | ⭕ | ❌ | ⭕ | 의도. plan §5 (6) + risk F-RISK-03 |
| F4: useEffect cancelled flag — AbortController 미도입 | ⭕ | ❌ | ⭕ | 의도. simple — fetch 자체 abort는 학습 컨텍스트 over-engineering |
| F5: 페이지네이션 점프 미지원 (5 페이지 가정) | ⭕ | ❌ | ⭕ | 의도. 100건/20 = 5 페이지 충분 |
| F6: Modal focus trap simple (first focus만, tab cycle 미구현) | ⭕ | ❌ | ⭕ | 의도. plan §5 (5) + risk F-RISK-04 |

NEEDS-WORK 0건.

## 6. NEEDS-WORK 항목

(없음) — 6 OX 모두 PASS.
