---
doc_type: feature-risk
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

# feat-seed-performance — Feature Risk

> P7. 4 F-RISK. 모두 Low. High 0건 → 단계적 롤아웃 N/A.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — F-RISK-01~04 (성능 미달 / 멱등 실패 / 외래키 위반 / 통계 신뢰성). 모두 Low |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
|---|---|---|---|---|
| F-RISK-01 | R-N-01 p95 < 200ms 미달 (측정값 200ms 초과) | 3 | 2 | Low |
| F-RISK-02 | seed 재실행 시 외래키 위반·트랜잭션 실패 | 3 | 2 | Low |
| F-RISK-03 | in-memory aiosqlite p95 측정값과 실 운영 SQLite 파일 측정값 괴리 | 2 | 3 | Low |
| F-RISK-04 | statistics.quantiles(n=20)[18] p95 신뢰성 (90 샘플로 충분한가) | 1 | 2 | Low |

15-risk RISK-07(성능 미달)과 매핑. 본 PR이 RISK-07의 *측정 게이트*.

## 2. 리스크 상세

### F-RISK-01: R-N-01 p95 < 200ms 미달

- **카테고리**: 성능
- **트리거 신호**: pytest test_articles_list_p95 실행 시 assert FAIL — `assert p95 < 0.200` 위반. stdout에 `p95=??ms` 200ms 초과
- **완화 전략**: (1) I-04에서 ArticleRepo.list_with_filters에 selectinload(Article.tags) + joined eager load(Article.author) 적용해 N+1 회피 완료 — 정상 케이스 p95 ~ 5~20ms 예상. (2) FAIL 시 RISK-07 후속 조치로 SQLAlchemy lazy="raise" + 쿼리 카운트 검증으로 N+1 잔존 여부 직접 확인. (3) FAIL 시 SQLite 파일 인덱스 누락 의심 → migrations/0003 인덱스(`articles.author_id`·`articles.slug`) 검증
- **검증 방법**: 자동 — pytest test_articles_list_p95 + stdout 출력값 PR description에 첨부

### F-RISK-02: seed 재실행 시 외래키 위반·트랜잭션 실패

- **카테고리**: 데이터 영속성
- **트리거 신호**: 2회차 실행 시 `(sqlite3.IntegrityError) FOREIGN KEY constraint failed` 등 외래키 위반 또는 부분 INSERT 후 ROLLBACK
- **완화 전략**: (1) DELETE 순서 강제 — article_tags M2M (CASCADE 의존) → articles → tags → users 4 테이블 순. (2) 단일 트랜잭션 `async with session.begin()` 내부 모든 DELETE + INSERT 실행 — 실패 시 자동 ROLLBACK. (3) ON DELETE CASCADE(I-04 alembic 0003)로 article_tags는 articles DELETE 시 자동 정리됨, 명시 DELETE는 안전 마진
- **검증 방법**: 수동 — AC-02 (2회 연속 실행 + count 확인)

### F-RISK-03: in-memory aiosqlite vs 운영 SQLite 파일 측정값 괴리

- **카테고리**: 성능
- **트리거 신호**: test_articles_list_p95 PASS인데 실 운영 DB(backend/dev.db 파일)에서 측정 시 p95 200ms 초과
- **완화 전략**: (1) 본 학습 과제는 단일 환경 운영 (RFP §NFR-06), in-memory 측정으로 갈음 가능. (2) FAIL 위험 시 후속 학습 과제에서 실 파일 SQLite + `pragma journal_mode=WAL` 적용해 재측정. (3) 본 PR의 *측정 인프라*는 운영 DB 측정에 그대로 재사용 가능 (engine URL만 교체)
- **검증 방법**: 수동 (후속 — 본 PR 범위 외) — 필요 시 `DATABASE_URL=sqlite+aiosqlite:///dev.db pytest tests/integration/test_performance.py -v -s`로 실 파일 측정

### F-RISK-04: statistics.quantiles 90 샘플 신뢰성

- **카테고리**: 성능
- **트리거 신호**: 측정값이 매 실행마다 ±50ms 등 큰 변동. 1회는 PASS 1회는 FAIL
- **완화 전략**: (1) random.seed(42) 고정 + warmup 10 제외로 변동 폭 축소. (2) 200ms 임계값 대비 selectinload N+1 회피 효과는 *수 ms ~ 수십 ms 수준* 차이 — 임계값 200ms 마진이 충분히 큼. (3) 신뢰성 향상 필요 시 후속 학습 과제에서 1000회 호출 + 5분위 percentile 사용
- **검증 방법**: 자동 — pytest 1회 실행 + CI 재현성. 동일 random.seed로 재실행 시 ±5ms 이내 변동 기대

## 3. High 등급 단계적 롤아웃

**N/A** — High 등급 리스크 0건. 모두 Low. 본 PR은 신규 *측정 인프라* 추가만, 기존 동작 변경 0. 단계적 롤아웃 불필요. 단일 PR 일괄 머지.

## 4. 데이터 영속성 변경

- DB 스키마 변경: 0 (alembic migrations 추가 0)
- seed 스크립트는 dev DB 데이터 *DELETE 후 INSERT* 수행 — 사용자 명시 실행 시에만. 운영 자동 트리거 0
- CI/test는 in-memory aiosqlite — 영속성 영향 0

## 5. 15-risk.md 갱신 항목

본 PR 머지 시 15-risk.md RISK-07(성능 미달)의 `완화 상태`를 `미측정 (목표값만)` → `측정 PASS (test_articles_list_p95 + stdout)`로 갱신 가능 (P13 docs-update에서). RISK-01·02·03·04·05·06·08은 본 PR과 무관.
