---
doc_type: feature-brief
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

# feat-auth-service — Feature Brief

> Issue #3 — `feat(backend): I-03 AuthService + bcrypt + JWT util + Auth Middleware`. utils/security(bcrypt) + utils/jwt(python-jose HS256) + services/auth(register/authenticate/get_current_user) + deps/auth(require_auth) + errors(도메인 예외) + 단위 테스트 8건.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — `/flow-feature 3` 진입. mode=add 자동 결정 (type:feature 라벨 + 부정 시그널 0건) |

## 1. 한 줄 의도

I-02 User 모델·UserRepo 위에 RealWorld Auth 도메인의 *비즈니스 계층*(bcrypt 해시 유틸 + JWT HS256 인코더/디코더 + AuthService 3 메서드 + FastAPI require_auth 의존성 + 도메인 예외 클래스)을 도입한다. I-04(users router)가 본 PR의 AuthService·require_auth를 의존성으로 가져다 쓴다.

## 2. 사용자 가치

본 PR 자체는 *외부 사용자에게 보이는 동작 변경 0* (HTTP 라우트 신설 0건). 다만 후속 I-04에서 `POST /api/users`(회원가입, R-F-01)·`POST /api/users/login`(로그인, R-F-02)·`GET /api/user`(현재 사용자, R-F-03) 라우트가 가능해지려면 비즈니스·인증 계층이 먼저 자리잡혀야 한다 — 본 PR은 RealWorld 인증·인가의 *필수 선행 인프라*.

내부 가치:
- **보안 원칙 코드화**: bcrypt round=12 + JWT HS256 + 만료 시간 환경변수가 utils 계층에 한 곳에 모이고, AuthService가 평문 비밀번호를 절대 저장하지 않는다 (RFP §NFR-03, R-N-03).
- **인증 의존성 추상화**: FastAPI `Depends(require_auth)` 패턴으로 라우트가 `current_user: User`를 1줄로 받게 됨 — I-04 라우트 구현 부담 최소화.
- **도메인 예외 체계 수립**: `DuplicateEmail/Username`, `InvalidCredentials`, `InvalidToken`, `ExpiredToken`, `Forbidden`, `NotFound` 6종이 `errors.py`에 박혀 한글 메시지 직렬화(I-04 exception_handlers)의 기반이 된다.

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 (I-02 머지 직후) | 변경 후 (본 PR 머지 후) |
| --- | --- | --- |
| backend 패키지 | `realworld/{config,db,main}.py` + `models/` + `repositories/` | + `realworld/utils/{__init__,security,jwt}.py` + `realworld/services/{__init__,auth}.py` + `realworld/deps/{__init__,auth}.py` + `realworld/errors.py` |
| 비밀번호 해시 | 없음 (`password_hash` 컬럼은 빈 슬롯) | bcrypt(passlib) round=12 — `hash_password`, `verify_password` 2 함수 |
| JWT | 없음 (JWT_SECRET/JWT_ALG/JWT_EXPIRE_MINUTES env만 정의) | python-jose HS256 — `encode_token(user_id)`, `decode_token(token) -> payload` 2 함수 |
| 비즈니스 서비스 | 없음 | `AuthService.register(username, email, password) -> User` + `authenticate(email, password) -> str(JWT)` + `get_current_user(token) -> User` |
| FastAPI 의존성 | 기본 `get_db_session`만 (I-01) | + `require_auth: User = Depends(...)` (Authorization 헤더 Bearer 파싱) |
| 도메인 예외 | 없음 | `RealWorldError` 베이스 + 6 서브클래스 (HTTP status 매핑 속성 포함) |
| 단위 테스트 | health 3건 + UserRepo 3건 = 6건 | + `test_security.py` (hash/verify) + `test_jwt.py` (encode/decode round-trip + 만료) + `test_auth_service.py` (register 3 / authenticate 2 / get_current_user 3) — 총 약 8~12건 추가 |
| 후속 의존 | (없음) | I-04 users router가 AuthService 3 메서드 + require_auth 의존성 사용 |

## 4. 모드 자동 감지 결과

- **결정 모드**: `add` (자동 결정, 부정 시그널 0건)
- **시그널**:
  - 라벨: `type:feature` ✅ (add 양의 시그널)
  - 자연어: "AuthService + bcrypt + JWT util + Auth Middleware" — 신규 동작
  - 부정 시그널 (bug / design / modify): 0건
- **수동 override**: 없음. ADR-0032 §2.1 무질문 자동 결정 발동.
- **결정 시각**: 2026-05-21

## 5. 영향 범위

| 영역 | 변경 | 비고 |
|---|---|---|
| backend 코드 | 신규: `utils/__init__.py`, `utils/security.py`, `utils/jwt.py`, `services/__init__.py`, `services/auth.py`, `deps/__init__.py`, `deps/auth.py`, `errors.py` (8 신규 파일) | 신규 디렉토리 3개(utils/services/deps) — 12-scaffolding §1 트리 정합 |
| 의존성 | 변경 0건 — `passlib[bcrypt]`·`python-jose[cryptography]` 이미 I-01에 명시됨 | `uv sync --frozen` drift 0 |
| 테스트 | 신규: `tests/unit/test_security.py`, `tests/unit/test_jwt.py`, `tests/unit/test_auth_service.py` (3 파일, 약 8~12 케이스) | 14-wbs §2 I-03 DoD "단위 테스트 8건" 충족 |
| conftest fixture | 추가 없음 — 기존 `db_session` (I-02) 재사용 | UserRepo·AuthService 모두 AsyncSession 의존 |
| Alembic | 변경 0건 — 본 PR DB 스키마 변경 없음 | I-02 0002 head 유지 |
| 환경변수 | 변경 0건 — JWT_SECRET/JWT_ALG/JWT_EXPIRE_MINUTES 이미 I-01 .env.example/config.py에 있음 | 본 PR은 *사용*만 |
| 문서 | 14-wbs §2 I-03 status:in-review 갱신, INDEX.md v0.7 갱신 | P13 docs-update |
| UI / FE | 영향 0 | ui_changed=false |
| 부팅 자산 | 변경 0건 (.env.example/LOCAL.md/uv.lock/alembic 모두 동일) | 단일 환경 운영 N/A (dev only) |

**3+영역 변경**: backend 코드 / 테스트 / 문서 (3 영역) → PR Touched Areas 절 필수.

## 6. 비목표

- **HTTP 라우트** (`POST /api/users`, `POST /api/users/login`, `GET /api/user`) — I-04 책임. 본 PR은 *비즈니스 서비스 + 의존성*만.
- **Pydantic 요청/응답 스키마** (`schemas/user.py`) — I-04 책임. 본 PR의 AuthService는 *primitive 타입*(str, int)만 받음.
- **FastAPI exception_handlers 등록** — I-04 책임. 본 PR은 *예외 클래스 정의*만 (errors.py).
- **Article·Comment 권한 검증** — I-04 (article 작성자 검증) + I-06 (comment 작성자 검증). 본 PR의 `require_auth`는 *로그인 여부*만 검증.
- **토큰 블랙리스트 / refresh token / OAuth 외부 IdP** — RealWorld MVP Out of Scope (RFP §3, RFP §Out of Scope §4).
- **bcrypt round 동적 튜닝** — 고정값 12. R-N-03 검증은 단위 테스트에서 hash 결과 `$2b$12$` 시작 확인으로 대체.
- **JWT 알고리즘 교체 / 키 회전** — `JWT_ALG=HS256` 환경변수 고정. R-N-04는 secret 환경변수 누락 시 부팅 실패 보장만 (config.py에서 default 값 placeholder 노출).

## 7. Open Questions

| Q | 결정 |
|---|---|
| bcrypt round 값 | 12 (passlib `CryptContext(schemes=["bcrypt"])` 기본). round 1 라이브러리 default에 위임. R-N-03 검증은 hash 결과 `$2b$12$` 시작 확인으로 |
| JWT 만료 시간 | env `JWT_EXPIRE_MINUTES=10080` (7일, I-01 .env.example 기본값). exp 클레임은 UTC 기준 |
| JWT 클레임 구조 | `{sub: str(user.id), exp: datetime}` 최소 형식. RealWorld spec 호환 |
| 토큰 디코드 실패 케이스 | python-jose `JWTError` → 도메인 `InvalidToken` 변환. `ExpiredSignatureError` → `ExpiredToken` (별도 분기 — 한글 메시지 다름) |
| require_auth 헤더 형식 | `Authorization: Token <JWT>` (RealWorld spec) — Bearer 아님. 09-api-spec §1 인증 헤더 명시 정합 |
| require_auth 누락 시 응답 | 401 Unauthorized + 한글 메시지 "인증이 필요합니다" — I-04 exception_handler가 직렬화 |
| `errors.py`의 status code 매핑 | 베이스 클래스 `status_code` 속성 — `DuplicateEmail/Username=422`, `InvalidCredentials=401`, `InvalidToken/ExpiredToken=401`, `Forbidden=403`, `NotFound=404`. I-04 handler가 사용 |
| `get_current_user`에 DB 의존 여부 | DB 의존 (JWT decode → user_id → UserRepo.find_by_id) — 사용자 삭제 후 토큰 잔존 케이스 차단. 단위 테스트는 in-memory DB로 검증 |
