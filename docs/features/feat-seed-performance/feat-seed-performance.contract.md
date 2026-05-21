---
doc_type: feature-contract
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

# feat-seed-performance — Change Contract

> Issue #5 / Sprint 1 / I-05 / mode=add (자동 결정, 부정 시그널 0). 신규 모듈 `backend/scripts/` + 통합 테스트 1건. 기존 라우트·서비스·모델·migrations 변경 0. selective read 진입점은 §0 8행.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — §0 8행 + §2 6행 + §3 3행 + BC neutral + Rollback (revert + 신규 파일 삭제 only) |

## 0. 참조 정본 ID (Referenced-IDs)

> ADR-0018. P4 implementation-planner가 본 표만 selective read해 결정 영역 식별.

| 종류 | 정본 위치 | 영향 ID |
|---|---|---|
| R-ID (요구) | `docs/planning/04-srs/04-srs.md` | R-N-01 (API p95 < 200ms), R-F-04 (게시글 목록) |
| F-ID (기능) | `docs/planning/05-prd/05-prd.md` | F-02 (게시판) |
| 영향 모듈 | `docs/planning/08-lld-module-spec/08-lld-module-spec.md` §1·§4 | (none — 신규 `scripts/seed_articles.py` 추가만, 기존 모듈 무수정) |
| 영향 엔드포인트 | `docs/planning/09-lld-api-spec/09-lld-api-spec.md` §3 | GET /api/articles (참조만, 무수정) |
| 적용 컨벤션 절 | `docs/planning/11-coding-conventions/11-coding-conventions.md` §1·§2 | Python 네이밍 (snake_case, async def) |
| 12-scaffolding 트리 | `docs/planning/12-scaffolding/python.md` §1 | scripts/ 디렉토리 신규 + §5 빌드·실행 명령에 seed 1줄 추가 |
| 13-test-design | `docs/planning/13-test-design/02-catalog.md` | R-N-01·R-F-04 통합 fan-in 행 갱신 |
| 14-wbs | `docs/planning/14-wbs/14-wbs.md` §2 Sprint 1 | I-05 DoD 5행 |

## 1. 변경 의도

I-04에서 8 라우트가 동작 가능 상태이며 단위 13 + 통합 19 = 32 신규 테스트가 PASS다. 그러나 R-N-01(API p95 < 200ms)는 *목표값만 명시*되어 있고 *실 측정값 0*인 상태. 본 PR은 (1) 100건+10명+5종 시드 데이터를 멱등 생성하는 `scripts/seed_articles.py`와 (2) GET /api/articles?limit=20을 100회 호출해 p95 측정 후 `< 200ms` 어서션하는 `tests/integration/test_performance.py` 1건을 추가해 R-N-01을 *측정 PASS 상태*로 격상시킨다. 기존 라우트 동작·코드 변경 0 — selectinload N+1 회피(I-04)의 효과를 정량적으로 입증하는 게이트 측정 PR.

## 2. Before / After

| 항목 | Before | After |
|---|---|---|
| `backend/scripts/__init__.py` | (없음) | (신규) — 빈 파일, Python 패키지 인식 |
| `backend/scripts/seed_articles.py` | (없음) | (신규) — async def `seed()` + `if __name__ == "__main__": asyncio.run(seed())` 진입점. AsyncEngine + async_sessionmaker → bcrypt 10명 사용자 + Article 100건 + Tag 5종 + M2M 매핑 random.seed(42) 고정 |
| `backend/tests/integration/test_performance.py` | (없음) | (신규) — `async def test_articles_list_p95(integration_client)` 1건. seed_in_memory fixture로 in-memory DB에 사용자 10명·게시글 100건·태그 5종 setup → GET /api/articles?limit=20 100회 호출 → statistics.quantiles(latencies[10:], n=20)[18] (p95) < 200ms assert + stdout print |
| `backend/realworld/main.py` | (수정 없음 from I-04) | (수정 없음) — exception_handler·router 등록 그대로 |
| `backend/realworld/services/article.py` | (수정 없음 from I-04) | (수정 없음) — ArticleService.create·list 그대로 사용 |
| `backend/realworld/repositories/article.py` | (수정 없음 from I-04) | (수정 없음) — ArticleRepo.list_with_filters selectinload 그대로 사용. R-N-01 PASS 시 본 결정이 정량적으로 입증됨 |
| `docs/planning/12-scaffolding/python.md` §1 트리 | I-04 머지 후 `scripts/` 없음 | `scripts/__init__.py` + `scripts/seed_articles.py` 2 노드 추가 |

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
|---|---|---|
| 사용자 (CLI 호출) | `(cd backend && uv run python -m scripts.seed_articles)` 명령으로 `seed_articles.py:__main__` 진입 | LOCAL.md §3.1·12-scaffolding §5에 명령 1줄 추가 |
| pytest runner | `pytest tests/integration/test_performance.py -v -s` 실행 시 신규 1건 추가 | conftest.py `integration_client` fixture 재사용 + 본 파일 자체 `seeded_client` async fixture 정의 (lifespan 1회 seed) |
| GitHub Actions backend-ci | 매 PR `pytest -v` 실행 시 신규 1건 자동 포함 | 53 passed (52 + 1) 정합 갱신. workflow YAML 변경 0 |

## 4. Backward Compatibility

- **Breaking**: no — 기존 라우트·DB 스키마·테스트·migrations 변경 0. 신규 파일 3개만 추가 (scripts/__init__.py + scripts/seed_articles.py + tests/integration/test_performance.py).
- **마이그레이션 필요**: no — alembic migrations 추가 0. seed 스크립트는 *DELETE 후 INSERT* 방식이므로 사용자가 수동 실행할 때만 dev DB에 영향. CI/test는 in-memory DB 사용.

본 PR 머지 직후 기존 사용자 경험 변화 0. seed 스크립트는 *opt-in* (수동 실행 안 하면 동작 안 함).

## 5. Rollback 전략

- **revert 가능**: yes — 신규 파일 3개 삭제 + 14-wbs/INDEX 변경 이력 행 제거. 1-commit revert로 충분 (`git revert <merge-sha>`).
- **rollback 절차**: (1) `git revert <merge-sha>` → revert PR 생성. (2) 머지 후 main 자동 동기. (3) 사용자 dev DB는 seed 스크립트 *재실행 안 하면* 영향 0. 이미 실행했으면 본인이 alembic downgrade base + upgrade head로 초기화.
- **데이터 손상 위험**: 없음 — 본 PR 자체는 무수정 추가. seed 스크립트가 dev DB에서 DELETE 전부 후 INSERT를 수행하지만, 이는 *사용자 명시 실행* 시에만. 자동 실행 hook·CI 호출 0.

## 6. 비목표

- seed 스크립트 CLI 옵션 (argparse) — 후속
- locust/wrk 등 외부 부하 도구 — 02-feasibility 기각
- p99/평균/표준편차 — RFP §NFR §R-N-01 p95만 명시
- 인증 라우트(POST /api/users·login) 성능 측정 — bcrypt 의도적 느림
- Comment·Profile·Follow 라우트 성능 — Out of Scope 또는 Sprint 2
