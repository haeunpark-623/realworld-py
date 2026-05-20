---
doc_type: feature-risk
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: feature
related:
  R-ID: [R-N-04, R-N-06]
  F-ID: []
  supersedes: null
---

# feat-bootstrap-backend — Feature Risk

> Issue #1 — 백엔드 스캐폴딩 작업의 로컬 리스크. 시스템 전역 리스크(15-risk.md)와 별개로 *본 PR* 한정 분석.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — 5건 식별, High 0건. mode=add 최소 침습 |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| FRISK-01 | uv lockfile cross-platform 차이 (Win/Mac/Linux native deps) | 2 | 2 | Low |
| FRISK-02 | Alembic async env.py 설정 오류 (sync vs async 모드 혼용) | 3 | 2 | Low |
| FRISK-03 | backend-ci.yml 워크플로 첫 실행 실패 (uv setup-uv action 미동기) | 2 | 3 | Low |
| FRISK-04 | LOCAL.md §3.1 명령이 Windows PowerShell에서 미동작 (bash 가정) | 2 | 3 | Low |
| FRISK-05 | `.env.example`의 JWT_SECRET placeholder가 실제 시크릿으로 오해되어 production에 그대로 사용될 위험 | 4 | 1 | Low |

**High 0건** — mode=modify가 아닌 mode=add (신규 디렉토리) + 사용자 기능 0개 (health check만) + 단일 환경 운영 (stg/prod 무관). 후속 이슈(#3 인증)에서 보안 리스크 본격화 (15-risk RISK-03).

## 2. 리스크 상세

### FRISK-01: uv lockfile cross-platform 차이

- **시나리오**: uv는 platform-specific 의존성을 lockfile에 명시. 작성자(Windows) 환경에서 sync 후 머지된 lockfile이 CI(Linux) 또는 다른 개발자(Mac)에서 dependency resolution 실패.
- **영향**: 신규 개발자 환경 셋업 지연 (수 분~수십 분).
- **가능성**: 본 이슈 의존성이 순수 Python (FastAPI, SQLAlchemy, aiosqlite, alembic, passlib, python-jose, pydantic-settings, ruff, pytest) → C 확장 적음. 그래도 bcrypt/cryptography는 platform-specific wheels 존재.
- **완화**:
  - pyproject.toml `requires-python = ">=3.11,<3.12"` 핀
  - uv가 자동으로 cross-platform lockfile 생성 (uv 0.5+ 기본 동작)
  - CI에서 Linux 환경 실행 → 가장 흔한 cross-platform 케이스 검증
- **Trigger**: 작성자 외 1인이 fresh clone 후 `uv sync` 실패 → 즉시 issue 신설.

### FRISK-02: Alembic async env.py 설정 오류

- **시나리오**: Alembic 기본 init은 sync 모드. async SQLAlchemy 사용 시 `env.py`를 async 모드로 수정 필요. 잘못 설정 시 `alembic upgrade head`가 deadlock 또는 silent fail.
- **영향**: AC-03 인수 기준 미통과 → PR 머지 차단.
- **가능성**: Alembic 공식 async template 예제 존재 + uvicorn lifespan에서 검증 가능.
- **완화**:
  - C4 커밋 후 `uv run alembic upgrade head` + `uv run alembic current` 실행 결과 확인 (plan §4)
  - `env.py`에 `from sqlalchemy.ext.asyncio import async_engine_from_config` 명시적 사용
  - Alembic 공식 async cookbook 패턴 채택 — `run_async_migrations()` 헬퍼

### FRISK-03: backend-ci.yml 워크플로 첫 실행 실패

- **시나리오**: GitHub Actions에서 `astral-sh/setup-uv@v3` 액션 사용. action 버전 호환성·캐시 키 충돌·Python 버전 setup 순서 오류로 첫 실행 실패.
- **영향**: PR status check FAIL → 머지 차단.
- **가능성**: 공식 action 사용 + uv 0.5+ stable. 그래도 매트릭스 신설 시 첫 실행은 종종 troubleshoot 필요.
- **완화**:
  - 단순 워크플로 — Linux ubuntu-latest 1개만 (Mac/Win 매트릭스 X)
  - C6 커밋 후 ADR-0047 양축 검증으로 *로컬 manual reproduction* 먼저 → 차이 즉시 catch
  - 실패 시 PR comment + plan §5에 추가 결정으로 명시 (uv setup action 버전 핀 등)

### FRISK-04: LOCAL.md §3.1 명령 PowerShell 미호환

- **시나리오**: LOCAL.md §3.1 명령이 bash 문법(`&&`, `cd` chaining)으로 작성됨. 작성자(Windows PowerShell)는 동작하지만 PowerShell 5.1 (Win10 default)에서는 `&&` 미지원.
- **영향**: Windows 신규 개발자가 LOCAL.md 명령 그대로 실행 실패.
- **가능성**: PowerShell 7+ (Win11/cross-platform) 기본에서는 `&&` 지원. PS 5.1만 문제.
- **완화**:
  - LOCAL.md §3.1에 *shell 가정 명시* — "PowerShell 7+ 또는 bash 기준. PS 5.1은 명령 분리 실행".
  - 단일 명령씩 줄 분리 권장 — `&&` 의존도 낮춤.
  - 본 이슈는 author가 PS에서 직접 실 검증 (Win11 PS 7) → AC-06 통과 시 자동 catch.

### FRISK-05: JWT_SECRET placeholder 오용

- **시나리오**: `.env.example`의 placeholder `JWT_SECRET=changeme-please-generate-random-32-chars`를 신규 개발자가 그대로 `.env`에 복사 후 production-like 환경에 배포.
- **영향**: 토큰 변조 가능 → 인증 우회 (단, 본 프로젝트는 학습 컨텍스트 + 단일 환경이므로 실제 영향 미미).
- **가능성**: 학습 컨텍스트, 단일 dev profile, 외부 노출 없음 → 매우 낮음.
- **완화**:
  - placeholder 형식에 명확한 "changeme-please-generate-random-32-chars" 키워드 포함 (육안 catch)
  - 후속 이슈 #3에서 startup 시 `JWT_SECRET == "changeme-please-generate-random-32-chars"`이면 stderr 경고 + 1초 sleep (UX nudge)
  - LOCAL.md §3.1에 `openssl rand -base64 32` 또는 `python -c "import secrets; print(secrets.token_urlsafe(32))"` 시크릿 생성 명령 안내

## 3. High 등급 단계적 롤아웃

**N/A** — High 등급 0건. mode=add 최소 침습으로 진행. 단계적 롤아웃 plan 불필요.

(참고: 15-risk.md RISK-03 보안은 시스템 차원 High이나 본 이슈가 도입하는 보안 surface는 0 — JWT/bcrypt 실 구현은 Issue #3. 본 PR은 env 키 정의만.)

## 4. 데이터 영속성 변경

- **신규 DB 파일**: `backend/data/realworld.db` (SQLite, gitignore). Alembic init revision은 빈 upgrade/downgrade → schema 0개 테이블 (단, `alembic_version` 테이블 1개 자동 생성).
- **마이그레이션 영향**: 후속 이슈(#2 User, #6 Comment)가 본 PR의 `0001_initial`을 `down_revision`으로 참조 → 본 PR의 revision id `0001` 변경 시 후속 PR 깨짐. **revision id 고정 (rollback 시 본 PR git revert 후 후속 PR 재작성 필요).**
- **데이터 손실 위험**: 본 PR 단독 회귀 시 0건 (스키마 0개). 머지 후 회귀는 후속 이슈 migration history 깨짐 → 별도 rollback procedure 필요 (Rollback 전략 §5).

## 5. 15-risk.md 갱신 항목

본 이슈로 인한 시스템 차원 리스크 갱신 0건 — FRISK-01 ~ 05 모두 *본 PR 한정 로컬 리스크*. 15-risk.md의 RISK-01~08과 별개.

후속 이슈에서 갱신될 항목 (참고):
- Issue #3 머지 후: RISK-03 (보안) 등급·완화 상태 갱신 (bcrypt/JWT 실 구현 완료).
- Issue #5 머지 후: RISK-04 (퍼포먼스) seed + p95 측정 결과 반영.
- Issue #9 머지 후: RISK-04 (FCP) 측정 결과 반영.
