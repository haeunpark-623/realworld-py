---
doc_type: feature-risk
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

# feat-auth-service — Feature Risk

> Issue #3. 7 FRISK — 6 Low + 1 Medium (JWT secret). High 0건 → 단계적 롤아웃 N/A. 데이터 영속성 변경 0건.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 7 FRISK (6 Low + 1 Medium). 15-risk.md RISK-03 보안 1행 갱신 |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| FRISK-01 | passlib + bcrypt 4.x 백엔드 경고로 인한 부팅 실패 가능 | 3 | 2 | Low |
| FRISK-02 | JWT secret 기본값(`changeme-...`)으로 prod 부팅 후 토큰 위조 | 5 | 2 | Medium |
| FRISK-03 | python-jose의 만료 토큰 검증 누락 가능 (옵션 설정 실수) | 4 | 1 | Low |
| FRISK-04 | AuthService.register의 동시성 UNIQUE 충돌 미처리 (race) | 2 | 2 | Low |
| FRISK-05 | require_auth 헤더 prefix `Token ` vs `Bearer ` 혼동 | 2 | 2 | Low |
| FRISK-06 | errors.py 도메인 예외와 FastAPI HTTPException 미연결 (I-04 의존) | 2 | 1 | Low |
| FRISK-07 | passlib bcrypt 4.x AttributeError warning이 단위 테스트 stdout 오염 | 1 | 3 | Low |

등급 계산: 영향 × 가능성 (최대 25). 9 이하 = Low, 10~14 = Medium, 15+ = High.

## 2. 리스크 상세

### FRISK-01: passlib + bcrypt 4.x 부팅 실패
- **시나리오**: passlib 1.7.4가 bcrypt 4.x의 `__about__` 모듈에 접근하다 AttributeError → 부팅 자체는 실패 안 하나 *경고 출력*. 일부 환경에서 hash_password 호출 자체가 실패 보고된 사례 있음 (passlib 이슈 트래커).
- **완화**: I-01에서 의존성 `passlib[bcrypt]>=1.7.4,<2.0.0` + `bcrypt` extras로 박힘. C2 단위 테스트가 `hash_password("test")` 실행해 즉시 검증.
- **검출**: pytest test_hash_password_starts_with_bcrypt_marker가 실패하면 즉시 발각.
- **롤백**: pyproject.toml에 `bcrypt<4` 핀 추가 + uv.lock 갱신. 별도 hotfix PR.

### FRISK-02: JWT secret 기본값 prod 부팅
- **시나리오**: `.env.example`의 `JWT_SECRET=changeme-please-generate-random-32-chars`이 실 환경에 노출되어 *토큰 위조 가능*. 본 PR 자체는 secret 관리 변경 0이지만, AuthService가 처음 secret을 *사용*하므로 책임 일부 전가됨.
- **완화 (본 PR 책임)**: utils/jwt.py가 부팅 시점에 `get_settings().JWT_SECRET`을 읽음 — 기본값 사용 감지 가능. I-03 단위 테스트는 실제 .env 값 사용 (in-memory가 아닌 환경변수 의존).
- **완화 (Out of Scope)**: prod 부팅 직전 `JWT_SECRET` 값이 placeholder인지 검사하는 startup 검증은 본 PR 비목표. 학습 과제는 dev 단일 환경 운영 (RFP §NFR-06)이라 prod 부팅 자체가 N/A.
- **검출**: 사람 검수 — .env 파일 직접 확인.
- **롤백**: secret 회전 (모든 토큰 무효화). 운영자 작업.

### FRISK-03: python-jose 만료 토큰 검증 누락
- **시나리오**: `jwt.decode(token, secret, algorithms=["HS256"])` 호출 시 옵션 미지정으로 만료 검증 skip 가능 (`options={"verify_exp": False}` 같은 옵션 실수).
- **완화**: 본 PR 정책 — `decode_token` 함수에서 옵션 *명시 안 함* (default = exp 검증 ON). C4 단위 테스트 `test_decode_expired_raises_expired_token`이 만료 토큰 → ExpiredSignatureError → ExpiredToken 변환을 직접 어서션.
- **검출**: C4 테스트가 실패하면 즉시 발각.
- **롤백**: decode_token 함수에 옵션 인자 명시.

### FRISK-04: AuthService.register 동시성 UNIQUE 충돌
- **시나리오**: 두 동시 요청이 같은 email로 register 호출 — find_by_email은 모두 None 반환, UserRepo.create 단계에서 한 쪽이 IntegrityError. 본 PR은 IntegrityError 명시적 처리 안 함.
- **완화**: RealWorld MVP는 단일 사용자 학습 부하 — 동시성 race 실제 발생 가능성 매우 낮음. SQLite는 단일 라이터로 직렬화. 추가 처리 부담 회피.
- **검출**: I-04 통합 테스트에서 발견 가능 (동시 register 시나리오는 통합 단계 외).
- **롤백**: I-04에서 IntegrityError → DuplicateEmail 변환 추가 (별도 이슈 또는 I-04 scope 내 흡수).

### FRISK-05: 헤더 prefix Token vs Bearer 혼동
- **시나리오**: 본 PR `require_auth`는 "Token <jwt>" prefix만 파싱. I-08 frontend가 "Bearer" 보내면 401. RealWorld spec은 "Token"이라 정합하나, 일반적 OAuth 관습은 "Bearer".
- **완화**: deps/auth.py 코드에 inline 주석 1줄 (RealWorld spec 출처). 09-api-spec §1에 헤더 형식 명시.
- **검출**: I-04 통합 테스트가 "Token " prefix로 호출, I-08 frontend 호출에서 일치 확인.
- **롤백**: ADR 신설 후 "Bearer"로 변경. 클라이언트 코드 동기 필요.

### FRISK-06: errors.py와 FastAPI HTTPException 미연결
- **시나리오**: 본 PR의 도메인 예외 (`DuplicateEmail` 등)가 FastAPI 라우트에서 raise되어도 *자동 변환 안 됨*. 500 Internal Server Error로 응답될 위험.
- **완화**: 본 PR scope = errors.py 클래스 정의만. I-04가 `app.add_exception_handler(RealWorldError, handler)` 등록 책임. 본 PR contract §6에 비목표 명시.
- **검출**: I-04 통합 테스트가 422/401/403/404 응답 확인.
- **롤백**: I-04와 묶여 cascade revert 또는 hotfix.

### FRISK-07: passlib bcrypt 4.x AttributeError warning
- **시나리오**: hash_password 호출 시 stderr/stdout에 `AttributeError: module 'bcrypt' has no attribute '__about__'` 1줄 경고 출력. ruff/pytest 결과에 영향 0.
- **완화**: 무시 (라이브러리 자체 버그, 동작 영향 0).
- **검출**: 사용자 가시 영향 0. 단위 테스트 결과 영향 0.
- **롤백**: pyproject.toml에 `bcrypt>=4.0.1,<4.1`로 pin (passlib 호환 패치 버전). 본 PR scope 외.

## 3. High 등급 단계적 롤아웃

**N/A** — High 등급 0건. 7 FRISK 중 1 Medium (FRISK-02 JWT secret prod 부팅), 6 Low. 학습 과제는 단일 dev 환경이라 FRISK-02 가능성 사실상 0. 단계적 롤아웃 불필요.

## 4. 데이터 영속성 변경

**N/A** — 본 PR DB 스키마 변경 0. Alembic 0002 head 유지. UserRepo find_by_id 1 메서드 추가는 *읽기 전용 쿼리*로 DB 데이터 변경 없음.

dev DB 영향:
- AuthService.register 호출 시 users 테이블에 row 추가 — 하지만 본 PR은 *테스트에서만* 호출 (in-memory aiosqlite). dev `data/realworld.db` 무영향.
- 단위 테스트 fixture `db_session`이 in-memory 사용 → 디스크 파일 생성 0.

## 5. 15-risk.md 갱신 항목

본 PR이 15-risk.md RISK-03 (보안) 단계적 검증 항목과 직접 연결됨:

- **RISK-03 갱신 후보**: "I-03 단위 테스트(bcrypt 마커 + JWT 검증)" 항목이 14-wbs §5 매핑 행에 이미 있음 → 본 PR 머지로 *체크 완료* 표시 가능. P13 docs-update에서 14-wbs §5 RISK-03 행에 PR #N 링크 추가.
- **RISK-04 (퍼포먼스) 미영향**: AuthService.get_current_user의 1 DB 조회 추가는 p95 < 200ms 여유 (R-N-01). I-05 100건 시드 + p95 측정에서 갱신 예상 — 본 PR 무관.

다음 이슈에서 갱신 후보:
- I-04 통합 테스트: 422/401 한글 응답 검증 — RISK-03 사용자 가시 검증
- I-05 100건 시드: p95 측정 갱신
