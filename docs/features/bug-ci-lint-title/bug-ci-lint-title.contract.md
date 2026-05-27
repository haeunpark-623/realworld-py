---
doc_type: feature-contract
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

# bug-ci-lint-title — Change Contract

> P3. mode=bug. workflow YAML 1줄 추가.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-27 | woosung.ahn@bespinglobal.com | 초안 — §0 4행 + §2 1행 + §3 2행 + BC neutral + Rollback 1-commit revert |

## 0. 참조 정본 ID (Referenced-IDs)

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| ADR | `policies/github-issue.md` §1.5 + ADR-0021 (제목 정규식) | (none) |
| Workflow | `.github/workflows/issue-pr-title-lint.yml` (현 파일) | (none) |
| GitHub CLI | gh CLI 공식 — `GH_REPO` env 자동 인식 | (none) |
| Test Catalog | N/A — workflow YAML 1줄 변경 | (none) |

## 1. 변경 의도

PR #22 (Issue #21) 검증 중 발견된 workflow 버그 — `gh pr comment` 호출 시 git context 없어 모호 에러 발생. **`GH_REPO: ${{ github.repository }}` env 1줄 추가**로 gh CLI가 자동 repo 인식 → 정확한 BLOCK 사유 메시지 + PR 본문 코멘트 정상 게시.

## 2. Before / After

| 항목 | Before | After |
| --- | --- | --- |
| `.github/workflows/issue-pr-title-lint.yml` lint-title job env | `TITLE`·`KIND`·`NUMBER`·`GH_TOKEN` 4개 | + `GH_REPO: ${{ github.repository }}` 1줄 추가 (총 5개) |

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| GitHub Actions runner — `gh pr comment` / `gh issue comment` | git context 자동 인식 | env 1줄 추가만으로 자동 동작 |
| ADR-0021 정규식 자체 | 무수정 | (none) |

## 4. Backward Compatibility

**BC neutral** — workflow trigger·정규식·step 구조 모두 무수정. env 1줄 추가만. 정상 제목 PASS 동작 무변경.

## 5. Rollback 전략

**1-commit revert로 충분** — env 1줄 제거.

## 6. 비목표

- **actions/checkout step 추가**: out of scope — GH_REPO env가 더 가벼움
- **regex 수정**: out of scope — ADR-0021 정본 유지
- **에러 코멘트 본문 폼 개선**: out of scope — 현 메시지 유지
