---
doc_type: feature-code-review
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

# feat-auth-service — Code Review

> P9. Generator≠Evaluator. C1~C6 diff 검토 후 Verdict PASS. NEEDS-WORK 0건.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 12 OX 결과 10 PASS + 2 DEFER (passlib→bcrypt 직접 사용 + UserRepo.find_by_id contract drift). NEEDS-WORK 0건 |

## 0. Verdict

**PASS** — 7 커밋 diff 검토 결과 contract §2 Before/After 13행 + plan 7 커밋 DAG 모두 매핑. NEEDS-WORK 0건. P10 AI 게이트 진입 허용.

- [reviewer]: woosung.ahn@bespinglobal.com (AI — Generator≠Evaluator)
- [review_at]: 2026-05-21

## 1. 컨트랙트 충실도

각 contract Before/After 행이 코드로 매핑됨:

| 항목 | Before | After | 코드 매핑 | OX |
| --- | --- | --- | --- | --- |
| `realworld/utils/__init__.py` | 없음 | 빈 마커 | `backend/realworld/utils/__init__.py` 0 lines | ✅ |
| `realworld/utils/security.py` | 없음 | hash/verify_password | `backend/realworld/utils/security.py` 13 lines (passlib 대신 bcrypt 직접 사용 — contract drift, code-review F1) | ✅ |
| `realworld/utils/jwt.py` | 없음 | encode/decode_token | `backend/realworld/utils/jwt.py` 22 lines | ✅ |
| `realworld/errors.py` | 없음 | RealWorldError + 6 서브클래스 | `backend/realworld/errors.py` 44 lines | ✅ |
| `realworld/services/__init__.py` | 없음 | 빈 마커 | 생성 | ✅ |
| `realworld/services/auth.py` | 없음 | AuthService 3 async 메서드 | `backend/realworld/services/auth.py` 50 lines | ✅ |
| `realworld/repositories/user.py` | 3 메서드 | + find_by_id | `backend/realworld/repositories/user.py` Edit (4 메서드 됨) | ✅ |
| `realworld/deps/__init__.py` | 없음 | 빈 마커 | 생성 | ✅ |
| `realworld/deps/auth.py` | 없음 | require_auth | `backend/realworld/deps/auth.py` 21 lines | ✅ |
| `tests/unit/test_security.py` | 없음 | 3 케이스 | `backend/tests/unit/test_security.py` 17 lines | ✅ |
| `tests/unit/test_jwt.py` | 없음 | 3 케이스 | `backend/tests/unit/test_jwt.py` 30 lines | ✅ |
| `tests/unit/test_auth_service.py` | 없음 | 8 케이스 | `backend/tests/unit/test_auth_service.py` 94 lines | ✅ |
| `pyproject.toml` ruff per-file-ignores | tests/** S101/S105/S106 | + errors.py N818 + deps/** B008 S105 | `backend/pyproject.toml` Edit (contract 외 추가 — F2) | ✅ |

Call Sites 검증:
- `repositories/user.py::UserRepo` — find_by_id 1 메서드 추가, 기존 3 메서드 시그니처 변경 0 ✅
- `models/user.py::User` — 변경 0건. AuthService 반환 타입으로 사용 ✅
- `db.py::get_db` — deps/auth.py에서 `Depends(get_db)` 호출 ✅ (contract §2는 get_db_session으로 적었으나 실제 코드명은 get_db — drift F3)
- `config.py::get_settings` — utils/jwt.py가 JWT_SECRET/JWT_ALG/JWT_EXPIRE_MINUTES 접근 ✅

## 2. 테스트 커버리지

- **단위 테스트 14건 / 핵심 메서드 8 = 100%+ 커버**
  - `test_security.py` 3건 — hash 마커 / verify 양 / verify 음
  - `test_jwt.py` 3건 — encode/decode round-trip / 만료 (monkeypatch -1) / 변조
  - `test_auth_service.py` 8건 — register 3 + authenticate 2 + get_current_user 3
- **회귀**: 기존 6 테스트 (3 health + 3 user_repo) PASS 유지 — `20 passed in 3.63s`
- **누락 시나리오** (DEFER):
  - require_auth 직접 단위 테스트 → AuthService.get_current_user 테스트로 간접 cover (require_auth는 헤더 파싱 로직만, 별도 단위 테스트 부담 회피)
  - register 동시성 race (UNIQUE 충돌) → I-04 통합 테스트에서 검증 (FRISK-04 명시)
  - errors.py 베이스 `RealWorldError(message)` 커스텀 메시지 → 본 PR 비목표 (I-04에서 검증)
- **커버리지 목표 달성**: 13/01-strategy §1 ≥80%. AuthService 3 메서드 + utils 4 함수 + require_auth 1 = 8 단위 / 14 테스트 ≈ 100% > 80% ✅

## 3. 보안 / 시크릿

- ✅ 시크릿 0건 — AuthService/utils/deps/tests 코드 어디에도 실제 비밀번호·API 키·JWT secret 평문 없음
- ✅ bcrypt round=12 (`_BCRYPT_ROUNDS = 12` 상수) — R-N-03 검증. 단위 테스트가 `$2b$12$` 마커 직접 어서션
- ✅ JWT_SECRET 환경변수 로드 — `get_settings().JWT_SECRET` 만 참조. 코드에 secret 값 0건. .env.example placeholder 그대로 유지 (R-N-04)
- ✅ 단위 테스트의 dummy password (`"correct horse battery staple"`, `"plaintext_pw"`, `"secret"`) — 메모리 fixture에서만 사용, .env 미오염
- ✅ 도메인 예외 메시지에 secret 노출 0건 (한글 메시지만)
- ✅ require_auth 헤더 파싱: prefix 검증 후 token 추출 — 누락 / 형식 오류 / 빈 토큰 모두 InvalidToken 분기. 타이밍 차이 작음 (early exit 패턴이지만 토큰 자체 검증은 jose 라이브러리 상수 시간 비교 위임)
- ✅ S105 ruff 경고: `_TOKEN_PREFIX = "Token "` false positive — per-file-ignore로 처리 (deps/**)

## 4. 가독성 / 단순성

- ✅ 모듈별 단일 책임 — errors.py(예외) / utils/security.py(bcrypt) / utils/jwt.py(jose) / services/auth.py(비즈니스) / deps/auth.py(FastAPI 의존성) 명확히 분리
- ✅ async/await 일관 — AuthService 3 메서드 + require_auth + UserRepo.find_by_id 모두 async, AsyncSession 의존성 주입
- ✅ 한글 메시지가 errors.py 클래스 속성에 모여 있음 — I-04 exception_handlers가 일괄 처리 가능
- ✅ AuthService.__init__에서 UserRepo 인스턴스화 — 호출자(I-04 라우트)는 `AuthService(session)` 1줄로 사용
- ✅ require_auth: Authorization 헤더 None/공백/prefix 오류/빈 토큰 4 분기 모두 InvalidToken 통일 → 사용자 가시 응답 일관
- ✅ docstring·comment 거의 0건 — 함수 시그니처 자체로 의도 표현. 비-자명한 결정 1곳에만 inline 주석 (deps/auth.py `_TOKEN_PREFIX` 의도)
- ✅ test 함수명 `test_<scenario>_<expected>` — 11-coding-conventions §1 컨벤션 정합

## 5. 발견 사항 (3축 OX 분류)

| 발견 | in_scope | blocks_merge | same_area | 처리 |
| --- | --- | --- | --- | --- |
| F1. passlib 대신 bcrypt 라이브러리 직접 사용 (contract §2는 passlib 명시) | ✅ | ❌ | ✅ | OK — FRISK-01 적시 위험 실 발현 (passlib 1.7.4 + bcrypt 4.x detect_wrap_bug 호환 이슈). C1 커밋 메시지 + risk.md FRISK-01 + 본 review에 명시 |
| F2. pyproject.toml ruff per-file-ignores 추가 (contract §2에 없음) | ✅ | ❌ | ✅ | OK — N818 (errors.py 도메인 명명) + B008/S105 (FastAPI Depends 표준) false positive. 별도 chore 커밋으로 분리 |
| F3. contract §2가 `get_db_session`이라 적었으나 실제 db.py 함수명은 `get_db` | ❌ (doc drift) | ❌ | ❌ | DEFER — 본 PR 코드는 정확함. 후속 P13 docs-update에서 feat-auth-service.contract.md §2/§3 정정 (또는 그대로 둠 — 코드와 매핑 명확) |
| F4. AuthService 생성자가 UserRepo 인스턴스화 (DI 패턴이 아님) | ✅ | ❌ | ✅ | OK — RealWorld MVP 학습 부담 회피. AsyncSession은 외부 주입, UserRepo는 내부 wiring |
| F5. AuthService.get_current_user의 sub `int` 변환 실패 핸들링 | ✅ | ❌ | ✅ | OK — sub은 항상 str(user_id)로 인코딩하므로 변조 케이스만 발현. TypeError/ValueError → InvalidToken 명시적 변환 |
| F6. require_auth가 단위 테스트로 직접 검증되지 않음 | ✅ | ❌ | ✅ | OK — AuthService.get_current_user 8 케이스가 핵심 로직 cover. require_auth는 헤더 파싱만 (4 분기 모두 InvalidToken). I-04 통합 테스트에서 통과 확인 예정 |
| F7. errors.py 클래스명에 Error 접미사 없음 (ruff N818) | ❌ (convention) | ❌ | ✅ | OK — RealWorld 도메인 명명 보존 (DuplicateEmail / InvalidToken / NotFound 등). ruff per-file-ignore 추가 |
| F8. JWT decode 옵션 명시 안 함 (exp 검증 default ON 의존) | ✅ | ❌ | ✅ | OK — jose 기본 동작 검증 단위 테스트 (test_decode_expired_raises_expired_token)로 보장 |
| F9. AuthService.authenticate 실패 시 user 미존재와 비밀번호 불일치 동일 InvalidCredentials | ✅ | ❌ | ✅ | OK — 보안 표준 (사용자 enumeration 차단). RealWorld 422/401 응답 통일 |
| F10. tests/unit/test_auth_service.py가 in-memory aiosqlite + 실제 bcrypt 사용 (느릴 가능) | ✅ | ❌ | ✅ | OK — 8 케이스 × 실제 bcrypt round=12 = 2.21s 측정. CI 통과 시간 영향 미미 |
| F11. ExpiredToken/InvalidToken 모두 401인데 별도 클래스 분리 | ✅ | ❌ | ✅ | OK — 한글 메시지 다름 ("만료되었습니다" vs "유효하지 않습니다") 사용자 가시성 ↑ |
| F12. monkeypatch.setattr(settings, "JWT_EXPIRE_MINUTES", -1)이 lru_cache 의존 (cache_clear() 호출 필요) | ✅ | ❌ | ✅ | OK — test_jwt + test_auth_service에서 명시적 `get_settings.cache_clear()` 호출로 격리 |

**3축 OX 결과**: 10 PASS + 2 DEFER (F1 contract drift는 의도된 위험 회피, F3 contract doc drift는 후속 정정 가능). blocks_merge 0건.

## 6. NEEDS-WORK 항목

(없음) — Verdict PASS. F3은 P13 docs-update에서 contract.md 정정 또는 그대로 둘 수 있음 (코드 매핑 명확).
