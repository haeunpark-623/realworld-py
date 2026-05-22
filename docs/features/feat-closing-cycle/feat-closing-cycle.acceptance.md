---
doc_type: feature-acceptance
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

# feat-closing-cycle — Acceptance Criteria

> P6. WBS I-10 DoD 9건 + 3 AC.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 3 AC + 9 DoD |

## 1. 인수 기준 (Given/When/Then)

| ID | Given | When | Then | 출처 |
| --- | --- | --- | --- | --- |
| AC-01 | Sprint 1·2 commit history (PR #11~#19 머지) | git ls-files + git grep + grep CORS_ORIGINS | secret 평문 0건 / JWT 평문 0건 / .env 파일 git 0건 / CORS_ORIGINS=`http://localhost:5173` (wildcard `*` 미사용) (R-N-05) | WBS I-10 / contract §1 |
| AC-02 | fresh checkout (`git worktree add ../realworld-py-fresh main`) | LOCAL.md §3.1 backend + frontend 부팅 명령 그대로 실행 | 5분 이내 부팅 완료 (backend uvicorn 8000 + frontend Vite 5173) | WBS I-10 (Manual verification) |
| AC-03 | main PR 머지 (squash and merge) | gh pr merge --squash | CI green + AI 게이트 6축 PASS + Sprint 1·2 10/10 머지 완료 + 사이클 종료 | WBS I-10 |

## 2. Definition of Done (D-06)

WBS I-10 DoD 9건 매핑 — D-10-N 명명:

- [ ] D-10-1 `/cso` 보안 점검 1회 — secret 평문·취약 라이브러리·CORS=`*` 점검 (gstack /cso 대체로 git ls-files + git grep + grep CORS 수동 4 항목)
- [ ] D-10-2 git grep으로 secret 평문 0건 확인
- [ ] D-10-3 `git worktree add ../realworld-py-fresh main` + LOCAL.md §3.1 부팅 ≤ 5분 (Manual verification)
- [ ] D-10-4 README.md — 프로젝트 의도 1단락 + LOCAL.md 링크 + 기술 스택
- [ ] D-10-5 CHANGELOG.md — v0.1.0 first release notes
- [ ] D-10-6 `/retro` 실행 결과 → `docs/planning/retro/2026-05-21-cycle.md` (수동 5+5+5 markdown 대체)
- [ ] D-10-7 PR description AI 게이트 6축 체크리스트 + 골든패스 스크린샷 7장(I-09 PR에 포함) + `/cso` 보고서 인용
- [ ] D-10-8 main 머지 (squash and merge) — 사람 책임
- [ ] D-10-9 pytest --cov 적용 범위 ≥ 80% (R-N-06) — 77 passed 유지 + I-04 --cov-fail-under=80 정착

## 3. 비기능 인수

- **R-N-05 (XSS/SQLi)**: 4 항목 점검 0건 (.env·JWT·secret·CORS wildcard 모두 PASS)
- **R-N-06 (커버리지)**: 77 passed + --cov-fail-under=80 정착(I-04)
- **R-N-04 (시크릿)**: 본 PR docs only → 신규 시크릿 노출 0

## 4. 회귀 인수

- backend pytest **77 passed**
- frontend npm run build 60 modules
- backend dev 8000 + frontend dev 5173 동시 부팅 회귀 N/A
- alembic 0004 (head) 정합 유지