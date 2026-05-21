---
doc_type: feature-plan
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

# feat-comment-module — Implementation Plan

> P4 (ADR-0018 selective read). contract §0 7행 정본만 가벼운 읽기로 충분. 4 commit DAG: C1 모델+Alembic → C2 repo·service·schema → C3 router·main 등록·테스트 → C4 docs sync (P13).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 4 commit DAG + ADR-0021 정규식 통과 (feat/test/docs) + 빌드 검증 5단계 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `feat(backend): I-06 Comment 모델 + Alembic 0004 마이그레이션 (#6)` | `models/comment.py` 신규 / `models/__init__.py` Comment export / `alembic/versions/0004_comments.py` 신규 | (없음) — DDL만 | 0 — 신규 테이블만, 기존 테이블 무수정 |
| C2 | `feat(backend): I-06 CommentRepo + CommentService + schemas (#6)` | `repositories/comment.py` 신규 / `services/comment.py` 신규 / `schemas/comment.py` 신규 | `tests/unit/test_comment_service.py` 신규 8건+ | 0 — 신규 모듈, 기존 import 무수정 |
| C3 | `feat(backend): I-06 comments 라우터 + 통합 테스트 + CASCADE 검증 (#6)` | `routers/comments.py` 신규 / `main.py` 라우터 등록 1줄 추가 / `tests/integration/test_comments_routes.py` 신규 / `tests/integration/test_articles_routes.py::test_delete_cascades_comments` 1건 추가 | 통합 13건+ (comments 12 + cascade 1) | 0 — 기존 12 articles 테스트 무수정 (추가만) |
| C4 | `docs(plan): feat-comment-module + 14-wbs I-06 in-review (#6)` | `docs/features/feat-comment-module/*.md` 8 산출 / `12-scaffolding/python.md` 트리 / `14-wbs/14-wbs.md` v0.9 / `INDEX.md` v0.10 | (없음) | 0 — docs만 |

ADR-0021 정규식 통과 검증: `^(feat|fix|chore|test|docs|refactor|perf|style|build|ci|revert)\([a-z0-9-]+\): .+` — 모든 4 커밋 OK.

## 2. 의존성 그래프

```
C1 (Comment 모델 + Alembic) ─→ C2 (repo·service·schema + 단위)
                                    │
                                    ▼
                              C3 (router·main + 통합 + CASCADE)
                                    │
                                    ▼
                              C4 (docs sync P13)
```

- **C1 → C2**: CommentRepo가 Comment 모델 import 필요. 단위 테스트는 in-memory session에서 Base.metadata.create_all()로 테이블 생성하므로 Alembic 의존 없음
- **C2 → C3**: CommentRouter가 CommentService를 Depends로 주입. 통합 테스트도 동일 fixture(`integration_client`) 사용 — Service·Repo 완비 후 라우터
- **C3 → C4**: 코드 모두 동작 + 53 + 13 = 약 66 passed 확인 후 docs sync

순환 없음. 1인 작업 순차 진행.

## 3. 테스트 매핑

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C1 | (없음 — DDL만) | alembic upgrade head → 0004 (head) 정합 + 회귀 53 passed |
| C2 단위 | `tests/unit/test_comment_service.py` | `test_create_returns_comment` / `test_create_for_missing_article_raises_not_found` / `test_list_returns_comments` / `test_list_for_missing_article_raises_not_found` / `test_update_by_author_succeeds` / `test_update_by_other_raises_forbidden` / `test_update_missing_raises_not_found` / `test_delete_by_author_succeeds` / `test_delete_by_other_raises_forbidden` / `test_delete_missing_raises_not_found` |
| C3 통합 | `tests/integration/test_comments_routes.py` | `test_create_returns_201_with_comment` / `test_create_without_auth_returns_401` / `test_create_for_missing_article_returns_404` / `test_create_empty_body_returns_422` / `test_list_returns_comments` / `test_list_for_missing_article_returns_404` / `test_list_empty_returns_empty_array` / `test_update_by_author_succeeds` / `test_update_by_other_returns_403` / `test_delete_by_author_returns_204` / `test_delete_by_other_returns_403` / `test_delete_missing_returns_404` |
| C3 CASCADE | `tests/integration/test_articles_routes.py::test_delete_cascades_comments` 1건 추가 | 작성자가 댓글 2건 작성 후 Article DELETE → GET comments 응답이 404 또는 직접 DB session 조회로 comments count=0 검증 |

## 4. 빌드·실행 검증 단계

```bash
# 1) 마이그레이션 정합
cd backend && uv run alembic upgrade head
# expect: "Running upgrade 0003 -> 0004, comments" + 0004 (head)

# 2) Lint + 포맷
uv run ruff check . && uv run ruff format --check .
# expect: All checks passed! + N files already formatted

# 3) 전체 회귀
uv run pytest -v
# expect: 약 66 passed (53 + 13)

# 4) 부팅 검증
uv run uvicorn realworld.main:app --host 0.0.0.0 --port 8000 &
curl -s http://localhost:8000/docs | grep -q "RealWorld API"
# expect: Swagger UI에 comments 4 라우트 노출

# 5) 멱등 seed (회귀)
uv run python -m scripts.seed_articles
# expect: users=10 articles=100 tags=5 (변경 0)
```

## 5. 점진 합의 / 결정 발생 항목

- **CommentService의 `_articles: ArticleService` 의존성 방향**: ArticleService를 직접 의존하지 않고 ArticleRepo만 의존하는 방안도 고려. → 단순화 위해 ArticleService.get_by_slug 호출(이미 NotFound 처리 정합) — 후속 ADR 불필요, code-review에서 인라인 메모로 충분
- **Comment.body validation 위치**: Pydantic min_length=1로 422 처리 (Article body와 동일). Service 단까지 빈 body 도달 시는 422 우선 (Pydantic) → Service에서 별도 422 raise 불필요
- **CASCADE 검증 방식**: 통합 테스트에서 DB session 직접 조회 vs API 호출 후 404 확인. → API 호출 후 GET comments 시 article 404가 먼저 발생하므로 *delete 후 새 article 생성 → 같은 article_id 회수 가능성 0* 검증으로 충분. 별도 raw select 안 함 (시간 절약)
- **`updated_at` 인덱스**: 댓글 정렬은 created_at 최신순(09-api-spec). updated_at 인덱스 없이 default 정렬 sufficient
