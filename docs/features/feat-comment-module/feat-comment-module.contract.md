---
doc_type: feature-contract
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

# feat-comment-module — Change Contract

> P3 (ADR-0018). §0 Referenced-IDs로 선택적 정본 진입. mode=add — Article 모듈 5층 패턴 재사용 + Alembic 0004 신규 + 4 라우트.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — §0 7행 + §2 Before/After 11행 + §3 Call Sites 4행 + BC neutral + Rollback 2-commit revert |

## 0. 참조 정본 ID (Referenced-IDs)

> 본 변경이 정본으로 따르는 04 SRS·05 PRD·09 LLD-API·08 LLD-Module·12 Scaffolding 정확한 위치 명시. 본 contract 전체 진입점.

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| SRS | `docs/planning/04-srs/04-srs.md` §6.1 (R-F-08 hard delete + CASCADE), §6.4 (R-F-09 작성), §6.4 (R-F-10 목록), §6.4 (R-F-11 삭제), §6.6 (R-F-13 수정 비표준) | R-F-08, R-F-09, R-F-10, R-F-11, R-F-13 |
| PRD | `docs/planning/05-prd/05-prd.md` §3 F-03 (댓글 모듈) | F-03 |
| LLD-API | `docs/planning/09-lld-api-spec/09-lld-api-spec.md` §3 4 라우트 (lines 240-331) | (none) |
| LLD-Module | `docs/planning/08-lld-module-spec/08-lld-module-spec.md` §1 Comment 모듈 (Article 패턴 재사용) | (none) |
| Scaffolding | `docs/planning/12-scaffolding/python.md` §1 tree (comment.py 5개 신규 + alembic 0004 추가 예정) | (none) |
| 코딩 컨벤션 | `docs/planning/11-coding-conventions/11-coding-conventions.md` (Python 명명·에러·import) | (none) |
| Test Catalog | `docs/planning/13-test-design/02-catalog.md` §2.3 R-F-09·R-F-10·R-F-11·R-F-13 | R-F-09, R-F-10, R-F-11, R-F-13 |

## 1. 변경 의도

RealWorld API 댓글 4 라우트(POST/GET/PUT/DELETE) + Article 삭제 시 댓글 CASCADE를 추가한다. 기존 Article 모듈 5층 구조를 mirroring해 *최소 침습 + 패턴 일관성* 유지. Sprint 2 첫 이슈로 backend 완성도 95% → 100%.

R-F-13 PUT comment는 RealWorld spec 비표준이지만 04-srs §6.6에서 사용자 결정으로 신설. URL은 `PUT /api/articles/{slug}/comments/{id}`.

## 2. Before / After

| 항목 | Before | After |
| --- | --- | --- |
| `backend/realworld/models/comment.py` | 없음 | 신규 — `Comment` class. id/body/author_id(FK CASCADE users)/article_id(FK CASCADE articles)/created_at/updated_at. author relationship lazy="joined" |
| `backend/realworld/models/__init__.py` | `["Article", "Base", "Tag", "User", "article_tags"]` | + `"Comment"` 추가 |
| `backend/alembic/versions/0004_comments.py` | 없음 | 신규 — revision=0004, down_revision=0003. comments 테이블 + ix_comments_article_id 인덱스 |
| `backend/realworld/repositories/comment.py` | 없음 | 신규 — `CommentRepo`. add/list_by_article/get_by_id/delete 4 메서드. selectinload(Comment.author) |
| `backend/realworld/services/comment.py` | 없음 | 신규 — `CommentService`. create/list_by_article/update/delete 4 메서드. NotFound("댓글을 찾을 수 없습니다") + Forbidden + ArticleService 의존 (slug 검증) |
| `backend/realworld/schemas/comment.py` | 없음 | 신규 — `CommentCreatePayload`/`CommentUpdatePayload`/`CommentCreateRequest`/`CommentUpdateRequest`/`CommentView`/`CommentResponse`/`CommentsListResponse`. body min_length=1 |
| `backend/realworld/routers/comments.py` | 없음 | 신규 — `APIRouter(prefix="/api/articles", tags=["comments"])`. 4 라우트 nested: GET·POST·PUT·DELETE `/{slug}/comments[/{id}]` |
| `backend/realworld/main.py` | 2 라우터 (users, articles) | + `from realworld.routers import comments as comments_router` + `app.include_router(comments_router.router)` |
| `backend/realworld/errors.py` | `NotFound("리소스를 찾을 수 없습니다")` 기본 | 무수정 — 도메인 메시지 호출부에서 `NotFound("댓글을 찾을 수 없습니다")`로 주입 |
| `backend/tests/unit/test_comment_service.py` | 없음 | 신규 — 8건+ (create happy·404 slug, list happy·404 slug, update happy·403 타인·404 id·422 빈 body, delete happy·403 타인·404 id) |
| `backend/tests/integration/test_comments_routes.py` | 없음 | 신규 — 4 라우트 × happy/failure (정상/401/403/404/422). about 12건 |
| `backend/tests/integration/test_articles_routes.py` | 12건 | + `test_delete_cascades_comments` 1건 추가 — 댓글 2건 작성 후 Article DELETE → DB 직접 조회로 comments count=0 검증 |

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| `realworld.main.create_app()` (`backend/realworld/main.py`) | 라우터 등록 추가 | comments_router import + include_router 1줄 (Article·User 등록 패턴 그대로) |
| `realworld.services.comment.CommentService` 내부 | ArticleService를 호출해 slug → article.id 변환 + 404 처리 위임 | `ArticleService.get_by_slug(slug)` 재사용 (이미 NotFound + 메시지 정합) |
| `realworld.deps.auth.require_auth` | POST/PUT/DELETE 댓글 라우트에서 FastAPI Depends | Article 라우터와 동일 패턴 |
| `tests/integration/conftest.py::integration_client` + `register_user` 헬퍼 | Comment 통합 테스트도 동일 fixture 사용 | 변경 0 — 그대로 재사용 (DI override는 in-memory aiosqlite로 격리) |

## 4. Backward Compatibility

**BC neutral** — 신규 모듈·라우트 추가만, 기존 API 무수정. 기존 12 통합 테스트 + 31 단위 테스트 + 1 성능 테스트 + 3 health = 53 passed 회귀 0건 보장.

- 기존 API 스키마: 무변경 (Article/User 스키마 import 시그니처 동일)
- 기존 DB 테이블: 무변경 (articles/users/tags/article_tags 모두 그대로. comments 신규 테이블만)
- Alembic upgrade chain: 0001 → 0002 → 0003 → **0004** (선형 head 진행)
- 기존 LOCAL.md 부팅 명령: 무수정 (alembic upgrade head가 자동으로 0004 적용)
- `.env.*.example`: 무수정 (신규 환경변수 0)

## 5. Rollback 전략

**2-commit revert로 충분**.

- 코드 revert: `git revert <PR commit>` — squash merged이므로 단일 commit 되돌리기
- DB revert (필요 시): `cd backend && uv run alembic downgrade 0003` — comments 테이블만 drop, 다른 테이블 영향 0
- 라우터 등록 1줄 revert: main.py에서 comments_router include 라인 제거 — 자동 revert 포함

리스크 등급 Low — F-RISK는 다음 risk.md에서 4건 식별 (CASCADE 미동작 / R-F-13 비표준 URL 충돌 / Comment.author 직렬화 N+1 / Article 삭제 시 트랜잭션 격리).

## 6. 비목표

- **CommentRepo 단위 테스트 별도 파일 신설**: out of scope — Service 단위 테스트가 Repo 통과 검증을 흡수 (Article 패턴 동일)
- **Comment에 대한 update 메서드의 Repo 별도 분리**: out of scope — ArticleService.update와 동일하게 Service 내부에서 mutation + flush (관성적 패턴 통일)
- **`exists_by_id` 같은 별도 lightweight 메서드**: out of scope — `get_by_id` 단일 메서드로 충분
- **Comment soft delete / archive**: out of scope (R-F-08 hard delete 정합)
