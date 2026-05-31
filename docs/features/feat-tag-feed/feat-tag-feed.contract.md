---
doc_type: feature-contract
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

# feat-tag-feed — Change Contract

> P3. mode=add. multi 2 영역(backend + frontend).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-31 | woosung.ahn@bespinglobal.com | 초안 — §0 6행 + §2 11행 + §3 4행 + BC neutral(`?author=`와 공존) + Rollback 1-commit revert |

## 0. 참조 정본 ID (Referenced-IDs)

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| SRS | (none — follow-up 신규 R-F-14, RFP §5 OoS 해제) | R-F-14 |
| PRD | `docs/planning/05-prd/05-prd.md` §3 F-02 (게시글 모듈) | F-02 |
| LLD-API | `docs/planning/09-lld-api-spec/09-lld-api-spec.md` (RealWorld spec `/api/tags` + `?tag=` follow-up) | (none) |
| Scaffolding | `docs/planning/12-scaffolding/python.md` §1 트리 — routers/tags.py + schemas/tag.py 신규 | (none) |
| 기존 패턴 | `repositories/article.py::list_with_filters` author 필터 (I-04) | (none) |
| Test Catalog | 본 PR 단위 1 + 통합 2 추가 | (none) |

## 1. 변경 의도

RFP §5 OoS였던 태그 피드 follow-up 추가. RealWorld spec 정합 — `GET /api/tags` 전체 목록 + `GET /api/articles?tag=<name>` 단일 필터. 기존 `?author=` 필터 패턴(I-04 정착) 재사용으로 모듈 분해·테스트 일관성 유지.

## 2. Before / After

| 항목 | Before | After |
| --- | --- | --- |
| `backend/realworld/routers/tags.py` | 없음 | 신규 — `APIRouter(prefix="/api/tags", tags=["tags"])` + `GET /` 단일 라우트 (auth optional) |
| `backend/realworld/schemas/tag.py` | 없음 | 신규 — `TagsListResponse { tags: list[str] }` |
| `backend/realworld/repositories/article.py::list_with_filters` | `author: str | None` 인자 | + `tag: str | None` 인자. tag 시 JOIN article_tags + tags + WHERE tags.name = tag |
| `backend/realworld/repositories/article.py` | 6 메서드 | + `list_all_tag_names() -> list[str]` (Tag.name distinct, ORDER BY name) |
| `backend/realworld/services/article.py::list` | `(*, limit, offset, author)` | + `tag: str | None = None` 인자 |
| `backend/realworld/routers/articles.py::list_articles` | `author: str | None = None` 쿼리 | + `tag: str | None = None` 쿼리 |
| `backend/realworld/main.py` | 3 라우터 (users/articles/comments) | + `tags_router` 1줄 |
| `backend/tests/integration/test_tags_routes.py` | 없음 | 신규 — `test_list_returns_tags` (seed 5종) |
| `backend/tests/integration/test_articles_routes.py` | 13 케이스 | + `test_list_with_tag_filter` (jane:python·bob:react 글 2건 후 ?tag=python → 1건) |
| `backend/tests/unit/test_article_service.py` | 8 케이스 | + `test_list_with_tag_filter` |
| `frontend/src/types/api.ts` | TagsListResponse 없음 | + `TagsListResponse { tags: string[] }` |
| `frontend/src/pages/HomePage.tsx` | 페이지네이션 + 카드 목록 | + 상단 태그 칩 영역 (apiFetch `/tags` mount 1회) + 선택 state `selectedTag` + `?tag=` 쿼리 + 선택 해제 버튼 |

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| `ArticleRepo.list_with_filters` 호출자 | author 인자만 사용 중 | tag 인자는 default None — 기존 호출자 무수정 (BC neutral) |
| `ArticleService.list` 호출자 | HomePage·ProfilePage 모두 author 인자만 | 동일 — tag default None |
| `routers/articles.py::list_articles` 쿼리 파라미터 | author 단독 또는 부재 | tag 쿼리 추가 — 동시 사용 가능 (`?author=jane&tag=python`) |
| `main.py::create_app` | 3 라우터 등록 | + tags_router 1줄 |

## 4. Backward Compatibility

**BC neutral** — 모든 변경이 추가만(인자 default None / 라우트 신규 / 쿼리 파라미터 신규):
- 기존 `?author=` 단독 호출 동작 무변경
- 기존 단위 8 + 통합 12 (articles) + 7 (users) + 11 (comments) = 77 passed 회귀 0
- 기존 frontend HomePage 페이지네이션 동작 무변경 (tag state 미선택 시 기존 동작)

## 5. Rollback 전략

**1-commit revert로 충분** — squash merge 단일 commit. 신규 파일 4(tags router·schema + test) + 기존 파일 5(article repo/service/router/main + types/HomePage) 자동 revert. DB·alembic 영향 0 (스키마 무수정).

## 6. 비목표

- **`/api/articles/feed` follow 피드**: out of scope — F-FOLLOW Issue #26 별도
- **태그 자동완성·검색**: out of scope
- **태그 카운트(글 수) 표시**: out of scope
- **다중 태그 필터(`?tag=python,fastapi`)**: out of scope — 단일 태그만
- **태그 페이지네이션**: out of scope (5종 단일 GET)
