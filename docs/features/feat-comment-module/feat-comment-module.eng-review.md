---
doc_type: feature-eng-review
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

# feat-comment-module — Engineering Review

> P5 plan-eng-review. contract + plan 자기검토(Generator) — 6 OX. PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — PASS, 6 OX 모두 PASS, NEEDS-WORK 0. Article 5층 패턴 mirroring 정합 |

## 0. Verdict

**PASS** — contract §0 7행·§2 11행 Before/After + plan 4 commit DAG 모두 ADR-0021 통과. P8 implement 진입 허용.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (self-review, generator)
- [review_at]: 2026-05-21

## 1. Contract 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| §0 Referenced-IDs 7행 채움 (ADR-0018 BLOCK) | ✅ | SRS §6.1·§6.4·§6.6 / PRD §3 F-03 / 09-api-spec §3 240-331줄 / 08-module / 12-scaffolding §1 / 13/02-catalog §2.3 |
| §1 변경 의도 명확 | ✅ | 4 라우트 + CASCADE + Sprint 2 backend 완료 95→100%. R-F-13 비표준 결정 근거(04-srs §6.6) 인용 |
| §2 Before/After 11행 (Article·Alembic·repo·service·schema·router·main·errors·단위·통합·CASCADE) | ✅ | 신규 파일 8 + 수정 3 + 신규 통합 테스트 1건 |
| §3 Call Sites 4행 (main 등록 / ArticleService 의존 / require_auth / conftest) | ✅ | 기존 패턴 재사용 명시 |
| §4 BC neutral | ✅ | 신규 모듈만 추가, 기존 API/DB/Alembic chain 무수정 |
| §5 Rollback 2-commit revert | ✅ | git revert + alembic downgrade 0003 두 단계로 충분 |

## 2. Plan 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| §1 4 commit DAG (C1 모델+Alembic → C2 repo·service·schema → C3 router·통합 → C4 docs) | ✅ | 모든 커밋 메시지 ADR-0021 정규식 통과 (`feat(backend)` 3 + `docs(plan)` 1) |
| §2 의존성 그래프 — 순환 없음 + C1→C2→C3→C4 선형 | ✅ | 1인 작업 순차 진행 가능 |
| §3 테스트 매핑 — 단위 10건+ + 통합 12건+ + CASCADE 1건 | ✅ | service 4 메서드 × happy/failure 평균 2.5 시나리오 = 10 / 라우트 4 × happy/failure 평균 3 = 12 |
| §4 빌드·실행 검증 5단계 (alembic·ruff·pytest·uvicorn·seed) | ✅ | I-04·I-05 패턴 재사용. 53 → 약 66 passed 예상 |
| §5 점진 합의 4건 명시 (의존성 방향·body validation·CASCADE 검증·인덱스) | ✅ | 후속 ADR 불필요. code-review 인라인 메모로 충분 |

## 3. UX 검토

mode=add backend-only — UX 검토 N/A. 09-api-spec §3 JSON contract만 정합 확인.

## 4. 6단계 폴더링 충족

본 PR 산출 위치:
- `docs/features/feat-comment-module/feat-comment-module.{brief,contract,plan,eng-review,acceptance,risk,code-review,ai-qa-report}.md` — `feat-` 접두(mode=add) + 평면 명명 ✅ (document-manifest §3.2)
- 코드: `backend/realworld/{models,repositories,services,schemas,routers}/comment.py` + `alembic/versions/0004_comments.py` + `tests/unit/test_comment_service.py` + `tests/integration/test_comments_routes.py` — Article 모듈 패턴 정합

## 5. frontmatter / Manifest 검증

- brief: `doc_type=feature-brief`, R-ID 5, F-ID 1 ✅
- contract: `doc_type=feature-contract`, §0 BLOCK 통과 ✅
- plan: `doc_type=feature-plan`, §1·§2·§3·§4·§5 BLOCK 통과 ✅
- eng-review (본 문서): `doc_type=feature-eng-review`, R-ID 5 ✅
- 모든 산출 date=2026-05-21 / author=woosung.ahn@bespinglobal.com 정합

## 6. 발견 사항 (3축 OX)

ADR-0008 in_scope / blocks_merge / same_area 3축:

| Q | 답 | 처리 |
| --- | --- | --- |
| F1: CommentService가 ArticleService에 직접 의존하는 방향이 services/ 레이어 간 결합 증가시키는가? | ⭕ in_scope / ❌ no blocks_merge / ⭕ same_area | INFO 처리. ArticleService.get_by_slug는 NotFound + 한글 메시지 정합으로 *재사용이 단순함*. ArticleRepo 직접 의존하면 NotFound 중복 raise 발생 |
| F2: Comment의 author relationship lazy="joined" 대 selectinload 선택 — N+1 위험? | ⭕ / ❌ / ⭕ | INFO. 댓글 목록 한 게시글 평균 5~10건이므로 joined lazy로 단일 JOIN sufficient. selectinload는 article tags(M2M)처럼 다수 row일 때만 필요 |
| F3: PUT comment 비표준 R-F-13 — RealWorld spec 비포함이라 frontend 호환 영향? | ⭕ / ❌ / ⭕ | INFO. 04-srs §6.6 사용자 결정 + 09-api-spec §3 명세 완료. frontend는 본 프로젝트 자체 구현(I-09)이므로 외부 RealWorld FE 클라이언트 호환 N/A |
| F4: alembic 0004 — comments 테이블 인덱스 (article_id, author_id) 둘 다 필요한가? | ⭕ / ❌ / ⭕ | article_id만 인덱스. list_by_article 쿼리가 article_id로 filter. author_id는 hard delete 시 FK CASCADE만 사용되므로 인덱스 불필요 (Article과 동일 패턴) |
| F5: CASCADE 검증을 직접 raw SQL select count로 강제하지 않는 선택 | ⭕ / ❌ / ⭕ | API 호출 후 GET comments→404 + 새 article 생성 후 비어있음 확인으로 충분. 시간 절약 + 가독성 |
| F6: 통합 테스트 12건 estimate — 실제 시간 1.5h fit? | ⭕ / ❌ / ⭕ | I-04 통합 19건이 ~1h. comments 4 라우트는 article 5보다 단순(slug nested, 같은 fixture 재사용). 시간 박스 fit |

NEEDS-WORK 0건. blocks_merge=yes 0건.

## 7. NEEDS-WORK 항목

(없음) — 6 OX 모두 PASS. P6 acceptance 진입 허용.
