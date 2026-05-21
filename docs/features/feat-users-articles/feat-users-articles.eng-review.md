---
doc_type: feature-eng-review
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-12, R-N-01, R-N-05]
  F-ID: [F-01, F-02]
  supersedes: null
---

# feat-users-articles — Engineering Review

> P5. Generator≠Evaluator. brief + contract + plan 검토. Verdict PASS — NEEDS-WORK 0건. P6 진입 허용.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — Verdict PASS / 9 OX 모두 PASS / NEEDS-WORK 0건 |

## 0. Verdict

**PASS** — brief + contract + plan 3 산출 모두 schema validate 통과. §0 Referenced-IDs 명시. C1~C10 10 커밋 DAG가 mode=add 정합. P6 acceptance-criteria 진입 허용.

- [reviewer]: woosung.ahn@bespinglobal.com (AI — Generator≠Evaluator)
- [review_at]: 2026-05-21

## 1. Contract 검토

- **§0 Referenced-IDs 8행 명시** — R-ID 11 + F-ID 2 + UC 8 + API 8 + LLD 3 + 정책 0 + 스캐폴딩 0 + ADR 5. ADR-0018 selective read 진입점 충족
- **§2 Before/After 16행** — models/Alembic/repositories/utils/services/schemas/routers/main.py/pyproject + 단위·통합 테스트 + conftest 모두 매핑
- **§3 Call Sites 8행** — main.py/UserRepo/AuthService/require_auth/get_db/User/errors/config 모두 *변경 0건* 명시 (BC neutral)
- **§4 BC neutral** — 기존 라우트 0, 기존 schema 0, 기존 테스트 20건 PASS 유지 (3 health + 3 user_repo + 3 security + 3 jwt + 8 auth_service)
- **§5 Rollback** — PR revert + alembic downgrade 0002 + 후속 이슈 차단 검토 3단계
- **§6 비목표 7건** — comments / seed / Profile·Follow / handlers 분리 / OpenAPI 명시 검증 / E2E / slug 동시성 race

## 2. Plan 검토

- **10 커밋 DAG (C1~C10)** — feat 5 + test 3 + chore 1 + docs 1. ADR-0021 정규식 모두 통과 예정
- **critical path = C1 → C2 → C4 → C6 → C7 → C9** — 6 노드. 분기 C3·C5·C8·C10
- **§3 테스트 매핑** — 단위 13 + 통합 19+ = 32 테스트. 16 진입점 / 32 테스트 ≈ 100% > 80%
- **§4 빌드·실행 검증 5 step** — sync·alembic·ruff·pytest·import 검증
- **§5 D-01~D-08 결정 8건** — autogenerate / M2M / slug 정규화 / 빈 tagList / GET optional 인증 / 통합 fixture / 부분 갱신 / slug 카운터

## 3. UX 검토

N/A — 본 PR ui_changed=false. backend HTTP API 계층. Frontend는 Sprint 2 I-07~I-09.

## 4. 6단계 폴더링 충족

- `docs/features/feat-users-articles/` — mode=add prefix `feat-` 충족 (manifest §3.2)
- `.brief.md` + `.contract.md` + `.plan.md` + `.eng-review.md` — schema filename_pattern 충족
- 후속 산출 (`.acceptance.md`, `.risk.md`, `.code-review.md`, `.ai-qa-report.md`)도 동일 폴더에 작성 예정

## 5. frontmatter / Manifest 검증

- **doc_type 명시**: 3 산출 모두 (feature-brief / feature-contract / feature-plan)
- **version 형식**: `v0.1 (Draft)` 정합
- **status 일관**: `Draft`
- **date**: `2026-05-21` (오늘)
- **gate**: `feature` (mode=sprint 이슈 단위)
- **related.R-ID/F-ID**: 11 + 2 동일 (3 산출 일관)
- **supersedes**: null (신규)
- **validate-doc.sh 결과**: 3 산출 모두 `OK`

## 6. 발견 사항 (3축 OX)

| Q | 답 | 처리 |
| --- | --- | --- |
| Q1. comments 4 라우트가 비목표인데 14-wbs 의존성과 정합한가 | ✅ PASS | 14-wbs §3 (I-05 또는 I-06이 comments 담당). 본 PR R-ID에 R-F-09/10/11/13 미포함 일관 |
| Q2. alembic 0003 autogenerate가 동시 작업 충돌 가능성 있나 | ✅ PASS | 14-wbs §3 — I-04 단독 head 0002 → 0003. I-05·I-06이 본 PR 머지 후 0003 → 0004 진행 |
| Q3. Article M2M tag — secondary table 패턴 vs 명시적 모델 | ✅ PASS | secondary table 패턴 선택 (D-02). 본 MVP는 tag 자체 CRUD 없음 |
| Q4. require_auth가 GET /api/articles[/...]에도 적용되는가 | ✅ PASS | optional 인증 (D-05). 비회원도 조회 가능. 09-api-spec 명시 |
| Q5. ArticleService 5 메서드가 8 라우트를 모두 cover하는가 | ✅ PASS | users 3 라우트는 AuthService(I-03) 호출. articles 5 라우트는 ArticleService 5 메서드 = list/get/create/update/delete 매핑 |
| Q6. 통합 테스트 14건+ 분배 — Acceptance 충족 | ✅ PASS | test_users_routes 7+ + test_articles_routes 12+ = 19+. ≥ 14 충족 |
| Q7. R-F-12 author 필터 통합 테스트 1건 강제 | ✅ PASS | C9 test_articles_routes의 `list_with_author_filter_returns_only_authors_articles` 명시 |
| Q8. exception_handler가 RealWorldError 6 도메인 예외(I-03) 모두 cover | ✅ PASS | C7에서 `@app.exception_handler(RealWorldError)` 1개 핸들러가 status_code 속성으로 분기 — DuplicateEmail/Username/Invalid/Expired/Forbidden/NotFound 모두 422/401/403/404 매핑 |
| Q9. 컨벤션 — 한글 메시지 + ruff per-file-ignores 정합 | ✅ PASS | errors.py(N818) + deps/**(B008 S105) 기존 + routers/**(B008) 신규 = 일관 false positive 처리 |

**3축 OX 결과**: 9 PASS / 0 DEFER / 0 NEEDS-WORK. Verdict PASS.

## 7. NEEDS-WORK 항목

(없음) — 9 OX 모두 PASS. P6 acceptance-criteria 진입 허용.
