---
doc_type: feature-plan
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

# feat-board-ui — Implementation Plan

> P4 (ADR-0018). 6 commit DAG: C1 components → C2 HomePage → C3 ArticlePage → C4 EditorPage → C5 ProfilePage → C6 docs.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 6 commit DAG + ADR-0021 통과 + 빌드·골든패스 시도 5단계 + 점진 합의 5건 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `feat(frontend): I-09 ArticleCard·CommentItem·Modal 컴포넌트 (#9)` | `components/ArticleCard.tsx` + `CommentItem.tsx` + `Modal.tsx` 신규 | (없음 — WBS DoD N/A) | 0 — 신규만 |
| C2 | `feat(frontend): I-09 HomePage 목록 + 페이지네이션 + 4 상태 (#9)` | `pages/HomePage.tsx` | (없음) | 0 |
| C3 | `feat(frontend): I-09 ArticlePage 본문 + 댓글 UI + 작성자 액션 + 삭제 모달 (#9)` | `pages/ArticlePage.tsx` | (없음) | 0 |
| C4 | `feat(frontend): I-09 EditorPage 새 글/수정 + 422 인라인 (#9)` | `pages/EditorPage.tsx` | (없음) | 0 |
| C5 | `feat(frontend): I-09 ProfilePage author 필터 글 목록 (#9)` | `pages/ProfilePage.tsx` (P2 컷 후보 — 시간 박스로 결정) | (없음) | 0 |
| C6 | `docs(plan): feat-board-ui 8 산출 + 12-scaffolding v0.9 + 14-wbs v0.12 + INDEX v0.13 (#9)` | feature docs 8 + 12-scaffolding + 14-wbs + INDEX | (없음) | 0 |

ADR-0021 통과: feat(frontend) 5 + docs(plan) 1.

## 2. 의존성 그래프

```
C1 (components) ─→ C2 (HomePage) ──┐
                                   ├─→ C3 (ArticlePage) ──┐
                                   │                       ├─→ C6 (docs)
                                   │                       │
                                   └─→ C4 (EditorPage) ────┤
                                                           │
                                            C5 (ProfilePage)
```

- **C1 → C2,C3,C5**: ArticleCard·CommentItem·Modal이 HomePage/ArticlePage/ProfilePage에 import
- **C3 → C4**: ArticlePage 수정/삭제 액션이 EditorPage에 link. EditorPage 수정 mode는 ArticlePage 데이터 흐름 후
- **C5 시간 박스**: Day 2 14:00 결정 — 컷 결정 시 C5 skip + commit 메시지에 "P2 컷" 표기

순환 없음.

## 3. 테스트 매핑

WBS I-09 DoD에 단위/통합 N/A. E2E 골든패스로 갈음:

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C1 | (없음 — tsc strict) | `npm run build` 통과 |
| C2 | (없음 — 수동 브라우저) | `/` 진입 → seed 100건 상태에서 카드 20개 + 페이지네이션 5 페이지 + 클릭 시 ArticlePage 이동 (R-F-04) |
| C3 | (없음 — 수동) | `/article/{slug}` → 본문 + 댓글 + (로그인 시) 댓글 작성 폼 + (작성자 본인 시) [수정][삭제]. 댓글 작성/삭제 동작. 삭제 모달 ESC + 확인 (R-F-05·R-F-08·R-F-09·R-F-10·R-F-11) |
| C4 | (없음 — 수동) | `/editor` 새 글: title+description+body+tagList → POST → `/article/{slug}` 이동. `/editor/{slug}` 수정: 폼 채움 → PUT → `/article/{slug}` (R-F-06·R-F-07) |
| C5 | (없음 — 수동) | `/profile/{username}` → 해당 사용자 글만 (R-F-12, P2 컷 후보) |
| C6 | (validate-doc.sh) | 모든 산출 schema PASS |

> backend 회귀: N/A (미수정). pytest 77 passed 유지.

## 4. 빌드·실행 검증 단계

```bash
# 1) frontend 빌드
cd frontend && npm run build
# expect: 70+ modules + dist/ 생성 + 에러 0

# 2) backend + frontend 동시 부팅
# 터미널 1
cd backend && uv run alembic upgrade head && uv run uvicorn realworld.main:app --port 8000

# 터미널 2
cd frontend && npm run dev

# 3) seed (100건 게시글)
# 터미널 3
cd backend && uv run python -m scripts.seed_articles
# expect: users=10 articles=100 tags=5

# 4) 브라우저 골든패스 7단계 (gstack /qa 시도 또는 수동)
# (1) /register → 가입 → Header 전환
# (2) (이미 로그인 상태)
# (3) /editor → 새 글 작성 → /article/{slug} 이동
# (4) ArticlePage → 댓글 작성 → 새 댓글 표시
# (5) CommentItem [수정] → body 수정 → 저장 (R-F-13 P2 컷 후보)
# (6) ArticlePage [수정] → /editor/{slug} → 수정 → 저장
# (7) ArticlePage [삭제] → Modal 확인 → 삭제 + / 이동

# 5) FCP 측정 (Chrome DevTools Performance)
# 6) XSS 시도: 본문에 <script>alert(1)</script> 작성 후 ArticlePage에서 alert 미발화 확인
```

## 5. 점진 합의 / 결정 발생 항목

- **(1) P2 컷 결정 시점**: Day 2 14:00 ProfilePage, 16:00 댓글 수정 UI, 17:00 골든패스 압축 (14-wbs §6.1). 컷 시 commit 메시지에 "P2 컷" 명시
- **(2) 본문 렌더링**: `<pre className="whitespace-pre-wrap">` 또는 `<p>` 단순 표시. 마크다운 lib 미도입 (학습 부담 회피)
- **(3) 페이지네이션 UI**: 단순 `< 1 2 [3] 4 5 >` 형식. 페이지 점프 미지원
- **(4) 댓글 인라인 편집**: CommentItem 내 `editing` state로 textarea 토글. R-F-13 P2 컷 후보 — 본 PR 일단 구현 후 시간 박스로 결정
- **(5) Modal focus trap**: 단순 — first focusable element에 ref autoFocus. 완전한 trap(tab cycle)은 over-engineering. ESC + 오버레이 클릭 닫기는 구현
- **(6) Promise.all 에러 처리**: ArticlePage Promise.all([article, comments])에서 한쪽 실패 시 → 404로 article은 표시, comments는 빈 배열로 fallback. error state 별 표시 불필요
