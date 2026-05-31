---
doc_type: feature-brief
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

# feat-tag-feed — Feature Brief

> Issue #25 — follow-up 신규 기능. RFP §5 OoS 해제 결정. RealWorld spec 태그 피드 — `GET /api/tags` + `?tag=` 필터.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-31 | woosung.ahn@bespinglobal.com | 초안 — mode=add. backend 라우트·필터 + frontend HomePage 칩 UI |

## 1. 한 줄 의도

backend에 `GET /api/tags` 라우트 신설 + `GET /api/articles?tag=<name>` 필터 추가하고, frontend HomePage에 태그 칩 UI 도입해 사용자가 클릭으로 태그 필터링 가능하도록 한다.

## 2. 사용자 가치

- **모든 사용자**: 관심 태그(python·fastapi·react 등) 클릭으로 글 필터링 → RealWorld spec의 핵심 탐색 UX
- **개발자**: 기존 `?author=` 필터 패턴(I-04 정착) 재사용 — 모듈 분해·테스트 패턴 일관성 학습

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 | 변경 후 |
| --- | --- | --- |
| `GET /api/tags` 라우트 | 없음 | 신규 — RealWorld spec: `{"tags": ["python", "fastapi", "react", "sqlalchemy", "realworld"]}` |
| `GET /api/articles?tag=` | 없음 | `?author=`와 동시 또는 단독 사용 가능. JOIN articles ↔ article_tags ↔ tags |
| `routers/tags.py` | 없음 | 신규 — 단일 라우트 |
| `repositories/article.py` | author 필터만 | + `list_all_tag_names()` + tag 인자 추가된 `list_with_filters` |
| `services/article.py` | list(author=...) | list(author=..., tag=...) |
| `schemas/tag.py` | 없음 | 신규 — `TagsListResponse { tags: list[str] }` |
| `frontend/types/api.ts` | I-08 정착 | + `TagsListResponse` 타입 |
| `frontend/pages/HomePage.tsx` | 페이지네이션 + 카드 목록 | + 태그 칩 UI (상단 sidebar 또는 헤더 영역) + 선택 상태 |
| 단위 테스트 | 31 | + 1 (test_article_service.py::test_list_with_tag_filter) |
| 통합 테스트 | 32 | + 2 (test_tags_routes.py 1건 + test_articles_routes.py::test_list_with_tag_filter) |
| pytest 합계 | 77 | 약 80 passed |

## 4. 모드 자동 감지 결과

**mode = add** (자동, ADR-0032 규칙 4). type:feature.

## 5. 영향 범위

**touched_areas**: 2 영역 (backend + frontend) — Touched Areas 표 N/A (3+ 영역 임계 미달).

- backend: `routers/tags.py` 신규 / `routers/articles.py` 수정 / `services/article.py` 수정 / `repositories/article.py` 수정 / `schemas/tag.py` 신규 / `main.py` 라우터 등록 / `tests/integration/test_tags_routes.py` 신규 / `tests/integration/test_articles_routes.py` 1 추가 / `tests/unit/test_article_service.py` 1 추가
- frontend: `types/api.ts` 1 타입 / `pages/HomePage.tsx` 태그 UI

## 6. 비목표

- **`/api/articles/feed` (사용자별 follow 피드)**: out of scope — F-FOLLOW (Issue #26) 별도
- **tag 자동완성**: out of scope — 칩 클릭만
- **태그별 URL `/tag/:name`**: out of scope — HomePage state로 충분
- **빈 tag DB**: out of scope — seed 5종 있음
- **태그 페이지네이션**: out of scope — 5종이라 단일 GET 충분
- **태그 카운트(글 수)**: out of scope — 단순 이름 목록만

## 7. Open Questions

(없음) — RealWorld spec 그대로 따름
