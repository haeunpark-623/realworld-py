---
doc_type: feature-contract
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-N-05, R-N-06]
  F-ID: []
  supersedes: null
---

# feat-closing-cycle — Change Contract

> P3. mode=add. 사이클 종료 PR — docs only.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — §0 5행 + §2 5행 + §3 2행 + BC neutral + Rollback 1-commit revert |

## 0. 참조 정본 ID (Referenced-IDs)

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| SRS | `docs/planning/04-srs/04-srs.md` §6.2 R-N-05 (XSS/SQLi 차단) + R-N-06 (커버리지 ≥80%) | R-N-05, R-N-06 |
| PRD | (none) — 본 PR은 신규 기능 0 | (none) |
| WBS | `docs/planning/14-wbs/14-wbs.md` §2 I-10 DoD 9건 | (none) |
| ADR | `adr/0040-local-md-onboarding-guide.md` (LOCAL.md 양축) + `adr/0046-pr-checkboxes-block-and-status-check.md` | (none) |
| Test Catalog | I-04 pytest --cov-fail-under=80 정착 (R-N-06) | (none) |

## 1. 변경 의도

본 사이클(2일 ~16h) 종료 docs PR. 코드 변경 0 — README.md + CHANGELOG.md + retro 회고 + 보안 점검 결과 명시 + 회귀 77 passed 확인 + main squash merge로 사이클 동결.

## 2. Before / After

| 항목 | Before | After |
| --- | --- | --- |
| `README.md` | 없음 | 신규 — 프로젝트 의도 + 기술 스택 + LOCAL.md 링크 + Sprint 1·2 5+5 = 10 이슈 완료 명시 + 라이선스 (학습 과제 무관) |
| `CHANGELOG.md` | 없음 | 신규 — Keep a Changelog 형식. ## [0.1.0] - 2026-05-21 (sprint 완주) ### Added (backend·frontend·infra·docs) 카테고리 |
| `docs/planning/retro/2026-05-21-cycle.md` | 없음 | 신규 — 5+5+5 형식 (잘된 점·개선점·메모) |
| `docs/features/feat-closing-cycle/` | 없음 | 신규 — feature 8 산출 |
| `docs/planning/14-wbs/14-wbs.md` | v0.12 | v0.13 (I-10 in-review + 사이클 종료 명시) |
| `docs/planning/INDEX.md` | v0.13 | v0.14 (Sprint 1·2 5+5/5 머지 + 마지막 PR 머지 대기) |

backend/frontend 영향: 0.

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| GitHub repo 루트 보기 | README.md 노출 | 사용자가 직접 진입 시 LOCAL.md로 위임 |
| CI 워크플로 | `paths: backend/**` 한정 → docs 변경 미트리거 | 무수정 |

## 4. Backward Compatibility

**BC neutral** — 코드 영향 0. README.md + CHANGELOG.md 신규는 외부 사용자 진입점 *추가*만. 기존 LOCAL.md 본문·docs/planning/ 산출·코드 모두 무수정.

- backend pytest **77 passed** 회귀 안정
- frontend `npm run build` 60 modules — 변경 0
- CI green

## 5. Rollback 전략

**1-commit revert로 충분** — squash merge 단일 commit. README.md + CHANGELOG.md + retro/* 자동 revert. 사이클 종료 자체는 git history로 영구 보존.

## 6. 비목표

- **CI badges**: out of scope (학습 컨텍스트, badge 추가는 후속 학습)
- **외부 배포(GitHub Pages, Docker Hub, npm publish)**: out of scope (RFP §5)
- **국제화 README (영문)**: out of scope — 한국어만
- **자동 changelog 도구(conventional-commits-changelog 등)**: out of scope — 수동 작성