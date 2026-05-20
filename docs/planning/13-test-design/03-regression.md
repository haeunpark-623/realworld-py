---
doc_type: test-design
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: []
  F-ID: [F-01, F-02, F-03, F-04]
  supersedes: null
---

# 13-test-design / 03-regression — Regression Test Policy

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, 학습 컨텍스트에 맞춘 최소 회귀 정책) |

## 1. 회귀 범위

본 프로젝트는 *전체 테스트 스위트가 회귀 범위*. 학습 컨텍스트 + MVP 규모(~ 25개 테스트 예상)이므로 부분 회귀·테스트 선별 실행 같은 최적화는 도입하지 않음.

- **단위 + 통합 전체 실행**: `uv run pytest`. 평균 < 30초 소요 가정.
- **커버리지 측정 동시 실행**: `--cov=realworld/services --cov=realworld/deps --cov-fail-under=80` 옵션을 매 CI 실행에 항상 포함.
- **E2E 골든패스**: gstack `/qa`는 PR 단계에서 1회. dev 단계 매 커밋엔 실행 안 함(시간 소요 + 외부 도구 의존).

## 2. 자동화 정책

| 시점 | 실행 대상 | 도구 / 명령 |
|---|---|---|
| 로컬 커밋 | 변경 파일 lint·format + 빠른 단위 테스트(선택) | pre-commit 훅 (ruff, black, eslint, prettier) |
| 로컬 push 전 | 전체 단위 + 통합 | `uv run pytest` (수동, 권장) |
| PR 생성 시 | 전체 단위 + 통합 + 커버리지 + lint | GitHub Actions `ci.yml` (자동) |
| PR 머지 직전 | 위 + gstack `/qa` 골든패스 E2E | 작성자가 로컬에서 1회 실행, 스크린샷 첨부 (수동) |
| main push | 동일 (PR 시점과 동일) | GitHub Actions `ci.yml` |

GitHub Actions 워크플로는 단일 (`.github/workflows/ci.yml`). matrix·캐시 등 최적화는 학습 부담 회피로 미적용 — 30초 실행이라 캐시 없이도 부담 없음.

## 3. 회귀 트리거

다음 변경은 *반드시 전체 회귀*를 PR 단계에서 통과해야 한다:

- `backend/realworld/services/*.py` 변경 → 단위·통합 전체
- `backend/realworld/models/*.py` 변경 (DB 스키마 변경) → 통합·마이그레이션 + 골든패스 E2E
- `backend/realworld/routers/*.py` 변경 → 통합 전체
- `backend/realworld/deps/auth.py` 또는 `utils/security.py` 또는 `utils/jwt.py` 변경 (보안 핵심) → 단위·통합 전체 + `/cso` 보안 점검
- `frontend/src/api/client.ts` 또는 `frontend/src/store/auth.ts` 변경 → 골든패스 E2E
- `pyproject.toml` 의존성 변경 → 전체 + lockfile 갱신
- `alembic/versions/*.py` 신규 또는 변경 → 통합 전체

다음 변경은 *전체 회귀 부담 적정*이라 trivial 변경으로 분류 (PR CI만 수행, 별 단계 추가 없음):

- 주석·docstring·README 수정
- 타입 힌트 추가
- 11-coding-conventions 표 갱신
