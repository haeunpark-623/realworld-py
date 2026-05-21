---
doc_type: feature-brief
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

# feat-board-ui — Feature Brief

> Sprint 2 핵심 마일스톤 (I-09, effort 2d). S-01 HomePage + S-02 ArticlePage + S-03 EditorPage + S-06 ProfilePage 실 구현 + 댓글 UI(작성/수정/삭제) + ArticleCard·CommentItem·Modal 컴포넌트 + 골든패스 7단계 + FCP/XSS 측정. backend Issue #4·#6 라우트와 end-to-end 연결.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — mode=add. 6 화면 실 동작 + 3 components + 골든패스 + FCP/XSS. ProfilePage·댓글 수정 UI는 P2 컷 후보(14-wbs §0.3) |

## 1. 한 줄 의도

I-08 인증 완료 위에 게시판 6 화면(S-01·S-02·S-03·S-06 + 기존 I-07 Login/Register)을 실 구현하고, 댓글 작성·목록·수정·삭제 UI를 ArticlePage 안에 인라인 구현. backend Issue #4 articles 라우트 5종 + Issue #6 comments 4종을 호출. gstack `/qa` 7단계 골든패스 + R-N-02 FCP < 1500ms + R-N-05 XSS payload 시도로 비기능 검증.

## 2. 사용자 가치

- **비회원**: `/` 진입 → 게시글 카드 목록 + 페이지네이션 → 카드 클릭 → 본문 + 댓글 조회 (R-F-04·R-F-05·R-F-10). 가입 유도 배너는 P2 컷 (10-lld-screen-design §5 Open Q 2)
- **가입 사용자**: 글 작성(`/editor`) + 수정(`/editor/:slug`) + 삭제 + 댓글 작성/수정/삭제 + 내 글 목록(`/profile/{username}`) (R-F-06·R-F-07·R-F-08·R-F-09·R-F-11·R-F-12·R-F-13)
- **시스템**: FCP < 1500ms (R-N-02) + XSS 차단 (R-N-05) — 학습 컨텍스트 비기능 정량 검증

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 (I-08) | 변경 후 (I-09) |
| --- | --- | --- |
| `pages/HomePage.tsx` | placeholder text | 실 구현 — `GET /api/articles?limit=20&offset=N` 호출 + ArticleCard 그리드 + 페이지네이션 (limit/offset) + loading·empty·error 상태 |
| `pages/ArticlePage.tsx` | placeholder + slug 표시 | 실 구현 — `GET /api/articles/{slug}` + `GET /api/articles/{slug}/comments` 병렬 호출. 본문 렌더링 + CommentItem 목록 + (로그인 시) 댓글 작성 폼 + 작성자 본인 시 [수정][삭제] 버튼 + Modal 확인 |
| `pages/EditorPage.tsx` | placeholder + mode 표시 | 실 구현 — useParams slug 유무로 mode 분기. 새 글: POST /api/articles. 수정: GET → form 채움 → PUT. 422 시 인라인 에러 (I-08 패턴 reuse) |
| `pages/ProfilePage.tsx` | placeholder + username | 실 구현(가벼움) — `GET /api/articles?author={username}` + ArticleCard 그리드 (R-F-12, P2 컷 후보 — 시간 박스로 결정) |
| `components/ArticleCard.tsx` | (없음) | 신규 — author/title/description/createdAt/tagList 카드 형식. 클릭 시 `/article/{slug}` 이동 |
| `components/CommentItem.tsx` | (없음) | 신규 — body + author + createdAt + (작성자 본인) [수정][삭제] + 인라인 편집 토글 (R-F-13 P2 컷 후보) |
| `components/Modal.tsx` | (없음) | 신규 — 삭제 확인 모달. props: `open`/`title`/`onConfirm`/`onCancel`. ESC + 오버레이 클릭 닫기 |
| `api/client.ts` | I-08 simple catch | 무수정 — apiFetch token 옵션 활용 (Authorization 헤더 자동 첨부) |
| `types/api.ts` | I-08 ErrorBody 추가 | 무수정 — 이미 모든 RealWorld spec 타입 정의됨 |
| 골든패스 E2E | 0건 | gstack `/qa` 7단계 + 스크린샷 7장 |
| FCP / XSS | 미측정 | FCP < 1500ms 측정 + XSS payload 시도 |

## 4. 모드 자동 감지 결과

**mode = add** (자동 결정, ADR-0032 규칙 4). 부정 시그널 0건 — 6 placeholder 채움 + 3 신규 컴포넌트.

라벨: type:feature + area:frontend.

## 5. 영향 범위

**touched_areas**: 1 영역 (frontend).

- `frontend/src/pages/{HomePage,ArticlePage,EditorPage,ProfilePage}.tsx` — 실 구현
- `frontend/src/components/{ArticleCard,CommentItem,Modal}.tsx` — 신규
- backend 영향: 0 (Issue #4·#6 라우트 무수정 호출)
- `docs/planning/12-scaffolding/python.md` — §1 트리 components 5종 → 3종 실 도입 표기 (P13)
- `docs/planning/14-wbs/14-wbs.md` v0.11 → v0.12 (P13)
- `docs/planning/INDEX.md` v0.12 → v0.13 (P13)

## 6. 비목표

- **댓글 페이지네이션**: out of scope (10-lld-screen-design §5 Open Q 3, 한 글당 평균 0~10건 가정)
- **마크다운 렌더링**: out of scope — `<pre>` 또는 plain `<p>` 본문 표시. `@tailwindcss/typography` preset 미도입 (I-07 plan §5)
- **이미지 업로드**: out of scope (RFP)
- **태그 페이지(`/tag/:name`) 또는 태그 필터링**: out of scope
- **무한 스크롤**: out of scope — limit/offset 페이지네이션
- **검색**: out of scope
- **즐겨찾기/팔로우**: out of scope (RFP)
- **Button·Input 컴포넌트 추출**: out of scope — 3 컴포넌트(ArticleCard·CommentItem·Modal)만 추출. Button·Input은 페이지 내 Tailwind utility 직접
- **단위/통합 테스트**: WBS DoD N/A 명시. E2E는 골든패스로 갈음

## 7. Open Questions

- **R-F-12 ProfilePage**: P2 컷 후보. 시간 박스로 결정 — 본 PR은 가벼운 구현(GET /api/articles?author= + ArticleCard 재사용). 컷 결정 시점 Day 2 14:00 (14-wbs §6.1)
- **댓글 수정 UI (R-F-13의 FE)**: P2 컷 후보. CommentItem 안 인라인 편집 토글. 컷 결정 시점 Day 2 16:00
- **골든패스 7→5 단계 압축**: 시간 박스에 따라 (가입→로그인→글 작성→댓글 작성→글 삭제) 5단계 가능. 컷 결정 시점 Day 2 17:00
