---
doc_type: feature-brief
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

# bug-ci-lint-title — Feature Brief

> Issue #23 follow-up. PR #22 검증 중 발견된 워크플로 infra 버그 — `gh pr comment`가 git context 없이 실행되어 모호한 에러 메시지 노출.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-27 | woosung.ahn@bespinglobal.com | 초안 — mode=bug. workflow YAML 1 파일 1줄 추가 |

## 1. 한 줄 의도

`.github/workflows/issue-pr-title-lint.yml`의 `lint-title` job에 `GH_REPO: ${{ github.repository }}` env 변수 1줄 추가로 gh CLI가 자동으로 repo context를 인식 → 제목 regex 미일치 시 정확한 사유 메시지 + PR/issue 자동 코멘트 정상 게시.

## 2. 사용자 가치

- **개발자(나)**: 제목 형식 오류 시 모호한 "not a git repository" 대신 *정확한 BLOCK 사유* + PR 본문 자동 코멘트로 원인·예시 제공
- **후속 사이클 사용자**: 동일 workflow를 도입한 다른 newProject에서도 깔끔한 UX

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 (PR #22에서 발현) | 변경 후 |
| --- | --- | --- |
| `gh pr/issue comment` 실행 | git context 없음 → `fatal: not a git repository` 모호 에러 → PR 코멘트 미게시 | `GH_REPO=owner/repo` env로 명시적 repo 지정 → comment 정상 게시 |
| 에러 메시지 | "Process completed with exit code 1" + git 에러만 | `::error::제목 형식 BLOCK — 위 코멘트 참조` + 본문 코멘트로 예시 표시 |
| 사용자 trace 시간 | 모호 에러 → workflow YAML 읽기 + 디버깅 (5-10분) | 즉시 PR 코멘트로 원인·예시 인지 (10초) |

## 4. 모드 자동 감지 결과

**mode = bug** — type:bug 라벨 + workflow 실제 버그 (PR #22에서 재현).

## 5. 영향 범위

**touched_areas**: 1 영역 (infra).

- `.github/workflows/issue-pr-title-lint.yml` — env에 `GH_REPO` 1줄 추가
- backend·frontend 영향: 0
- 다른 워크플로(`backend-ci.yml`·`sync-issue-labels.yml`) 영향: 0

## 6. 비목표

- **actions/checkout 추가**: out of scope — `GH_REPO` env 1줄이 더 가벼움 (checkout 1-2초 절약)
- **regex 변경**: out of scope — ADR-0021 정본 그대로 (feat|fix|chore|docs|test|refactor)
- **다른 워크플로 audit**: out of scope — 본 PR은 lint-title만

## 7. Open Questions

- **GH_REPO vs actions/checkout 선택 이유**: gh CLI 공식 문서가 `GH_REPO` env 자동 인식 명시 — actions/checkout보다 가볍고 명시적. 단점 0 (workflow runner는 GitHub Actions 환경 내라 인증 자동 처리)
