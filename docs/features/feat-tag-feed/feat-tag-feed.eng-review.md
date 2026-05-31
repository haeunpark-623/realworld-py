---
doc_type: feature-eng-review
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

# feat-tag-feed — Engineering Review

> P5. PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-31 | woosung.ahn@bespinglobal.com | 초안 — PASS |

## 0. Verdict

**PASS** — contract §0 6행·§2 11행 + plan 4 commit DAG. P8 진입 허용.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (self-review)
- [review_at]: 2026-05-31

## 1. Contract 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| §0 Referenced-IDs 6행 | ✅ | R-F-14 follow-up / F-02 / 09-api-spec follow-up / 12-scaffolding / 기존 author 패턴 / test catalog |
| §1 변경 의도 | ✅ | RealWorld spec 정합 + 기존 ?author= 패턴 재사용 |
| §2 Before/After 11행 | ✅ | backend 7 + frontend 2 + 테스트 3 |
| §3 Call Sites 4행 | ✅ | repo·service·router·main 모두 BC neutral 명시 |
| §4 BC neutral | ✅ | default None 인자 추가만 |
| §5 Rollback 1-commit revert | ✅ | DB 무수정 |

## 2. Plan 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| §1 4 commit DAG | ✅ | C1 backend tags → C2 backend filter → C3 frontend → C4 docs |
| §2 의존성 그래프 | ✅ | C1·C2 독립, C3 두 backend 의존 |
| §3 테스트 매핑 — 단위 1 + 통합 2 | ✅ | service + tags 라우트 + articles ?tag= |
| §4 빌드·실행 검증 | ✅ | pytest + npm + curl + 수동 |
| §5 점진 합의 5건 | ✅ | schema 별도·UI 위치·state 로컬·정렬·URL encode |

## 3. UX 검토

- 10-lld-screen-design §1.1 헤더 일관성 — 본 PR 헤더 무수정. HomePage 상단 태그 영역 추가
- §3.3 Spacing — `gap-2`·`p-1`·`p-4` Tailwind utility 활용
- §3.4 Component primitives — Tag 칩은 이미 ArticleCard에서 사용 중. 패턴 재사용
- 선택 상태 시각 표현 — `bg-blue-600 text-white` (selected) vs `border` (default)

## 4. 6단계 폴더링 충족

- `docs/features/feat-tag-feed/*.md` — feat- 접두 (mode=add)
- branch: `feat/tag-feed-issue-25` ADR-0044 정합

## 5. frontmatter / Manifest 검증

- 8 산출 R-F-14 + F-02 / date / author 정합

## 6. 발견 사항 (3축 OX)

| Q | 답 | 처리 |
| --- | --- | --- |
| F1: R-F-14 신규 R-ID — 04-srs 무수정 | ⭕ in_scope / ❌ no / ⭕ same_area | follow-up 사이클이라 SRS 무수정 acceptable. feat docs에만 trace |
| F2: list_all_tag_names ORDER BY name | ⭕ / ❌ / ⭕ | 의도 — UI 알파벳 정렬 |
| F3: HomePage 로컬 state — URL 동기 안 함 | ⭕ / ❌ / ⭕ | 의도 plan §5 (3). 새로고침 시 필터 손실은 trade-off |
| F4: schemas/tag.py 별도 vs article.py 추가 | ⭕ / ❌ / ⭕ | 의도 plan §5 (1) |
| F5: tag 1개 단독 필터만 | ⭕ / ❌ / ⭕ | 의도. 다중 태그는 follow-up |
| F6: 빈 칩 영역(tags=0) — empty state? | ⭕ / ❌ / ⭕ | 의도 — seed 100건이라 5종 보장. tags=[] 시 칩 영역 미노출 (`tags.length > 0` 조건부) |

NEEDS-WORK 0건.

## 7. NEEDS-WORK 항목

(없음)
