---
doc_type: feature-acceptance
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-N-01, R-F-04]
  F-ID: [F-02]
  supersedes: null
---

# feat-seed-performance — Acceptance Criteria

> P6. 4 AC + 5 DoD. PR body에 본 DoD를 그대로 미체크 상태로 등록 (ADR-0046 §2.3).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 4 AC (AC-01~04) + DoD 5 (D-05-1~5). 14-wbs §2 I-05 DoD 5행 정합 |

## 1. 인수 기준 (Given/When/Then)

### AC-01: scripts/seed_articles.py 멱등 실행

- **Given**: I-04 머지 직후 main 브랜치 + 빈 dev DB (alembic upgrade head 후)
- **When**: `(cd backend && uv run python -m scripts.seed_articles)` 1회 실행
- **Then**: User=10, Article=100, Tag=5 정확히 생성. stdout에 `users=10 articles=100 tags=5` 또는 동등 메시지 출력
- **측정 방법**: 자동 테스트 (수동 SELECT count 확인 + C1 commit 직후 plan §4 검증 코드 실행)
- **R-ID**: R-F-04 (게시글 목록 데이터 준비)

### AC-02: seed 재실행 멱등성

- **Given**: AC-01 1회 실행 후 dev DB에 100건 데이터 존재
- **When**: `(cd backend && uv run python -m scripts.seed_articles)` 2회차 실행
- **Then**: DELETE 전부 후 INSERT 재실행. 최종 User=10, Article=100, Tag=5 동일 유지. 에러 0. 외래키 위반 0
- **측정 방법**: 수동 확인 (재실행 + count 재검증)
- **R-ID**: R-F-04

### AC-03: test_articles_list_p95 통합 테스트 PASS

- **Given**: in-memory aiosqlite + seed_articles.seed() fixture 1회 setup 후 User 10·Article 100·Tag 5 채워진 DB
- **When**: `pytest tests/integration/test_performance.py -v -s` 실행 → GET /api/articles?limit=20 100회 호출 (warmup 10 + 측정 90)
- **Then**: latencies[10:] 90건 statistics.quantiles(n=20)[18] = p95 < 0.200 (sec). assert PASS + stdout에 `p95=??ms` 출력
- **측정 방법**: 자동 테스트 (pytest)
- **R-ID**: R-N-01 (API p95 < 200ms 목표값 충족)

### AC-04: 전체 회귀 53 passed

- **Given**: 본 PR feat/seed-performance-issue-5 브랜치 + 모든 커밋 적용 후 상태
- **When**: `(cd backend && uv run alembic upgrade head && uv run ruff check . && uv run ruff format --check . && uv run pytest -v)` 4 step 실행
- **Then**: alembic 0003 (head) 정합 + ruff check All checks passed + ruff format 44 files already formatted (42 + scripts 2) + pytest 53 passed (52 + test_articles_list_p95 1)
- **측정 방법**: 자동 테스트
- **R-ID**: R-N-01·R-F-04·(기존 매핑 회귀 검증)

## 2. Definition of Done (D-06)

14-wbs §2 I-05 DoD 5행 + ADR-0046 §2.3 (PR body 미체크 상태로 등록):

- [ ] **D-05-1** `backend/scripts/__init__.py` + `backend/scripts/seed_articles.py` 신규. async `seed()` 함수 + `if __name__ == "__main__": asyncio.run(seed())` 진입점 (단위 테스트 0, 수동 검증 only)
- [ ] **D-05-2** seed 멱등 — 재실행 시 DELETE 전부 후 INSERT. AC-02 수동 검증 PASS
- [ ] **D-05-3** `backend/tests/integration/test_performance.py::test_articles_list_p95` PASS (AI 게이트 시점)
- [ ] **D-05-4** 측정값 stdout 출력 — `pytest -s`로 `p95=??ms` 가시화 (PR description 첨부 가능)
- [ ] **D-05-5** P2 컷 후보 표시 — 본 이슈 시간 부족 시 Sprint 2로 미루기 가능 (14-wbs §0.3 컷 후보 #1). 본 PR로 충족 시 cut 불필요

본 DoD 5행은 PR body `### DoD coverage` 절에 그대로 미체크 상태로 등록한다 (ADR-0046 §2.3 schema BLOCK).

추가 머지 게이트 (사람 책임 3단):
- [ ] **단위 테스트 / 통합 테스트** — 53 passed (전체)
- [ ] **AI 게이트** — D-06 1단 6축 모두 PASS (UI 5번째 축 N/A 자동 통과)
- [ ] **Test Plan 4블록** — Build / Automated / Manual / DoD
- [ ] **tested 라벨** — v1.2 폐지. `pr-body-checkboxes` status check가 자동 발행 (ADR-0046 §3)
- [ ] **Approve** ≥ 1
- [ ] **CI green** — backend-ci workflow PASS

## 3. 비기능 인수

- R-N-01: GET /api/articles?limit=20 p95 < 200ms — AC-03이 *측정 PASS*로 입증
- R-N-03 (bcrypt): seed 사용자 10명 비밀번호 `"seed-password"`로 hash_password 호출 — 기존 bcrypt 로직 회귀 검증
- R-N-04 (시크릿): seed 스크립트 .env 의존 0 (DATABASE_URL은 db.py 기본값). 시크릿 추가 0

## 4. 회귀 인수

- 기존 52 테스트(3 health + 30 unit + 19 integration) 모두 PASS 유지
- 신규 1건 추가 → 53 passed
- 기존 라우트·서비스·모델·migrations 변경 0 → 회귀 위험 minimal
