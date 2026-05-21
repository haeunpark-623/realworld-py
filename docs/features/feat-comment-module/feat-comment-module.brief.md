---
doc_type: feature-brief
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

# feat-comment-module — Feature Brief

> Sprint 2 첫 이슈 (I-06). RealWorld API의 댓글 4 라우트 + Article 삭제 시 CASCADE 검증. Article 모듈 5층 구조(model→repo→service→router→schema)를 mirroring.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — mode=add 자동 결정. 5층 mirroring + Alembic 0004 + CASCADE 검증 + 4 라우트 nested |

## 1. 한 줄 의도

`POST/GET/PUT/DELETE /api/articles/{slug}/comments`(4 라우트, R-F-13 PUT 비표준 포함)를 추가하고 `DELETE /api/articles/{slug}`가 관련 댓글을 CASCADE 삭제함을 검증한다.

## 2. 사용자 가치

- **가입 사용자**: 게시글에 댓글을 작성/수정/삭제할 수 있어 토론·피드백 흐름이 가능 (RealWorld 핵심 UX의 절반)
- **비회원 방문자**: 댓글 목록 조회는 인증 없이 가능 — 게시글 가치 판단 시 댓글이 신호로 작동
- **시스템 안정성**: 게시글 hard delete 시 댓글 고아 row 0건 — DB 무결성 보장 (R-F-08 정합)

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 | 변경 후 |
| --- | --- | --- |
| Comment 모델 | 없음 | `models/comment.py` — id/body/author_id(FK CASCADE users)/article_id(FK CASCADE articles)/created_at/updated_at |
| Alembic 마이그레이션 | 0003 (articles+tags) | 0004 (comments) |
| Repository | `repositories/{user,article}.py` 2 종 | + `repositories/comment.py` (CRUD + by_article 조회) |
| Service | `services/{auth,article}.py` 2 종 | + `services/comment.py` 4 메서드(create/list_by_article/update/delete + 작성자 검증) |
| Schema | `schemas/{user,article}.py` 2 종 | + `schemas/comment.py` (CreateRequest/UpdateRequest/View/Response/ListResponse) |
| Router | `users.py` + `articles.py` 2 종 | + `routers/comments.py` 4 라우트 nested |
| main.py | 2 라우터 등록 | 3 라우터 등록 (comments_router 추가) |
| 단위 테스트 | 6 파일 (auth/article/jwt/security/slug/user_repo) | + `test_comment_service.py` 4 메서드 × happy/failure 8건+ |
| 통합 테스트 | 3 파일 (articles/users/performance) | + `test_comments_routes.py` 4 라우트 + `test_articles_routes.py::test_delete_cascades_comments` 1건 추가 |
| pytest 합계 | 53 passed | 약 65+ passed (단위 +8, 통합 +5 추정) |
| Article 모델 | 무변경 | 무변경 ✅ (CASCADE는 Comment 측 FK ondelete=CASCADE로 자동) |

## 4. 모드 자동 감지 결과

**mode = add** (자동 결정, ADR-0032 규칙 4).

- 부정 시그널 0건: `type:bug` 라벨 없음 / UI·design 키워드 없음 / 기존 동작 변경 없음
- 긍정 시그널: `type:feature` 라벨 + 신규 모델·라우터·테스트 추가
- 자동 결정 trace: Issue #6 labels = [status:todo, priority:P0, type:feature, area:backend] → 규칙 4 발동 → add 조용히 진행

## 5. 영향 범위

**touched_areas**: 1 영역 (backend) — Touched Areas 표 PR body 등록 N/A (단일 영역).

- `backend/realworld/models/` — `comment.py` 신규 + `__init__.py` Comment export 추가
- `backend/realworld/repositories/comment.py` — 신규
- `backend/realworld/services/comment.py` — 신규
- `backend/realworld/schemas/comment.py` — 신규
- `backend/realworld/routers/comments.py` — 신규
- `backend/realworld/main.py` — comments_router import + include_router 1줄 추가
- `backend/alembic/versions/0004_comments.py` — 신규
- `backend/tests/unit/test_comment_service.py` — 신규
- `backend/tests/integration/test_comments_routes.py` — 신규
- `backend/tests/integration/test_articles_routes.py` — `test_delete_cascades_comments` 1건 추가
- `docs/planning/12-scaffolding/python.md` — §1 트리 갱신 (P13)
- `docs/planning/14-wbs/14-wbs.md` — I-06 status:in-review 전이 (P13)
- `docs/planning/INDEX.md` — v0.9 → v0.10 (P13)

## 6. 비목표

- **댓글 nested reply / threaded 댓글**: out of scope (RealWorld spec 비포함, 04-srs §6)
- **댓글 좋아요·신고**: out of scope (P2 컷 후보 아님 — 사용자 의도 외)
- **댓글 페이지네이션**: out of scope — 한 게시글의 댓글은 전체 반환 (RealWorld spec 동작)
- **soft delete**: out of scope — hard delete + CASCADE (R-F-08 정합)
- **댓글 작성자 외 프로필 정보 embed**: bio/image는 ProfileEmbed에 null로 채움 (Article과 동일)

## 7. Open Questions

(없음) — 09-api-spec §3 4 라우트 spec 명세 완료. RealWorld spec PUT comment 비표준 R-F-13은 04-srs §6.6에서 사용자 결정 완료. 의문점 0건.
