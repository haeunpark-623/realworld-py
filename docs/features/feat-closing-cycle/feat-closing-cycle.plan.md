---
doc_type: feature-plan
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

# feat-closing-cycle — Implementation Plan

> P4. 단일 commit DAG: C1 README + CHANGELOG + retro + feature docs 8 + docs sync 일괄.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 1 commit (docs 일괄) + 보안 점검 + 회귀 검증 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `docs(plan): I-10 사이클 종료 — README + CHANGELOG + retro + feat-closing-cycle 8 산출 (#10)` | README.md + CHANGELOG.md + docs/planning/retro/2026-05-21-cycle.md + feat-closing-cycle 8 docs + 14-wbs v0.13 + INDEX v0.14 | (없음) | 0 — docs만, 코드 0 |

ADR-0021 통과: docs(plan).

## 2. 의존성 그래프

```
C1 (사이클 종료 docs 일괄)
```

순환 없음. 단일 commit.

## 3. 테스트 매핑

WBS DoD에 자동 테스트 N/A. 검증은 *수동 + 자동 회귀*. 본 PR 코드 변경 0이라 commit-단위 테스트 매핑 N/A — 다음은 사이클 종료 검증 매트릭스:

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C1 | (없음 — 코드 변경 0) | backend pytest 77 passed / frontend build 60 modules / 보안 4 항목 / validate-doc.sh 모두 PASS / `git worktree` fresh checkout LOCAL.md §3.1 ≤ 5분 (Manual verification) |

## 4. 빌드·실행 검증 단계

```bash
# 1) backend 회귀
cd backend && uv run pytest -v
# expect: 77 passed

# 2) frontend 빌드
cd frontend && npm run build
# expect: 60 modules, dist/ exit 0

# 3) 보안 점검 (수동 /cso 대체)
git ls-files | grep -E "^\.env(\.|$)" || echo "(none — .env NOT tracked)"
git grep "eyJ[A-Za-z0-9_-]\{20,\}" || echo "(none — JWT 평문 0건)"
git grep -E "JWT_SECRET\s*=\s*[a-zA-Z0-9]{20,}" || echo "(none — secret 평문 0건)"
grep -r "CORS_ORIGINS" backend/.env.example backend/realworld/config.py
# expect: http://localhost:5173 (wildcard 미사용)

# 4) validate
bash .claude/scripts/validate-doc.sh docs/features/feat-closing-cycle/*.md
```

## 5. 점진 합의 / 결정 발생 항목

- **(1) /cso 자동 호출 대체**: gstack `/cso` 직접 호출 대신 git ls-files + git grep + CORS 수동 점검으로 대체. 학습 컨텍스트 acceptable
- **(2) `git worktree` fresh checkout**: AI 자동 N/A — Manual verification에서 사람이 별도 디렉토리에 worktree 생성 + LOCAL.md §3.1 명령 실행 + 5분 부팅 확인
- **(3) /retro 형식**: 5+5+5 형식 (잘된 점·개선점·메모). devtoolkit-template `retro/0000-*.md` 참고하지 않고 단순 markdown
- **(4) CHANGELOG 단일 release**: v0.1.0 first release 1건. 후속 학습에서 v0.2.0 추가 시 위에 prepend
- **(5) README.md 영문 미작성**: 한국어만. 학습 컨텍스트 + 1인 작업