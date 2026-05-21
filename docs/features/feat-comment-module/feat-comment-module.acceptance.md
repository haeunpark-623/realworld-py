---
doc_type: feature-acceptance
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-08, R-F-09, R-F-10, R-F-11, R-F-13]
  F-ID: [F-03]
  supersedes: null
---

# feat-comment-module — Acceptance Criteria

> P6. Given/When/Then 6건 + DoD 8건 (14-wbs Issue #6 mapping).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 6 AC + 8 DoD (D-06-1~8) |

## 1. 인수 기준 (Given/When/Then)

| ID | Given | When | Then | 출처 |
| --- | --- | --- | --- | --- |
| AC-01 | backend 부팅 + 가입 사용자 jane이 작성한 article slug=`my-post` 존재 | jane 토큰으로 `POST /api/articles/my-post/comments` `{"comment":{"body":"good post"}}` | 201 Created + `{"comment":{"id":N, "body":"good post", "createdAt":..., "updatedAt":..., "author":{"username":"jane","bio":null,"image":null}}}` (R-F-09) | 09-api-spec §3 264 |
| AC-02 | jane이 my-post에 댓글 2건 작성한 상태 | `GET /api/articles/my-post/comments` (인증 무관) | 200 OK + `{"comments":[{...},{...}]}` 최신순 정렬 (R-F-10) | 09-api-spec §3 240 |
| AC-03 | jane이 작성한 댓글 id=12 + bob 토큰 보유 | bob 토큰으로 `PUT /api/articles/my-post/comments/12` `{"comment":{"body":"hacked"}}` | 403 Forbidden + `{"errors":{"body":["권한이 없습니다"]}}` (R-F-13) | 09-api-spec §3 287 |
| AC-04 | jane이 자기 댓글 id=12 + jane 토큰 보유 | jane 토큰으로 `PUT /api/articles/my-post/comments/12` `{"comment":{"body":"수정된 댓글"}}` | 200 OK + `{"comment":{"id":12,"body":"수정된 댓글","updatedAt":...}}` (R-F-13) | 09-api-spec §3 287 |
| AC-05 | jane이 자기 댓글 id=12 + jane 토큰 보유 | jane 토큰으로 `DELETE /api/articles/my-post/comments/12` | 204 No Content + 후속 GET comments 시 해당 댓글 부재 (R-F-11) | 09-api-spec §3 311 |
| AC-06 | jane이 my-post에 댓글 2건 작성한 상태 | jane 토큰으로 `DELETE /api/articles/my-post` | 204 No Content + 후속 `GET /api/articles/my-post/comments` 시 404 ("게시글을 찾을 수 없습니다") + 새 article 생성 후 GET 시 빈 배열 — CASCADE 동작 (R-F-08) | contract §1 / 09-api-spec §3 |

## 2. Definition of Done (D-06)

WBS I-06 DoD Checklist 8건 매핑 (PR body 미체크 상태로 등록 — ADR-0046 §2.3):

- [ ] D-06-1 `models/comment.py` — Comment class with `article_id FK ondelete=CASCADE` + `author_id FK ondelete=CASCADE` + body/created_at/updated_at + author relationship lazy="joined"
- [ ] D-06-2 `alembic revision --autogenerate -m "comments"` 또는 수동 작성 → `0004_comments.py` (revision="0004", down_revision="0003")
- [ ] D-06-3 `repositories/comment.py` — CommentRepo with add/list_by_article/get_by_id/delete + selectinload(Comment.author) on list
- [ ] D-06-4 `services/comment.py` — CommentService 4 메서드 (create/list_by_article/update/delete) + 작성자 검증 + ArticleService.get_by_slug 위임
- [ ] D-06-5 `schemas/comment.py` — CommentCreatePayload/UpdatePayload/Request/Response/ListResponse with body min_length=1
- [ ] D-06-6 `routers/comments.py` — 4 라우트 (GET·POST·PUT·DELETE `/api/articles/{slug}/comments[/{id}]`) + R-F-13 PUT 비표준 포함 + require_auth on POST/PUT/DELETE
- [ ] D-06-7 단위 테스트 — `test_comment_service.py` 10건+ (service 4 메서드 × happy/failure 평균 2.5)
- [ ] D-06-8 통합 테스트 — `test_comments_routes.py` 12건+ + `test_articles_routes.py::test_delete_cascades_comments` CASCADE 검증 1건

## 3. 비기능 인수

- **R-N-01 영향**: 댓글 4 라우트 신규지만 list_by_article은 한 article의 댓글만 반환(평균 5~10건). p95 < 200ms 회귀 없음 — I-05 측정 결과 4.24ms 마진 ~47배로 충분
- **R-N-04 (시크릿)**: 신규 환경변수 0 — 위반 0건
- **R-N-05 (XSS/SQLi)**: SQLAlchemy ORM + Pydantic 입력 검증 + JSONResponse escape — 위반 0건
- **R-N-06 (커버리지)**: Service·Router 신규 코드 100% 커버 (단위 10 + 통합 12 = 22건). 전체 80% 임계 유지

## 4. 회귀 인수

- 기존 53 passed 전부 통과 — 12 articles + 7 users + 1 performance + 31 unit + 3 health
- `uv run alembic upgrade head` → 0001 → 0002 → 0003 → **0004** 선형 진행
- `uv run python -m scripts.seed_articles` → `users=10 articles=100 tags=5` 무변경 (Comment 시드 추가 안 함)
- `uv run uvicorn realworld.main:app` 부팅 + `GET /docs`에서 comments 4 라우트 노출
- ruff check + ruff format --check → All checks passed!
