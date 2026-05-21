---
doc_type: feature-contract
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

# feat-auth-service — Change Contract

> Issue #3. AuthService 3 메서드 + utils/security(bcrypt) + utils/jwt(python-jose HS256) + deps/auth(require_auth) + errors(6 도메인 예외) + 단위 테스트 8건+.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — §0 5행 + §2 13 Before/After + §3 6 Call Sites |

## 0. 참조 정본 ID (Referenced-IDs)

본 PR 작업 시 selective read 진입점 (ADR-0018). 후속 P4 implementation-planner가 본 표를 기반으로 *부분 읽기*로 plan 작성.

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| R-ID (SRS) | `docs/planning/04-srs/04-srs.md` §R-F-01~03 / §R-N-03 / §R-N-04 | R-F-01 (회원가입 비즈니스 로직), R-F-02 (로그인 인증), R-F-03 (현재 사용자 — JWT 기반), R-N-03 (bcrypt 해시), R-N-04 (JWT secret 환경변수) |
| F-ID (PRD) | `docs/planning/05-prd/05-prd.md` §F-01 | F-01 (Auth — register/login/me 서비스 + 미들웨어) |
| Module (LLD) | `docs/planning/08-lld-module-spec/08-lld-module-spec.md` §1 모듈 개요 + §3 M-Auth-Service 책임 + §6 인증 미들웨어 | M-Auth-Service (UserRepo 의존), M-Auth-Dep (FastAPI Depends require_auth) |
| Scaffolding | `docs/planning/12-scaffolding/python.md` §1 트리 (`realworld/utils/`, `realworld/services/`, `realworld/deps/`, `realworld/errors.py`, `tests/unit/`) | backend 디렉토리 구조 (utils/services/deps 신규 폴더) |
| Conventions | `docs/planning/11-coding-conventions/11-coding-conventions.md` §1 명명 + §3 에러 코드 + §2 예외 클래스 PascalCase | 함수 snake_case (`hash_password`, `verify_password`, `encode_token`, `decode_token`) / 서비스 PascalCase 단수 (`AuthService`) / 예외 PascalCase (`DuplicateEmail`, `InvalidCredentials`) |

## 1. 변경 의도

I-02 User 모델·UserRepo 위에 RealWorld Auth 도메인의 *비즈니스·인증 계층*을 도입한다:

1. **utils/security.py** — passlib bcrypt context. `hash_password(plain: str) -> str` + `verify_password(plain: str, hashed: str) -> bool` 2 함수. round=12 (라이브러리 default).
2. **utils/jwt.py** — python-jose HS256. `encode_token(user_id: int) -> str` + `decode_token(token: str) -> dict` 2 함수. exp 클레임 자동 설정 (`JWT_EXPIRE_MINUTES` 환경변수). 만료/서명 오류 시 도메인 예외 변환.
3. **errors.py** — `RealWorldError` 베이스 + 6 서브클래스 (`DuplicateEmail`, `DuplicateUsername`, `InvalidCredentials`, `InvalidToken`, `ExpiredToken`, `Forbidden`, `NotFound`). 각 클래스에 `status_code` 속성 + 한글 메시지.
4. **services/auth.py** — `AuthService(session: AsyncSession)`. `register(username, email, password) -> User` (UserRepo로 중복 검사 + hash 저장) / `authenticate(email, password) -> str` (JWT 발급) / `get_current_user(token) -> User` (JWT decode + UserRepo.find_by_id).
5. **deps/auth.py** — `async def require_auth(authorization: str = Header(...), session: AsyncSession = Depends(get_db)) -> User`. RealWorld `Authorization: Token <JWT>` 헤더 파싱 → AuthService.get_current_user 호출.
6. **단위 테스트 8건+** — `test_security.py` (hash/verify 라운드 트립 + `$2b$12$` 마커 확인) + `test_jwt.py` (encode/decode 라운드 트립 + 만료 토큰 → ExpiredToken + 변조 토큰 → InvalidToken) + `test_auth_service.py` (register 3 / authenticate 2 / get_current_user 3).

본 PR의 *외부 사용자 동작 영향 0* (라우트 0건). I-04 진입을 위한 필수 선행 인프라.

## 2. Before / After

| 항목 | Before | After |
| --- | --- | --- |
| `realworld/utils/__init__.py` | 없음 | 빈 패키지 마커 |
| `realworld/utils/security.py` | 없음 | `from passlib.context import CryptContext` + `pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")` + `hash_password(plain) -> str` + `verify_password(plain, hashed) -> bool` |
| `realworld/utils/jwt.py` | 없음 | `from jose import jwt, JWTError, ExpiredSignatureError` + `encode_token(user_id: int) -> str` (sub=str(user_id), exp=now+JWT_EXPIRE_MINUTES) + `decode_token(token: str) -> dict` (ExpiredSignatureError → ExpiredToken, JWTError → InvalidToken) |
| `realworld/errors.py` | 없음 | `class RealWorldError(Exception)` 베이스 + `status_code: int` + `message: str` 속성. 6 서브클래스: `DuplicateEmail/Username (422)`, `InvalidCredentials (401)`, `InvalidToken/ExpiredToken (401)`, `Forbidden (403)`, `NotFound (404)`. 모두 한글 메시지 |
| `realworld/services/__init__.py` | 없음 | 빈 패키지 마커 |
| `realworld/services/auth.py` | 없음 | `class AuthService` + `__init__(session: AsyncSession)`. `async register(username, email, password) -> User` (UserRepo.find_by_email/find_by_username 중복 검사 → DuplicateEmail/Username 또는 UserRepo.create with hash_password) / `async authenticate(email, password) -> str` (find_by_email + verify_password → encode_token, 실패 시 InvalidCredentials) / `async get_current_user(token) -> User` (decode_token → user_id → UserRepo.find_by_id, 미존재 시 InvalidToken) |
| `realworld/repositories/user.py` | I-02 3 메서드 (find_by_email/find_by_username/create) | + `find_by_id(user_id: int) -> User \| None` (1 메서드 추가, AuthService.get_current_user용) |
| `realworld/deps/__init__.py` | 없음 | 빈 패키지 마커 |
| `realworld/deps/auth.py` | 없음 | `async require_auth(authorization: str \| None = Header(default=None, alias="Authorization"), session: AsyncSession = Depends(get_db_session)) -> User`. None/빈 헤더 → InvalidToken. "Token <jwt>" prefix 파싱. AuthService(session).get_current_user(jwt) 호출 |
| `realworld/db.py::get_db_session` | I-01에서 `get_db` 또는 동등 이름 | 본 PR이 `Depends(get_db_session)` 임포트 — 기존 함수 그대로 사용 (이름 변경 없음) |
| `tests/unit/test_security.py` | 없음 | 2~3 케이스: `test_hash_password_returns_bcrypt_marker` ($2b$12$ 시작) / `test_verify_password_matches` / `test_verify_password_rejects_wrong` |
| `tests/unit/test_jwt.py` | 없음 | 3 케이스: `test_encode_decode_round_trip` / `test_decode_expired_raises_expired_token` (monkeypatch JWT_EXPIRE_MINUTES=-1 또는 시간 조작) / `test_decode_tampered_raises_invalid_token` |
| `tests/unit/test_auth_service.py` | 없음 | 8 케이스: register 3 (정상 / 이메일 중복 / 사용자명 중복) + authenticate 2 (정상 → JWT 발급 / 비밀번호 불일치 → InvalidCredentials) + get_current_user 3 (정상 토큰 → User / 만료 토큰 → ExpiredToken / 존재하지 않는 user_id → InvalidToken) |

## 3. 호출자·의존자 (Call Sites)

본 PR 머지 후 *직접 의존하는 후속 모듈*과 *본 PR이 의존하는 기존 모듈*.

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| `realworld/repositories/user.py::UserRepo` (I-02) | AuthService가 find_by_email/find_by_username/create 호출 + 신규 find_by_id 호출 | 본 PR이 find_by_id 1 메서드 추가 |
| `realworld/models/user.py::User` (I-02) | AuthService.register/get_current_user 반환 타입, AuthService.authenticate 내부 사용 | 변경 없음. 시그니처 그대로 활용 |
| `realworld/db.py::get_db_session` (I-01) | deps/auth.py에서 `Depends(get_db_session)` 사용 | 변경 없음. 본 PR 사용자 |
| `realworld/config.py::get_settings` (I-01) | utils/jwt.py에서 JWT_SECRET/JWT_ALG/JWT_EXPIRE_MINUTES 접근 | 변경 없음. 본 PR 사용자 |
| 후속 `realworld/routers/users.py` (I-04 예정) | `AuthService(session).register/.authenticate` 호출 + `Depends(require_auth)` 사용 | 본 PR에서 인터페이스 확정. I-04가 import |
| 후속 `realworld/routers/articles.py` (I-04 예정) | `Depends(require_auth)`로 `current_user: User` 주입 — 작성자 검증 (I-04 책임) | 본 PR이 require_auth 패턴 시연 |

## 4. Backward Compatibility

**N/A — neutral**. 본 PR은 *신규 도입*만. 기존 동작 변경 0.

- I-01 health check 3 라우트·테스트: 무영향
- I-02 UserRepo 3 메서드 + 단위 테스트 3건: 무영향 (본 PR에서 `find_by_id` 1 메서드 추가, 기존 3 메서드 시그니처 변경 없음 — 단순 확장)
- 기존 Alembic 0001/0002 head: 그대로 유지 (본 PR DB 스키마 변경 0)
- 기존 `tests/test_health.py` + `tests/unit/test_user_repo.py`: 회귀 0건 보장

**의존성 라이브러리**: `passlib[bcrypt]`·`python-jose[cryptography]` 모두 I-01 `pyproject.toml`에 이미 명시 + `uv.lock` 락 적용. 본 PR에서 의존성 추가 0건 — `uv sync --frozen` drift 0.

**환경변수**: I-01에서 이미 `JWT_SECRET`/`JWT_ALG`/`JWT_EXPIRE_MINUTES` 3개 정의 + config.py·.env.example 양축. 본 PR은 *사용*만.

## 5. Rollback 전략

**1차 (PR 머지 전 회귀)**: 본 PR open 상태에서 close + 브랜치 삭제. 영향 0.

**2차 (PR 머지 후 회귀)**:
1. **revert PR**: `git revert <merge_sha>` 후 별도 PR. utils/services/deps/errors 및 추가된 UserRepo.find_by_id 일괄 삭제. DB 스키마 변경 0이라 alembic downgrade 불필요.
2. **revert 영향 (cascade)**:
   - I-04 미진입 상태: 무영향. UserRepo 3 메서드 그대로 유지
   - I-04 머지 후 본 PR revert: *블로커* — I-04도 함께 revert 필요. users router·articles router가 AuthService·require_auth에 의존
3. **부분 회귀 (hotfix)**: bcrypt round 변경 또는 JWT_EXPIRE 조정 같은 *config 값* 수정은 환경변수만으로 충분. 별도 PR 불필요

**Trigger 조건**:
- 단위 테스트 30% 이상 실패 → revert PR
- bcrypt 마커가 `$2b$`로 시작 안 함 (passlib 동작 이상) → 즉시 revert
- JWT decode가 만료 토큰을 통과시킴 (보안 결함) → 즉시 revert + Issue 신설
- 단순 import 에러·typo → hotfix PR 권장 (revert 부담 큼)

## 6. 비목표

- HTTP 라우트 (`POST /api/users`, `POST /api/users/login`, `GET /api/user`) — I-04
- Pydantic 요청/응답 스키마 (`schemas/user.py`) — I-04
- FastAPI exception_handlers 등록 (도메인 예외 → HTTP 응답 매핑) — I-04. 본 PR은 *예외 클래스 정의*만
- Article·Comment 작성자 권한 검증 — I-04 / I-06. 본 PR `require_auth`는 *로그인 여부*만 검증
- 토큰 블랙리스트 / refresh token / 로그아웃 무효화 — RealWorld MVP Out of Scope
- OAuth / 외부 IdP — RealWorld MVP Out of Scope
- bcrypt round 동적 조정 / 알고리즘 마이그레이션 — 고정 round=12
- JWT 알고리즘 교체 (HS256 → RS256 등) / 키 회전 — 환경변수 고정
- 통합 테스트 (HTTPX 클라이언트로 라우트 통한) — I-04 책임
