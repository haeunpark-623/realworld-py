---
doc_type: feature-brief
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

# feat-seed-performance — Feature Brief

> Issue #5 / Sprint 1 / I-05 (effort 0.5d ≈ 30~45min). I-04 머지 직후 — 게시글 100건 + 사용자 10명 + 태그 5종을 멱등 seed 스크립트로 생성하고, GET /api/articles?limit=20을 100회 호출해 p95 < 200ms (R-N-01) 충족을 통합 테스트로 검증. Sprint 1 마지막 이슈.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — mode=add 자동 결정 / R-N-01 + R-F-04 매핑 / 영향 3 영역 / 비목표 4건 |

## 1. 한 줄 의도

게시글 100건 + 사용자 10명 + 태그 5종을 멱등 seed 스크립트로 생성하고, GET /api/articles?limit=20을 100회 호출해 p95 < 200ms를 충족함을 통합 테스트로 측정·검증한다.

## 2. 사용자 가치

- **개발자 (간접)**: 빈 DB가 아닌 *현실적인 데이터셋*에서 라우트 응답 시간을 검증해 R-N-01(API p95 < 200ms) 충족 여부를 *측정값*으로 확인할 수 있다. I-04 selectinload N+1 회피 결정의 효과를 정량적으로 입증.
- **운영자 (간접)**: 차후 Sprint 2 frontend 작업 시 게시판 화면이 *비어 보이지 않게* 100건 데이터로 시각적 검증 가능 (I-09 HomePage 진입).
- **검증자 (간접)**: 02-feasibility §6.1·15-risk RISK-07에서 명시한 성능 측정 게이트 — 코드가 컴파일·통합 테스트 PASS와 별개로 *p95 측정값*이 200ms를 만족함을 PR description에 첨부.

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 (PR #14 머지 직후) | 변경 후 (본 PR 머지 직후) |
| --- | --- | --- |
| seed 스크립트 | 없음 — DB는 alembic 마이그레이션 후 빈 상태 | + `scripts/seed_articles.py` 모듈 (Python `python -m scripts.seed_articles` 진입점) — User 10 + Article 100 + Tag 5 멱등 생성 |
| 성능 측정 | 없음 — R-N-01은 *목표값만* 명시. 측정 없음 | + `tests/integration/test_performance.py::test_articles_list_p95` (GET /api/articles?limit=20 100회 호출 → p95 < 200ms 어서션 + stdout 측정값 출력) |
| 디렉토리 | `backend/realworld/` + `backend/tests/` | + `backend/scripts/` 신규 (`__init__.py` + `seed_articles.py`) |
| Tag 관계 | I-04 ArticleService.create 시 동적 생성만. 시드 데이터 0 | + 5종 고정 태그 ("python", "fastapi", "react", "sqlalchemy", "realworld") + 100개 Article 무작위 0~3 매핑 |
| 테스트 합산 | 52 passed (3 health + 30 unit + 19 integration) | + 통합 1건 = 53 passed (test_performance.py 1) |
| ID 매핑 (R-F) | R-F-01~08·R-F-12·R-N-03·R-N-04 cover | + R-N-01 (cover로 승격, 실 측정값 PASS) + R-F-04 (목록 라우트 성능 확인) |

## 4. 모드 자동 감지 결과

**mode=add** (자동 결정, ADR-0032 §2.1 무질문 진행). 부정 시그널 0건:

- ❌ `type:bug` 라벨 → 없음. 본 이슈는 `type:test`·`area:backend`·`priority:P1`. type:test는 모드 결정에 영향 없음 (bug 시그널 아님)
- ❌ UI/시각/token/리브랜딩 키워드 → 없음 (백엔드 측정만)
- ❌ 기존 동작 변경 / breaking 가능성 → 없음 (신규 스크립트 + 신규 테스트 1건 추가만, 기존 라우트·서비스·모델 변경 0)

✅ 부정 시그널 0건 → 기본값 add 결정 (ADR-0032 규칙 4).

**Mode Decision Trace**: PR body Mode Decision Trace 절에 위 3행을 그대로 인용 (ADR-0032 §3.2).

## 5. 영향 범위

**3 영역 → PR body Touched Areas 절 필수 (pull-request.md §4.2)**. 본 PR 3 영역:

| 영역 | 변경 내용 | 영향 |
| --- | --- | --- |
| backend 스크립트 | `backend/scripts/__init__.py` + `backend/scripts/seed_articles.py` (User 10 + Article 100 + Tag 5 멱등 생성, async + AsyncSession) | 2 신규 파일 |
| backend 테스트 | `backend/tests/integration/test_performance.py` (GET /api/articles?limit=20 100회 호출 + statistics.quantiles p95 측정 + stdout 출력 + assert) | 1 신규 파일 |
| 문서 | 12-scaffolding/python.md §1 트리에 `scripts/seed_articles.py` + §5 빌드·실행 명령에 seed 1줄 추가 + 14-wbs Issue #5 status:in-review + INDEX.md 변경 이력 | docs 3 파일 갱신 |

**UI / FE 영향**: 0건. 본 PR은 백엔드 스크립트·통합 테스트. ui_changed=false. AI 게이트 5번째 축 N/A로 자동 통과 (ADR-0011).

**부팅 자산 동기 (ADR-0040)**: 변경 0건. alembic migrations·`.env.example`·LOCAL.md·pyproject.toml·uv.lock 모두 변경 없음 (의존성 추가 0 — statistics는 stdlib). dev profile만 검증 (RFP §NFR-06 단일 환경 운영).

## 6. 비목표

| # | 항목 | 사유 | 위탁 위치 |
| --- | --- | --- | --- |
| 1 | seed 스크립트 CLI 옵션 (--count, --user-count 등) | 본 학습 과제는 고정 100/10/5. 옵션 추가는 후속 학습 과제. argparse 미사용 | 후속 (필요 시 별도 이슈) |
| 2 | locust / hey / wrk 등 외부 부하 도구 통합 | 02-feasibility 기각. 본 학습은 *Python 내부 측정으로 충분* | 비목표 (RFP §Out of Scope) |
| 3 | p99 / 평균 / 표준편차 측정 | RFP §NFR §R-N-01은 p95만 명시. 추가 통계는 의미 없음 | 비목표 |
| 4 | 인증 라우트(POST /api/users·login·GET /api/user) 성능 측정 | R-N-01은 *GET /api/articles* 한정. 인증은 bcrypt 의도적 느림 (~100ms) | 비목표 |

## 7. Open Questions

| # | Question | 결정 시점 | 임시 가정 |
| --- | --- | --- | --- |
| 1 | seed 스크립트 멱등 방식 — TRUNCATE vs DELETE 전부 vs UPSERT | P3 contract | **DELETE 전부 후 INSERT** — SQLAlchemy `await session.execute(delete(Article))` + `delete(Tag)` + `delete(User)` 3행. TRUNCATE는 SQLite 미지원, UPSERT는 코드 복잡도 ↑ |
| 2 | Article 본문 텍스트 — Lorem ipsum vs faker vs 고정 문자열 | P3 contract | **고정 문자열 + i 변수** — `f"Sample article body #{i}. Lorem ipsum dolor sit amet."` 1줄. faker는 외부 의존, 학습 과제에 과함 |
| 3 | Article-Tag 매핑 분포 — random vs 고정 | P3 contract | **random.seed(42) 고정 + 0~3 random.sample** — 재현 가능. statistics 모듈 stdlib |
| 4 | p95 측정 시 첫 호출 warmup 처리 | P3 contract | **첫 10회 warmup 제외 + 90회만 quantiles** — JIT/connection pool warmup 효과 분리. 100회 호출 후 1~10 인덱스 skip |
| 5 | seed 스크립트와 test_performance.py 결합 방식 | P3 contract | **분리** — seed는 `python -m scripts.seed_articles` 수동 실행. test_performance.py는 conftest.py integration_client + 자체 fixture로 seed_in_memory (DB 1회 setup) |
