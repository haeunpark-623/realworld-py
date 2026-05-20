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

# 13-test-design / 05-delivery-format — Customer Delivery Format

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, ADR-0034 ID 채번 + 전달 시점 BLOCK 충족) |

## 1. 산출 범위 (단위·통합·E2E 시나리오)

본 프로젝트는 학습 과제로 *외부 고객 납품 없음*. 단, 사이클 완주 학습 목적상 다음을 *내부 산출*로 정리하여 멘토·리뷰어가 검토할 수 있게 한다.

| 산출 | 형식 | 위치 | 비고 |
|---|---|---|---|
| 단위·통합 테스트 코드 자체 | Python `tests/` 디렉토리 | `backend/tests/unit/`, `backend/tests/integration/` | pytest 표준 |
| 커버리지 리포트 | HTML | CI 아티팩트 `coverage-html/` | `pytest --cov-report=html` 생성 |
| 테스트 결과 (CI) | GitHub Actions log | `actions/runs/<id>` | 매 PR 자동 |
| 골든패스 E2E 스크린샷 | PNG | `docs/features/<slug>/screenshots/` | gstack `/qa` 출력 |
| 성능 측정 결과 (R-N-01 p95) | pytest 출력 stdout | CI log | `tests/integration/test_performance.py` 단일 |
| 보안 점검 (`/cso`) 결과 | Markdown report | PR 코멘트 (gstack 출력) | 매 PR |

본 프로젝트는 별도 고객 납품용 HTML/XLSX 보고서를 생성하지 않는다 (학습 컨텍스트). Allure·pytest-html 등 도구는 미도입.

## 2. 포맷·도구 (HTML/XLSX/Allure 등)

- **HTML**: `pytest-cov`의 HTML 리포트만 사용 (`htmlcov/` 디렉토리). 별도 디자인 안 함.
- **XLSX**: 미사용. 학습 컨텍스트.
- **Allure / pytest-html**: 미사용. 학습 부담 회피.
- **Markdown**: 본 산출(`docs/planning/13-test-design/*.md`)과 PR body가 정본.

## 3. 시나리오 ID 채번 규칙

본 프로젝트는 *고객 납품용 별도 ID 채번 미적용*. 04-srs R-ID와 13/02-catalog의 시나리오가 *그대로* 트레이스 ID 역할을 한다. 단, ADR-0034 schema BLOCK 충족을 위해 다음 채번 규칙을 명시:

| Prefix | 의미 | 예 | 비고 |
|---|---|---|---|
| **TC-** | Test Case (단위·통합 통합 채번, 사용 시) | `TC-001`, `TC-002` | 본 프로젝트는 *미사용* (04-srs R-ID로 대체) — 후속 학습 시 도입 검토 |
| **SC-** | Scenario (시나리오 단위) | `SC-AUTH-01`, `SC-ARTICLE-01` | 본 프로젝트는 미사용 |
| **UC-** | Use Case (사용자 여정) | `UC-01` ~ `UC-12` | 03-user-scenarios에서 이미 사용 중. 본 13에서도 fan-in 시 인용 가능 |
| **IT-** | Integration Test | `IT-USERS-01` | 본 프로젝트는 미사용 — `tests/integration/test_*_routes.py::test_*` 함수명으로 대체 |
| **E2E-** | E2E Test | `E2E-GOLDEN-PATH` | 본 프로젝트는 골든패스 1개라 ID 채번 불필요 — gstack `/qa` 단일 실행 |

**원칙**: 본 프로젝트는 *상류 ID(R-/F-/UC-)를 그대로 fan-in 키로 사용*. 별도 TC-/SC-/IT-/E2E- 채번을 도입하지 않음 — 작은 규모에서 중복 ID 관리 부담만 늘림.

후속 프로젝트(고객 납품·QA 전담 분리·테스트 자동화 도구 도입 등)에서 본 §3 규칙을 *활성화*하여 채번을 시작할 수 있도록 schema BLOCK 만 충족시켜 놓는다.

## 4. 전달 시점 (스프린트 종료·릴리스·고객 요청)

본 프로젝트는 학습 과제 + 단일 sprint(2일) + 외부 고객 없음. 다음 시점에 *내부 검토*가 발생:

- **PR 단계마다**: 매 PR에서 단위·통합 결과 + 커버리지 + (필요 시) gstack `/qa` 스크린샷이 GitHub PR body·CI log에 첨부. 멘토·리뷰어가 PR 단계에서 검토.
- **스프린트 종료 시**: 2026-05-22 마감 시점에 `/retro` 1회 실행 — 전체 사이클 회고 + 학습 노트 작성. `docs/planning/retro/<date>-cycle.md` 산출.
- **릴리스 시점**: 본 프로젝트는 클라우드 배포 없음 — 별도 릴리스 시점 없음. 단, main에 squash merge된 PR 단위가 *논리적 릴리스*. CHANGELOG.md 1회 갱신.
- **고객 요청 시점**: N/A — 외부 고객 없음. 단, 사내 멘토 요청 시 본 13-test-design 폴더 전체 + PR 링크 + CI 결과 링크를 단일 패키지로 제공.

전달 형식은 *모두 GitHub native* (PR body, CI artifact, Issue 코멘트, Discussions). 별도 보고서 도구 없음.
