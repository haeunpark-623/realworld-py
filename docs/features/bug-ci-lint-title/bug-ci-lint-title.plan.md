---
doc_type: feature-plan
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-27
gate: feature
related:
  R-ID: []
  F-ID: []
  supersedes: null
---

# bug-ci-lint-title — Implementation Plan

> P4. 단일 commit DAG. workflow YAML 1줄 추가.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-27 | woosung.ahn@bespinglobal.com | 초안 — 2 commit (fix + docs) + 재현 시나리오 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `fix(ci): issue-pr-title-lint GH_REPO env 추가 (#23)` | `.github/workflows/issue-pr-title-lint.yml` | (없음 — YAML) | 0 — env 1줄 추가 |
| C2 | `docs(plan): bug-ci-lint-title 8 산출 + INDEX v0.16 (#23)` | feature docs 8 + INDEX | (없음) | 0 |

ADR-0021 통과: fix(ci) + docs(plan).

## 2. 의존성 그래프

```
C1 (workflow fix) ─→ C2 (docs)
```

순환 0.

## 3. 테스트 매핑

WBS DoD N/A. 검증은 *워크플로 자체 실행 + 재현 시나리오*:

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C1 | (없음 — YAML) | 본 PR이 만들어진 후 lint-title workflow 자동 트리거 → 본 PR 제목 PASS → workflow PASS 확인. 추가 검증: 의도적 잘못된 제목으로 별도 dry-run 또는 follow-up 재현 (Manual) |
| C2 | (validate-doc.sh) | 8 산출 schema PASS |

> backend·frontend 회귀: N/A (코드 미수정).

## 4. 빌드·실행 검증 단계

```bash
# 1) workflow YAML lint (선택)
# (act 또는 actionlint 미설치 시 GitHub 측 자동 검증에 의존)

# 2) PR open 후 lint-title workflow 자동 실행
# expect: pass (본 PR 제목 'fix(ci): ...' regex 통과)

# 3) Manual verification (선택, 사람 책임)
# - 별도 사이드 브랜치에서 의도적 잘못된 제목으로 PR 또는 issue 생성
# - workflow가 정확한 BLOCK 사유 메시지 + 자동 코멘트 게시 확인 후 close

# 4) 회귀: backend pytest 77 passed (변경 0)
```

## 5. 점진 합의 / 결정 발생 항목

- **(1) `GH_REPO` env vs `actions/checkout`**: env 1줄이 더 가벼움 + 의도 명시적. checkout 1-2s 절약. 선택 근거: brief §7
- **(2) Manual verification 재현 시나리오 — 의도적 BLOCK 유도**: PR 머지 후 follow-up에서 1회 dry-run으로 충분. 본 PR scope out
- **(3) 다른 workflow audit**: backend-ci.yml·sync-issue-labels.yml에 동일 패턴 발현 가능성 — backend-ci는 `actions/checkout@v4` 명시되어 무관, sync-issue-labels는 별도 점검 (follow-up)
