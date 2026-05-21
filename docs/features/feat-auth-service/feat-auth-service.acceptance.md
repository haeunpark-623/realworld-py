---
doc_type: feature-acceptance
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-N-03, R-N-04]
  F-ID: [F-01]
  supersedes: null
---

# feat-auth-service — Acceptance Criteria

> Issue #3. 8 AC + 8 DoD. P10 AI 게이트가 AC 자동 검증, P14 휴먼 게이트가 DoD 사람 검증.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — Given/When/Then 8건 + DoD 8건 + 비기능·회귀 |

## 1. 인수 기준 (Given/When/Then)

### AC-01: utils/security 모듈 import + bcrypt 마커
- **Given** 본 PR 머지 후
- **When** `cd backend && uv run python -c "from realworld.utils.security import hash_password, verify_password; h = hash_password('test'); print(h[:7], verify_password('test', h), verify_password('wrong', h))"` 실행
- **Then** stdout에 `$2b$12$ True False` 출력 + exit 0. bcrypt 라운드 12 마커 + verify 양/음성 검증 PASS (R-N-03)

### AC-02: utils/jwt 모듈 encode/decode 라운드트립
- **Given** 본 PR 머지 후 + `JWT_SECRET`이 .env에서 로드된 상태
- **When** `cd backend && uv run python -c "from realworld.utils.jwt import encode_token, decode_token; t = encode_token(42); p = decode_token(t); print(p['sub'])"` 실행
- **Then** stdout에 `42` 출력 + exit 0. JWT_SECRET 환경변수 로드 검증 (R-N-04)

### AC-03: errors.py 도메인 예외 6 클래스 정의
- **Given** 본 PR 머지 후
- **When** `cd backend && uv run python -c "from realworld.errors import RealWorldError, DuplicateEmail, DuplicateUsername, InvalidCredentials, InvalidToken, ExpiredToken, Forbidden, NotFound; print(DuplicateEmail.status_code, InvalidCredentials.status_code, Forbidden.status_code, NotFound.status_code)"` 실행
- **Then** stdout에 `422 401 403 404` 출력 + exit 0. HTTP status code 매핑 검증

### AC-04: AuthService 3 메서드 시그니처 (async)
- **Given** 본 PR 머지 후
- **When** `cd backend && uv run python -c "import inspect; from realworld.services.auth import AuthService; print(sorted(m for m in dir(AuthService) if not m.startswith('_')))"` 실행
- **Then** 출력에 `['authenticate', 'get_current_user', 'register']` 포함. 각각 `inspect.iscoroutinefunction(getattr(AuthService, m))` True

### AC-05: deps/auth require_auth FastAPI 의존성 시그니처
- **Given** 본 PR 머지 후
- **When** `cd backend && uv run python -c "import inspect; from realworld.deps.auth import require_auth; print(inspect.iscoroutinefunction(require_auth), list(inspect.signature(require_auth).parameters.keys()))"` 실행
- **Then** 출력 `True ['authorization', 'session']` (또는 동등 이름). FastAPI Depends 의존성으로 사용 가능

### AC-06: pytest 단위 테스트 — security 3 + jwt 3 PASS
- **Given** 본 PR 머지 후
- **When** `cd backend && uv run pytest tests/unit/test_security.py tests/unit/test_jwt.py -v` 실행
- **Then** `6 passed` + exit 0. 세부: hash 마커 / verify 양 / verify 음 / encode-decode round-trip / expired → ExpiredToken / tampered → InvalidToken

### AC-07: pytest 단위 테스트 — auth_service 8 PASS
- **Given** 본 PR 머지 후
- **When** `cd backend && uv run pytest tests/unit/test_auth_service.py -v` 실행
- **Then** `8 passed` + exit 0. 세부: register 3 (정상 / DuplicateEmail / DuplicateUsername) + authenticate 2 (정상 → JWT / InvalidCredentials) + get_current_user 3 (정상 / ExpiredToken / InvalidToken — user_id 없음)

### AC-08: 회귀 — 기존 6 테스트 무영향
- **Given** 본 PR 머지 후
- **When** `cd backend && uv run pytest -v` 실행 (전체)
- **Then** `20 passed` + exit 0 (3 health + 3 user_repo 회귀 + 3 security + 3 jwt + 8 auth_service 신규)

## 2. Definition of Done (D-06)

본 8 DoD 항목은 Issue #3 body의 7 DoD checklist + 본 PR 표준 1 (CI green) 일치. P14 휴먼 게이트에서 사람이 미체크 → 체크로 전환.

- [ ] D-03-1 `utils/security.py` hash_password / verify_password (bcrypt)
- [ ] D-03-2 `utils/jwt.py` encode_token / decode_token (python-jose HS256)
- [ ] D-03-3 `errors.py` 6 도메인 예외 (DuplicateEmail/Username, InvalidCredentials, InvalidToken, ExpiredToken, Forbidden, NotFound) + status_code 속성
- [ ] D-03-4 `services/auth.py` AuthService 3 메서드 (register / authenticate / get_current_user)
- [ ] D-03-5 `deps/auth.py` require_auth (FastAPI Depends)
- [ ] D-03-6 단위 테스트 — security 3 + jwt 3 + auth_service 8 = 14건 PASS
- [ ] D-03-7 R-N-03 검증 (`$2b$12$` 마커) + R-N-04 검증 (JWT_SECRET env 로드)
- [ ] D-03-8 GitHub Actions `backend-ci` workflow green (lint + pytest 5 step)

## 3. 비기능 인수

- **R-N-03 bcrypt**: AC-01에서 `$2b$12$` 마커 + verify 양/음성 직접 검증. round=12 default 정합.
- **R-N-04 시크릿 환경변수**: AC-02에서 JWT_SECRET 환경변수 로드 검증 (encode/decode가 .env에서 secret 읽음). 본 PR은 .env.example 변경 0 (I-01에서 이미 정의).
- **R-N-06 단일 환경 운영**: dev 1 profile만. stg/prod N/A (RFP §NFR-06).
- **보안 (시크릿 노출)**: 단위 테스트의 dummy password `"correct horse battery staple"` 또는 `"testpassword"`는 placeholder만 사용. .env 실제 값 / API 키 / 실제 JWT secret 코드에 0건.
- **보안 (예외 메시지)**: 한글 메시지 ("이메일이 이미 사용 중입니다", "인증 정보가 올바르지 않습니다" 등). I-04 exception_handlers가 직렬화. 본 PR은 클래스 정의만.
- **성능**: AuthService.get_current_user의 DB 조회 1 요청당 1회. R-N-01 p95 < 200ms 여유 (R-N-01 검증은 I-05 책임).

## 4. 회귀 인수

- **기존 6 테스트**: AC-08에서 전수 회귀 — 3 health + 3 user_repo. 본 PR 코드 변경이 import 경로 무관 (신규 모듈만).
- **UserRepo 4 메서드**: 기존 3 (find_by_email/find_by_username/create) 시그니처 변경 0 + find_by_id 1 추가. I-02 단위 테스트 3 PASS 유지.
- **Alembic 0002 head**: 본 PR DB 스키마 변경 0. alembic upgrade head 결과 동일.
- **GitHub Actions backend-ci**: I-01의 5 step workflow 그대로 적용. 본 PR에서 추가 step 0건.
- **uv.lock 변경**: 의존성 추가 0건 (passlib/python-jose 이미 I-01에 있음). uv sync --frozen drift 0.
