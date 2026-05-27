---
doc_type: feature-acceptance
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

# bug-ci-lint-title — Acceptance Criteria

> P6. 3 AC + 3 DoD.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-27 | woosung.ahn@bespinglobal.com | 초안 |

## 1. 인수 기준 (Given/When/Then)

| ID | Given | When | Then | 출처 |
| --- | --- | --- | --- | --- |
| AC-01 | 본 PR 제목 `fix(ci): ...` (ADR-0021 정합) | PR open + workflow 자동 트리거 | lint-title PASS — `::notice::Title OK` 출력 + green status | contract §2 |
| AC-02 | 의도적 잘못된 제목 PR (예: `bug(...)` 또는 `update(...)` ) | workflow 트리거 | `::error::제목 형식 BLOCK` + PR 본문에 자동 코멘트 ("❌ 제목 형식이 잘못되었습니다 (ADR-0021)..." with 예시) 정상 게시 | brief §3 |
| AC-03 | issue 생성 시점 잘못된 제목 | workflow 트리거 | issue 본문에 자동 코멘트 정상 게시 | brief §3 |

## 2. Definition of Done (D-06)

D-23-1~3 (3건):

- [ ] D-23-1 `.github/workflows/issue-pr-title-lint.yml` — env에 `GH_REPO: ${{ github.repository }}` 1줄 추가
- [ ] D-23-2 본 PR 제목 `fix(ci): ...` lint-title PASS 확인 (자동)
- [ ] D-23-3 Manual verification (선택, follow-up dry-run) — 잘못된 제목 시나리오로 자동 코멘트 정상 게시 확인

## 3. 비기능 인수

- **R-N-04 (시크릿)**: 본 PR 시크릿 노출 0 — `${{ github.repository }}`는 GitHub 환경변수
- **R-N-05 (XSS)**: workflow YAML 변경, 코드 0 — XSS 영향 0

## 4. 회귀 인수

- backend pytest 77 passed 유지 (코드 무변경)
- frontend build 무영향 (코드 무변경)
- 다른 workflow(`backend-ci.yml`·`sync-issue-labels.yml`) 무영향
