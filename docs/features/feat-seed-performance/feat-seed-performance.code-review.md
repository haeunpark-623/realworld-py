---
doc_type: feature-code-review
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

# feat-seed-performance — Code Review

> P9. Generator ≠ Evaluator (self-review). C1·C2 2 코드 커밋 검토. PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — Verdict PASS. 6 OX 모두 PASS. NEEDS-WORK 0 |

## 0. Verdict

**PASS** — 2 코드 커밋(C1 seed + C2 test) 모두 contract §2 Before/After 6행 매핑. 측정값 p95=4.24ms로 R-N-01 200ms 마진 ~47배. NEEDS-WORK 0건.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (AI self-review)
- [review_at]: 2026-05-21

## 1. 컨트랙트 충실도

contract §2 6행 매핑:

| Before/After 항목 | Before | After 구현 (코드 경로) |
|---|---|---|
| `backend/scripts/__init__.py` | 없음 | `backend/scripts/__init__.py` 빈 파일 (Python 패키지 인식). C1 |
| `backend/scripts/seed_articles.py` | 없음 | C1 — `seed()` async + `main()` + `__main__` 진입점. random.seed(42) 고정. DELETE 순서 article_tags → Article → Tag → User |
| `backend/tests/integration/test_performance.py` | 없음 | C2 — `seeded_client` async fixture (in-memory aiosqlite + seed) + `test_articles_list_p95` (100 호출, warmup 10, p95 < 0.200 assert + stdout) |
| `backend/realworld/main.py` | 무수정 | 무수정 ✅ |
| `backend/realworld/services/article.py` | 무수정 | 무수정 ✅ |
| `backend/realworld/repositories/article.py` | 무수정 | 무수정 ✅ — 본 PR이 selectinload 효과 입증 |

contract §3 Call Sites 3행 매핑:

| Call Site | 동작 검증 |
|---|---|
| 사용자 CLI: `(cd backend && uv run python -m scripts.seed_articles)` | ✅ `users=10 articles=100 tags=5` 출력 — AC-01 PASS. 재실행도 동일 — AC-02 PASS |
| pytest runner: `pytest tests/integration/test_performance.py -v -s` | ✅ 1 passed in 0.64s — AC-03 PASS |
| GitHub Actions backend-ci `pytest -v` | ✅ 53 passed in 8.57s — AC-04 PASS |

contract §4 BC neutral, §5 Rollback 1-commit revert로 충분 — 모두 정합.

## 2. 테스트 커버리지

신규 1건 — `test_articles_list_p95`. 단위 0건 (seed는 스크립트성 코드).

- **Happy path**: 100 호출 모두 200 status. `articlesCount=100` + `len(articles)=20` 응답 형식 검증
- **측정 통계**: warmup 10 제외 + 90회 quantiles(n=20)[18] = p95. JIT/connection pool 영향 분리
- **Failure path 검토**: assert FAIL 시 stdout에 p95 값 노출되어 RISK-07 후속 조치 진입 가능
- **회귀**: 기존 52 테스트 무영향 — `seeded_client`는 자체 fixture로 conftest.py `integration_client` 분리 (DI override 충돌 0)

총 53 passed in 8.57s. 신규 테스트 0.64s 부담. CI workflow 변경 0.

## 3. 보안 / 시크릿

- seed `SEED_PASSWORD = "seed-password"` 상수 — dev 전용 시드, 운영 미사용. ruff S105 per-file-ignore 처리
- `random.seed(42)` 고정 — 재현성 목적, 보안 무관. ruff S311 per-file-ignore 처리
- bcrypt `hash_password` 호출 — utils/security 기존 함수 재사용. seed 사용자 10명 비밀번호 hash 1회 (성능 영향 minimal)
- 시크릿 노출 0 — 코드·로그·커밋 메시지에 환경변수 출력 없음. .env.* 변경 0
- 외부 의존 추가 0 — statistics는 stdlib, random은 stdlib, time은 stdlib

`/cso` 점검 대상 0. R-N-04(시크릿) 위반 0.

## 4. 가독성 / 단순성

- seed_articles.py 81줄 — 단일 진입점 명확. `seed()` 외부 호출용 + `main()` CLI 진입점 분리
- test_performance.py 76줄 — `seeded_client` fixture 24줄 + `test_articles_list_p95` 30줄. 상수 4개 모듈 상단 명시
- `from __future__ import annotations` — `list[float]` 등 PEP 604 미래 호환 (I-04 패턴 재사용)
- 함수 길이·매개변수 수·중첩 깊이 모두 컨벤션 §1·§2 준수
- 주석 minimal — 첫 line docstring + 함수 docstring만. 코드 자체가 표현적

## 5. 발견 사항 (3축 OX 분류)

ADR-0008 3축 OX:

| 발견 | in_scope | blocks_merge | same_area | 처리 |
|---|---|---|---|---|
| F1: `seed()` 외부 호출 시 `session.begin()` 위치 — 현재 `main()`에서만 transaction wrap | ⭕ in_scope | ❌ no | ⭕ same_area | INFO 처리. test fixture에서 `setup_session.begin()` 명시 호출하므로 안전. AC-02 멱등 검증 PASS |
| F2: `random.randint(0, 3)` — 평균 1.5 태그/article. 일부 article 태그 0건 가능 | ⭕ in_scope | ❌ no | ⭕ same_area | INFO 처리. 의도된 분포 — RealWorld 실 사용 시나리오 (태그 없는 글 존재) 반영 |
| F3: `latencies` list[float] 메모리 — 100건이라 무시 가능 | ⭕ in_scope | ❌ no | ⭕ same_area | INFO 처리. 100 * 8B = 800B |
| F4: `print(...)` stdout 출력 — pytest `-s` 옵션 필요 | ⭕ in_scope | ❌ no | ⭕ same_area | 의도. ADR-0011 6번째 축의 측정값 가시화 요건 충족. PR description에 첨부 가능 |
| F5: 측정 신뢰성 — 90 샘플 quantiles[18] p95 | ⭕ in_scope | ❌ no | ⭕ same_area | F-RISK-04에 명시. 200ms 임계값 마진 ~47배라 신뢰성 충분 |
| F6: `articlesCount=100` assertion — limit=20인데 전체 카운트 확인 | ⭕ in_scope | ❌ no | ⭕ same_area | 의도. ArticleRepo.list_with_filters의 count() 별도 쿼리 동작 검증 |

NEEDS-WORK 0건. blocks_merge=yes 0건. 모두 in_scope + same_area로 본 PR 범위 정합.

## 6. NEEDS-WORK 항목

(없음) — 6 OX 모두 PASS. P10 ai-qa-report 진입 허용.
