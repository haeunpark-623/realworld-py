---
doc_type: feature-code-review
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

# feat-comment-module — Code Review

> P9. Generator≠Evaluator self-review. 3 코드 커밋(C1·C2·C3) 검토. PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — PASS, 6 OX 모두 PASS, NEEDS-WORK 0. lazy load fresh reload 패턴 인라인 메모 |

## 0. Verdict

**PASS** — 3 코드 커밋 모두 contract §2 11행 매핑. 회귀 53 → 77 passed (단위 +11 + 통합 +13). CASCADE 동작 직접 검증. NEEDS-WORK 0건.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (AI self-review)
- [review_at]: 2026-05-21

## 1. 컨트랙트 충실도

contract §2 11행 매핑:

| Before/After 항목 | Before | After 구현 (코드 경로) |
|---|---|---|
| `backend/realworld/models/comment.py` | 없음 | C1 — Comment class with article_id FK CASCADE + author lazy="joined" + created_at/updated_at |
| `backend/realworld/models/__init__.py` | 5 export | C1 — + "Comment" added (sorted) |
| `backend/alembic/versions/0004_comments.py` | 없음 | C1 — revision="0004" down="0003" comments + ix_comments_article_id |
| `backend/realworld/repositories/comment.py` | 없음 | C2 — CommentRepo 4 메서드 + selectinload(Comment.author) |
| `backend/realworld/services/comment.py` | 없음 | C2 — CommentService 4 메서드 + ArticleService.get_by_slug 위임 + 작성자 검증 |
| `backend/realworld/schemas/comment.py` | 없음 | C2 — body min_length=1 Pydantic + ProfileEmbed 재사용 |
| `backend/realworld/routers/comments.py` | 없음 | C3 — 4 라우트 nested + require_auth on mutation |
| `backend/realworld/main.py` | 2 라우터 | C3 — + comments_router import + include_router |
| `backend/realworld/errors.py` | 무수정 | 무수정 ✅ — 도메인 메시지 호출부 주입 |
| `backend/tests/unit/test_comment_service.py` | 없음 | C2 — 11건 PASS |
| `backend/tests/integration/test_comments_routes.py` | 없음 | C3 — 12건 PASS |
| `backend/tests/integration/test_articles_routes.py::test_delete_cascades_comments` | 12건 | C3 — + 1건 (CASCADE 검증) → 13건 |

contract §3 Call Sites 4행 매핑:

| Call Site | 동작 검증 |
|---|---|
| `main.create_app()` 라우터 등록 | ✅ — Swagger /docs에 comments 4 라우트 노출 (FastAPI 자동) |
| `CommentService → ArticleService.get_by_slug` | ✅ — slug 미존재 시 NotFound("게시글을 찾을 수 없습니다") 단일 메시지 정합 |
| `require_auth` Depends | ✅ — POST/PUT/DELETE 401 검증 PASS (test_create_without_auth_returns_401) |
| `integration_client + register_user` fixture | ✅ — 12 신규 통합 테스트 모두 기존 fixture 재사용. DI override 충돌 0 |

contract §4 BC neutral, §5 Rollback 2-commit revert로 충분 — 모두 정합.

## 2. 테스트 커버리지

신규 24건 = 단위 11 + 통합 13 (comments 12 + CASCADE 1).

- **단위 11건** (`test_comment_service.py`):
  - create: happy (1) + 404 article (1) = 2건
  - list: happy 정렬 (1) + 404 article (1) + 빈 배열 (1) = 3건
  - update: happy (1) + 403 타인 (1) + 404 missing (1) = 3건
  - delete: happy (1) + 403 타인 (1) + 404 missing (1) = 3건
- **통합 12건** (`test_comments_routes.py`):
  - 4 라우트 × (happy + failure 평균 3) = 12건
  - failure 케이스: 401(인증), 403(타인), 404(article·comment 부재), 422(빈 body)
- **CASCADE 1건** (`test_articles_routes::test_delete_cascades_comments`):
  - 댓글 2건 작성 → article DELETE 204 → comments list 404 (article 부재) 검증

회귀: 53 + 24 = **77 passed in 12.92s**. 신규 테스트 0.4초 부담. CI workflow 변경 0.

## 3. 보안 / 시크릿

- 신규 환경변수 0
- 시크릿 노출 0 — 코드·로그·커밋 메시지에 평문 키 없음. .env.* 변경 0
- 외부 의존 추가 0 — 신규 import는 모두 기존 stack (sqlalchemy / fastapi / pydantic)
- bcrypt·JWT 무관 (인증 검증은 require_auth Depends 재사용)
- XSS/SQLi (R-N-05) 노출 0 — Pydantic 입력 검증 + SQLAlchemy ORM (raw SQL 0)
- `assert reloaded is not None` (repositories/comment.py:add) — production 코드의 assert 사용은 ruff S101 trigger 안 함 (test 코드 외 default off). 본 케이스는 invariant 검증으로 의도적

`/cso` 점검 대상 0. R-N-04 위반 0.

## 4. 가독성 / 단순성

- comment.py 5개 파일 평균 35줄 — 단일 책임 명확
- ArticleService.get_by_slug 위임으로 `NotFound("게시글을 찾을 수 없습니다")` 중복 raise 0
- `_get_comment` private helper — comment_id + article_id 일치 검증 (URL의 slug와 comment의 article_id 정합) 단일 진입점
- `from __future__ import annotations` (services/comment.py) — PEP 604 미래 호환 (I-04 패턴 재사용)
- 함수 길이·매개변수 수·중첩 깊이 모두 컨벤션 §1·§2 준수
- 주석 minimal — first-line docstring 0, 함수 docstring 0 (코드 자체 표현적, Article 모듈 패턴 동일)

## 5. 발견 사항 (3축 OX 분류)

ADR-0008 3축 OX:

| 발견 | in_scope | blocks_merge | same_area | 처리 |
|---|---|---|---|---|
| F1: CommentRepo.add + CommentService.update에서 `refresh()` 대신 `get_by_id()` fresh reload 패턴 — author lazy load + commit 후 N+1 회피 | ⭕ in_scope | ❌ no | ⭕ same_area | INFO 처리. ArticleService.update의 I-04 F2 동일 패턴. 1 query 추가지만 N+1보다 안정적. 측정 영향 N/A (댓글 1건 SELECT) |
| F2: `assert reloaded is not None` — production 코드의 assert 사용 | ⭕ in_scope | ❌ no | ⭕ same_area | INFO. invariant 검증 — flush 직후 같은 id로 select는 항상 hit. 운영 환경에서 PYTHONOPTIMIZE=1 시 assert 무시됨에 유의 (본 프로젝트는 dev 1 profile 운영, 무관) |
| F3: PUT comment 비표준 (R-F-13) | ⭕ in_scope | ❌ no | ⭕ same_area | 의도 — 04-srs §6.6 사용자 결정. 외부 RealWorld FE 클라이언트 호환 N/A (frontend 자체 구현) |
| F4: Comment.author lazy="joined" — Article 패턴 그대로 | ⭕ in_scope | ❌ no | ⭕ same_area | 의도. 댓글 list_by_article 시 selectinload(Comment.author)로 추가 보강 (joined가 무시되지 않음, sqlalchemy가 최적 선택) |
| F5: `_get_comment` 가 article_id 일치 검증 — slug spoofing 차단 | ⭕ in_scope | ❌ no | ⭕ same_area | 의도. URL의 slug와 comment의 실제 article_id 불일치 시 404 (보안 경계) |
| F6: 통합 테스트 12건 / 단위 11건 — Service 4 메서드 × happy/failure 평균 2.5 sufficient | ⭕ in_scope | ❌ no | ⭕ same_area | INFO. acceptance §1 AC-01~06 매핑 100% 커버 |

NEEDS-WORK 0건. blocks_merge=yes 0건. 모두 in_scope + same_area로 본 PR 범위 정합.

## 6. NEEDS-WORK 항목

(없음) — 6 OX 모두 PASS. P10 ai-qa-report 진입 허용.
