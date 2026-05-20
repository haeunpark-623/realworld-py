---
doc_type: test-design
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: [R-N-06]
  F-ID: [F-01, F-02, F-03, F-04]
  supersedes: null
---

# 13-test-design / 01-strategy — Test Strategy

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, ADR-0034 sub-file BLOCK 충족 — 방법론·레벨·커버리지 ≥ 80%) |

## 1. 방법론 (TDD/BDD)

본 프로젝트는 **비-TDD** 접근을 채택한다 — 사이클 자체가 학습 목표라서 *설계 후 구현 + 즉시 단위 테스트 작성*이 가장 학습 효과 높다는 판단. 단, **BDD-style 어휘**(Given/When/Then)는 04-srs·05-prd Acceptance 정의 단계부터 사용 중이므로 테스트 함수 명명에도 동일 어휘를 일부 적용한다.

- **테스트 작성 시점**: 서비스 구현 직후 같은 PR에서 작성 (별 PR 분리 금지). 통합 테스트는 라우터 구현 직후. 단위·통합 테스트 미작성 시 `/code-review` 진입 차단 (Strict Rule §5).
- **테스트 함수 명명**: `test_<scenario>_<expected>()` 형식 — 예: `test_register_duplicate_email_returns_422()`, `test_article_delete_cascades_comments()`. 11-coding-conventions §1 정본.
- **레벨**: **단위 / 통합 / E2E** 3축 모두 적용. 단, 본 프로젝트는 백엔드 1차 목표이므로 단위·통합 중심. E2E는 gstack `/qa` 골든패스 1회로 대체 (F-04 UI 단위/통합 N/A 결정, v0.2).

## 2. 도구 선택

| 레벨 | 도구 | 이유 |
|---|---|---|
| 단위 (Python) | `pytest` + `pytest-asyncio` + `pytest-cov` | Python 표준. async 함수 테스트 + 커버리지 측정 일괄 |
| 단위 fixture·factory | `pytest` fixture (`conftest.py`) — `pytest-factoryboy` 등 추가 도구는 학습 부담 회피로 미도입 | 학습 단순성. 게이트 C `13-test-design` 결정 |
| 단위 mocking | `unittest.mock` (stdlib) + `pytest-mock` | 표준. DB는 mock 대신 *실제 SQLite 인메모리* 사용(`sqlite:///:memory:`) — 학습 정합성 우선 |
| 통합 | `pytest` + `httpx.AsyncClient` (FastAPI TestClient의 비동기 대체) | FastAPI 공식 권장 |
| 통합 DB | SQLite 인메모리 (`sqlite+aiosqlite:///:memory:`) per-test session | 빠름·격리·외부 의존 0 |
| E2E (브라우저) | gstack `/qa` (외부 도구) | DoD §3 — 골든패스 1회. Playwright 직접 작성은 학습 범위 외 |
| 성능 (R-N-01) | `pytest` + `httpx` + `statistics.quantiles` | 게시글 목록 API 100회 호출 → p95 계산. 별 도구 도입 불필요 |
| FCP 측정 (R-N-02) | gstack `/qa` Performance 트레이스 1회 | Lighthouse 등 별 도구 미도입. 학습 컨텍스트 |
| XSS 검증 (R-N-05) | gstack `/qa` 페이로드 1회 시도 | 단순 입력 후 응답 escape 확인 |

## 3. 커버리지 목표 (≥ 80%)

**커버리지 목표**: **80% 이상** (ADR-0015 §2.3 정책값 채택, 04-srs §R-N-06).

- **측정 도구**: `pytest-cov`
- **측정 명령**: `uv run pytest --cov=realworld/services --cov=realworld/deps --cov-fail-under=80`
- **적용 범위 (04-srs §R-N-06)**:
  - `backend/realworld/services/auth.py` (UserService / AuthService)
  - `backend/realworld/services/article.py` (ArticleService)
  - `backend/realworld/services/comment.py` (CommentService)
  - `backend/realworld/deps/auth.py` (require_auth, require_author)
  - `backend/realworld/utils/security.py` (bcrypt hash·verify)
  - `backend/realworld/utils/jwt.py` (encode·decode)
  - `backend/realworld/utils/slug.py` (kebab-case + 숫자 suffix)
- **제외 범위**:
  - `routers/*` — 통합 테스트가 라우터+서비스+DB까지 커버
  - `schemas/*` — Pydantic 모델은 declarative, 테스트 우선순위 낮음
  - `models/*` — SQLAlchemy declarative
  - `config.py`, `db.py`, `main.py` — 부팅·설정 코드
  - `frontend/*` — F-04 UI 단위/통합 N/A 결정 (v0.2)
- **임계 미달 시**:
  - CI에서 `--cov-fail-under=80` 옵션이 실패 → 머지 차단
  - 누락 케이스에 단위 테스트 추가 → 통과 후 재시도
  - 적용 범위 자체 조정이 필요하면 04-srs §R-N-06 갱신 + ADR 신설

> 본 정량값(≥ 80%)은 ADR-0015 §2.3 정책. RFP §NFR-05의 60% 기준과 차이가 있으나 게이트 B에서 사용자가 정책값을 채택 결정 (v0.2).
