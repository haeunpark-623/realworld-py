---
doc_type: feature-contract
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

# feat-board-ui — Change Contract

> P3 (ADR-0018). mode=add — I-07/I-08 위에 게시판 6 화면 + 댓글 UI + 3 컴포넌트 + 골든패스.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — §0 6행 + §2 11행 Before/After + §3 Call Sites 5행 + BC neutral + Rollback 1-commit revert |

## 0. 참조 정본 ID (Referenced-IDs)

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| SRS | `docs/planning/04-srs/04-srs.md` §6.1 R-F-04~F-13 (게시글 4종 + 댓글 4종 + 내 글) + §6.2 R-N-02 FCP + §6.2 R-N-05 XSS | R-F-04~R-F-13, R-N-02, R-N-05 |
| PRD | `docs/planning/05-prd/05-prd.md` §3 F-02·F-03·F-04 | F-02, F-03, F-04 |
| LLD-Screen | `docs/planning/10-lld-screen-design/10-lld-screen-design.md` §2 S-01·S-02·S-03·S-06 + §3 디자인 토큰 + §4 a11y | (none) |
| LLD-API | `docs/planning/09-lld-api-spec/09-lld-api-spec.md` §3 articles 5종(R-F-04~R-F-08) + comments 4종(R-F-09~R-F-11·R-F-13) | (none) |
| Scaffolding | `docs/planning/12-scaffolding/python.md` §1 frontend 트리 components 5종 placeholder → 3종 실 도입 | (none) |
| Test Catalog | N/A — WBS I-09 DoD 단위/통합 N/A. E2E 골든패스로 갈음 | (none) |

## 1. 변경 의도

I-08 인증 완료 위에 게시판 6 화면 실 구현 + 댓글 UI 통합 + 3 컴포넌트(ArticleCard·CommentItem·Modal) + 골든패스 7단계 + R-N-02 FCP + R-N-05 XSS 시도. Sprint 2 핵심 마일스톤 — 14-wbs §6.1 Day 2 시간 박스 5h 할당 (effort 2d ≈ 2.5-3.5h 실 작업).

**P2 컷 후보 명시** (14-wbs §0.3·§6.1): (a) R-F-12 ProfilePage / (b) R-F-13 댓글 수정 UI / (c) 골든패스 7→5 압축. Day 2 시점별 컷 결정.

## 2. Before / After

| 항목 | Before (I-08) | After (I-09) |
| --- | --- | --- |
| `frontend/src/pages/HomePage.tsx` | placeholder | 실 구현 — `apiFetch<ArticlesListResponse>('/articles?limit=20&offset=N')` + ArticleCard 그리드 (gap-4) + 페이지네이션 (`< 1 [2] 3 4 5 >` 형식, articlesCount/limit) + loading 스피너 + empty "게시글 없음" + error 재시도 버튼 |
| `frontend/src/pages/ArticlePage.tsx` | placeholder + slug | 실 구현 — Promise.all([article, comments]) 병렬 로드. 본문(`<article>` semantic) + 작성자 메타 + (작성자 본인) [수정][삭제] 버튼 + Modal 확인. 댓글 영역: 목록 (CommentItem) + (로그인) 댓글 작성 폼 + (작성자) 인라인 편집(R-F-13 P2 컷 후보) + 삭제 |
| `frontend/src/pages/EditorPage.tsx` | placeholder + mode | 실 구현 — useParams slug 유무로 mode 분기. 새 글: 빈 폼 → POST. 수정: GET → 폼 채움 → PUT. controlled inputs (title/description/body textarea/tagList 쉼표 split). 422 catch + extractErrorMessage 인라인 (I-08 패턴). 성공 시 navigate(`/article/${slug}`) |
| `frontend/src/pages/ProfilePage.tsx` | placeholder + username | 실 구현(가벼움, P2 컷 후보) — `apiFetch<ArticlesListResponse>('/articles?author={username}')` + ArticleCard 그리드. 빈 결과 시 "작성한 글이 없습니다" |
| `frontend/src/components/ArticleCard.tsx` | (없음) | 신규 — props: `article: ArticleView`. Link to=`/article/${slug}`. Tailwind: border + p-4 + hover shadow. 표시: author/createdAt 메타 → h2 title → description → tagList 칩 |
| `frontend/src/components/CommentItem.tsx` | (없음) | 신규 — props: `comment + currentUser + onDelete + onEdit`. 인라인 편집 상태: editing 토글 (R-F-13 P2 컷 후보, FE는 시간 박스로 결정. 본 PR은 placeholder 토글로 일단 추가) |
| `frontend/src/components/Modal.tsx` | (없음) | 신규 — props: `open/title/message/onConfirm/onCancel`. 오버레이 + ESC 닫기 + focus trap (간단). 디자인 토큰 §3.1 danger 색상 |
| `frontend/src/api/client.ts` | I-08 ApiError | 무수정 — token 옵션 활용 |
| `frontend/src/types/api.ts` | I-08 ErrorBody | 무수정 — 모든 타입 정의됨 |
| backend 영향 | 무수정 | 무수정 ✅ — Issue #4·#6 라우트 그대로 호출 |

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| `HomePage → apiFetch<ArticlesListResponse>('/articles')` | I-08 시그니처 그대로 | 무수정 |
| `ArticlePage → Promise.all([apiFetch<ArticleResponse>, apiFetch<CommentsListResponse>])` | 병렬 호출 패턴 | 본 PR 첫 사용 — error 처리는 호출자 catch |
| `EditorPage → apiFetch<ArticleResponse>(method=POST or PUT, token from useAuthStore)` | 인증 필요 라우트 | useAuthStore.getState().token으로 token 전달 |
| `CommentItem → apiFetch(method=PUT or DELETE, token)` | 댓글 수정/삭제 | 동일 패턴 |
| Header (I-08) → user 상태 분기 | 무수정 (I-08 구현) | I-09에서 Header 자체는 무수정 |

## 4. Backward Compatibility

**BC neutral** — frontend 4 페이지 placeholder *대체* + 3 신규 컴포넌트만. 외부 인터페이스(store/api/types) 무수정. backend 영향 0.

- I-08 ApiError·useAuthStore·apiFetch 시그니처 그대로 사용
- backend pytest 77 passed 회귀 N/A (backend 미수정)
- backend-ci `paths: backend/**` 한정 — frontend 변경에 미트리거

## 5. Rollback 전략

**1-commit revert로 충분** — squash merge 단일 commit. 4 페이지 + 3 신규 컴포넌트 = 7개 파일 자동 revert. 부수 영향 0.

- 데이터 영속성: localStorage 무수정. backend DB 무수정
- backend pytest 회귀 N/A

리스크 등급 Low — risk.md 4건 F-RISK 모두 Low.

## 6. 비목표

- **마크다운 렌더링**: out of scope — `<pre>` 또는 plain `<p>` 본문 (`@tailwindcss/typography` 미도입)
- **이미지 업로드**: out of scope (RFP)
- **태그 페이지/필터**: out of scope
- **무한 스크롤**: out of scope (limit/offset)
- **검색·즐겨찾기·팔로우**: out of scope (RFP)
- **Button·Input 컴포넌트 추출**: out of scope — 페이지 내 Tailwind utility 직접
- **댓글 페이지네이션**: out of scope (10-lld-screen-design §5 Open Q 3)
- **모바일 햄버거 메뉴**: out of scope (10-lld-screen-design §5 Open Q 1)
- **단위/통합 테스트**: WBS DoD N/A. E2E 골든패스로 갈음
