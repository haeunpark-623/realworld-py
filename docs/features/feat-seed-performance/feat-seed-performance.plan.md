---
doc_type: feature-plan
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

# feat-seed-performance — Implementation Plan

> Issue #5 / I-05 / effort 0.5d ≈ 30~45min. selective read (ADR-0018): contract §0 8행만 진입. critical path C1→C2→C3 (3 커밋). 신규 모듈만 추가 — 기존 코드 변경 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 3 커밋 DAG (seed script → performance test → docs sync). critical path 직선. D-05-1~5 결정 5건 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
|---|---|---|---|---|
| C1 | `feat(backend): scripts/seed_articles.py 멱등 seed (User 10 + Article 100 + Tag 5)` | `backend/scripts/__init__.py` + `backend/scripts/seed_articles.py` | (수동 실행 확인) | 0 — 신규 디렉토리·기존 코드 변경 없음 |
| C2 | `test(backend): tests/integration/test_performance.py — GET /api/articles?limit=20 p95 < 200ms` | `backend/tests/integration/test_performance.py` | test_articles_list_p95 1건 (warmup 10 + 측정 90 → quantiles[18]) | 0 — 새 파일 + 자체 fixture |
| C3 | `docs(plan): 12-scaffolding §1+§5 + 14-wbs I-05 + INDEX v0.9 — Sprint 1 완료` | `docs/planning/12-scaffolding/python.md` + `docs/planning/14-wbs/14-wbs.md` + `docs/planning/INDEX.md` | (문서 갱신만) | 0 |

## 2. 의존성 그래프

```
C1 (seed script) ─→ C2 (performance test)
                     │
                     ▼
                    C3 (docs sync)
```

- **critical path**: C1 → C2 → C3 (직선). C1 없으면 C2 fixture가 `from realworld.models.article import Article` 등 import는 가능하지만 *시드 로직 자체를 검증* 못 함 (seed_articles.py의 `seed()` async 함수가 fixture에서 import되어 in-memory DB에 시드 데이터 채우는 단일 진입점).
- C2는 C1의 `seed()` 함수를 import해 in-memory engine에 *재사용*. 코드 중복 회피 + 멱등 검증 동시 충족.
- C3는 C1·C2 머지 후 문서 동기. PR open 직전.

## 3. 테스트 매핑

| 커밋 | 테스트 추가 위치 | 시나리오 |
|---|---|---|
| C1 | (단위 테스트 0 — seed는 스크립트성 코드) | 수동 검증: `(cd backend && uv run python -m scripts.seed_articles)` 실행 → `select count(*)` 3회로 User=10·Article=100·Tag=5 확인. 재실행 시 DELETE 후 INSERT 멱등 |
| C2 | `tests/integration/test_performance.py::test_articles_list_p95` | (1) seed_articles.seed(session) 호출로 in-memory DB seed. (2) GET /api/articles?limit=20 100회 호출 (warmup 10 제외). (3) latencies[10:] 90건 statistics.quantiles(n=20)[18] = p95. (4) assert p95 < 0.200 (sec). (5) print(f"p95={p95*1000:.2f}ms") stdout |
| C3 | (테스트 0 — 문서만) | validate-doc.sh 통과 + check-test-catalog-sync.sh WARN 0 확인 |

## 4. 빌드·실행 검증 단계

```bash
# C1 commit 직후 — seed 수동 실행
cd backend
uv run alembic upgrade head
uv run python -m scripts.seed_articles
uv run python -c "
import asyncio
from sqlalchemy import select, func
from realworld.db import AsyncSessionLocal
from realworld.models import User, Article, Tag
async def check():
    async with AsyncSessionLocal() as s:
        u = (await s.execute(select(func.count(User.id)))).scalar_one()
        a = (await s.execute(select(func.count(Article.id)))).scalar_one()
        t = (await s.execute(select(func.count(Tag.id)))).scalar_one()
        print(f'users={u} articles={a} tags={t}')
asyncio.run(check())
"
# 기대: users=10 articles=100 tags=5

# C2 commit 직후 — p95 측정
uv run pytest tests/integration/test_performance.py -v -s
# 기대: 1 passed + stdout에 p95=??ms 출력 + < 200ms

# C3 commit 직후 — 문서 검증
cd ..
bash .claude/scripts/validate-doc.sh docs/planning/12-scaffolding/python.md
bash .claude/scripts/validate-doc.sh docs/planning/14-wbs/14-wbs.md
bash .claude/scripts/validate-doc.sh docs/planning/INDEX.md

# AI 게이트 전 종합 확인 (C3 직후)
cd backend
uv run alembic upgrade head
uv run ruff check .
uv run ruff format --check .
uv run pytest -v
# 기대: 53 passed (52 + test_articles_list_p95 1)
```

## 5. 점진 합의 / 결정 발생 항목

- **ADR 작성 필요**: no — 본 PR은 신규 *측정 인프라*만 추가. 기존 동작·아키텍처 변경 0. ADR-0011(AI 게이트 6축)·ADR-0037(부팅 자산)에 이미 측정 정책 명시됨
- **D-05-1**: seed 멱등 방식 = DELETE 전부 후 INSERT (3 테이블 순서 article_tags M2M cascade → articles → tags → users). TRUNCATE는 SQLite 미지원, UPSERT는 코드 ↑
- **D-05-2**: bcrypt 사용 — seed 사용자 10명 비밀번호는 `"seed-password"` 공통 (utils/security.hash_password 호출). 학습 과제, 보안 위험 0 (dev DB only)
- **D-05-3**: warmup 10회 제외 — JIT·connection pool·SQLAlchemy compiled cache 영향 분리. 90회 측정값으로 quantiles(n=20)[18] = p95
- **D-05-4**: 측정값 stdout 출력 — `pytest -s` 옵션 필요. PR description에 stdout 캡처 첨부 가능
- **D-05-5**: random.seed(42) 고정 — Article 본문·태그 매핑 재현 가능. CI 멱등 보장
