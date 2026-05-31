---
doc_type: feature-acceptance
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-31
gate: feature
related:
  R-ID: [R-F-14]
  F-ID: [F-02]
  supersedes: null
---

# feat-tag-feed — Acceptance Criteria

> P6. 5 AC + 6 DoD.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-31 | woosung.ahn@bespinglobal.com | 초안 |

## 1. 인수 기준 (Given/When/Then)

| ID | Given | When | Then | 출처 |
| --- | --- | --- | --- | --- |
| AC-01 | backend 부팅 + seed 100건 (Tag 5종) | `curl GET /api/tags` | 200 + `{"tags": ["fastapi", "python", "react", "realworld", "sqlalchemy"]}` 정렬 (RealWorld spec) | contract §1 |
| AC-02 | jane:python 글 + bob:react 글 작성된 상태 | `GET /api/articles?tag=python` | 200 + articlesCount=1 + articles[0].tagList includes "python" | contract §2 |
| AC-03 | 동일 상태 | `GET /api/articles?author=jane&tag=python` | 200 + articlesCount=1 (jane이 작성한 python 글) — author+tag 동시 필터 | contract §3 |
| AC-04 | HomePage 진입 + seed 상태 | 페이지 로드 | h1 아래 태그 칩 5개 노출 (알파벳 순) + 기본 전체 글 목록 표시 | brief §3 |
| AC-05 | HomePage 태그 칩 'python' 클릭 | state 갱신 + 재조회 | 카드 목록이 python 태그 글만으로 갱신 + 페이지네이션 재계산 + 선택 칩 시각 강조 + 해제 버튼 노출 → 클릭 시 전체 복귀 | brief §3 |

## 2. Definition of Done (D-06)

D-25-1~6 (6건):

- [ ] D-25-1 backend `routers/tags.py` 신규 + `main.py` 라우터 등록
- [ ] D-25-2 backend `schemas/tag.py` 신규 `TagsListResponse`
- [ ] D-25-3 backend `repositories/article.py` `list_all_tag_names()` + `list_with_filters` tag 인자
- [ ] D-25-4 backend `services/article.py::list` + `routers/articles.py::list_articles` tag 쿼리
- [ ] D-25-5 backend 단위 1 + 통합 2 신규 = pytest 약 80 passed
- [ ] D-25-6 frontend `types/api.ts` TagsListResponse + `pages/HomePage.tsx` 태그 칩 UI

## 3. 비기능 인수

- **R-N-01 (API p95)**: tag 필터는 article_tags 인덱스 활용 — 100건 seed에서 영향 minimal. I-05 p95=4.24ms 마진 ~47배 유지
- **R-N-05 (XSS)**: tag name은 backend Tag 모델 입력 — Pydantic + ORM 차단. frontend는 React JSX escape
- **R-N-06 (커버리지)**: backend service·repo 신규 코드 100% cover

## 4. 회귀 인수

- backend pytest 77 → 약 80 passed (회귀 0)
- 기존 `?author=` 필터 단독 호출 무변경
- HomePage 페이지네이션 + 4 상태 무변경 (태그 미선택 시 기존 동작)
- frontend build TS strict 통과
