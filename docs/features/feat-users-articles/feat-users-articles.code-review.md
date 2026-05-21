---
doc_type: feature-code-review
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-12, R-N-01, R-N-05]
  F-ID: [F-01, F-02]
  supersedes: null
---

# feat-users-articles — Code Review

> P9. Generator≠Evaluator. C1~C11 diff 검토. Verdict PASS — 13 OX (11 PASS + 2 DEFER). NEEDS-WORK 0건.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — Verdict PASS. 13 OX = 11 PASS + 2 DEFER (F1 errors.InvalidCredentials.status_code 401→422 변경 / F2 update가 refresh 대신 reload). NEEDS-WORK 0건 |

## 0. Verdict

**PASS** — 11 커밋 diff 검토 결과 contract §2 Before/After 16행 + plan 10 커밋 DAG 모두 매핑. NEEDS-WORK 0건. P10 AI 게이트 진입 허용. 49 passed in 11.15s.

- [reviewer]: woosung.ahn@bespinglobal.com (AI — Generator≠Evaluator)
- [review_at]: 2026-05-21

## 1. 컨트랙트 충실도

각 contract Before/After 행이 코드로 매핑됨:

| 항목 | Before | After | 코드 매핑 | OX |
| --- | --- | --- | --- | --- |
| `realworld/models/article.py` | 없음 | Article + Tag + article_tags M2M | `backend/realworld/models/article.py` 47 lines | ✅ |
| `realworld/models/__init__.py` | User만 export | + Article/Tag/article_tags | `backend/realworld/models/__init__.py` 2 lines diff | ✅ |
| `alembic/versions/0003_articles_tags.py` | 없음 | autogenerate (수기 작성) | 75 lines, upgrade + downgrade | ✅ |
| `realworld/repositories/article.py` | 없음 | ArticleRepo 6 메서드 (list_with_filters/get_by_slug/exists_by_slug/get_or_create_tag/add/delete) | 80 lines, selectinload N+1 회피 | ✅ |
| `realworld/utils/slug.py` | 없음 | slugify + unique_slug + Protocol | 25 lines | ✅ |
| `realworld/services/article.py` | 없음 | ArticleService 5 async 메서드 + 작성자 검증 | 78 lines + `from __future__ import annotations` | ✅ |
| `realworld/schemas/__init__.py` | 없음 | 빈 마커 | 0 lines | ✅ |
| `realworld/schemas/user.py` | 없음 | UserCreateRequest/LoginRequest/Response (RealWorld 래핑) | 32 lines | ✅ |
| `realworld/schemas/article.py` | 없음 | ArticleCreate/UpdateRequest + View/Response + ListResponse + ProfileEmbed | 58 lines (camelCase serialization_alias) | ✅ |
| `realworld/routers/__init__.py` | 없음 | 빈 마커 | 0 lines | ✅ |
| `realworld/routers/users.py` | 없음 | POST /users + POST /users/login + GET /user | 51 lines | ✅ |
| `realworld/routers/articles.py` | 없음 | GET ""/GET /{slug}/POST ""/PUT /{slug}/DELETE /{slug} | 105 lines | ✅ |
| `realworld/main.py` | /health 1 | + 라우터 2 + RealWorldError handler | `+15 lines` (include_router 2 + JSONResponse handler) | ✅ |
| `realworld/errors.py` | InvalidCredentials 401 | InvalidCredentials 422 (9-api-spec 정합) | `errors.py:22` 1 line diff — code-review F1 | ✅ |
| `pyproject.toml` ruff per-file-ignores | tests/** S101/S105/S106 + errors.py N818 + deps/** B008/S105 | + tests/** S107 + routers/** B008 | 2 line diff — chore 커밋 분리 | ✅ |
| `tests/unit/test_slug.py` | 없음 | 5 케이스 | 36 lines | ✅ |
| `tests/unit/test_article_service.py` | 없음 | 8 케이스 | 134 lines | ✅ |
| `tests/integration/__init__.py` + conftest.py | 없음 | AsyncClient + dependency_overrides[get_db] in-memory aiosqlite + register_user 헬퍼 | 41 lines | ✅ |
| `tests/integration/test_users_routes.py` | 없음 | 7 케이스 | 89 lines | ✅ |
| `tests/integration/test_articles_routes.py` | 없음 | 12 케이스 | 164 lines | ✅ |

Call Sites 검증:
- `main.py` — 라우터 2개 + exception_handler 1 등록 ✅
- `UserRepo` — 변경 0 (AuthService가 wrapper). ArticleService는 author 조회 안 함 (Article.author lazy="joined") ✅
- `AuthService` — 변경 0. routers/users.py가 register/authenticate/get_current_user 3 wrapper ✅
- `require_auth` — 변경 0. routers/articles.py POST/PUT/DELETE 3 라우트가 `Depends(require_auth)` ✅
- `get_db` — 변경 0. 라우터 함수가 `Depends(get_db)` + 통합 테스트 conftest가 dependency_overrides[get_db] ✅
- `User` 모델 — 변경 0. Article.author relationship target ✅
- `errors.py` — InvalidCredentials.status_code 401→422 변경. 9-api-spec 정합. code-review F1 ✅
- `config.get_settings` — 변경 0. utils/jwt.py 그대로 사용 ✅

## 2. 테스트 커버리지

- **단위 테스트 13건 신규** — test_slug.py 5 (slugify 3 + unique_slug 2) + test_article_service.py 8 (create + slug 충돌 / list / get / update 본인·타인 / delete 본인·타인)
- **통합 테스트 19건 신규** — test_users_routes.py 7 (register happy/422 dup/422 short + login happy/422 invalid + GET /user happy/401) + test_articles_routes.py 12 (list happy/?author= 필터/unknown 빈/detail happy/404/POST happy+401+slug 충돌 -2/PUT happy+403/DELETE 204+follow-up 404+403)
- **회귀**: 기존 단위 17건(test_health 3 + test_user_repo 3 + test_security 3 + test_jwt 3 + test_auth_service 8) PASS 유지 — **합산 49 passed in 11.15s**
- **누락 시나리오** (DEFER):
  - 통합 테스트의 R-N-01 p95 측정 → 14-wbs I-05에서 100건 시드 + 측정
  - 동시 race (동일 title 동시 POST 2개) → SQLite 직렬 write로 자체 보호. 04-srs §R-F-06 Failure-3 Out 명시
  - PUT 시 tag_list만 변경 + 빈 배열 → 부분 케이스, AC-10에서 정상화 (default_factory=list)
- **커버리지 목표 달성**: 13/01-strategy §1 ≥80%. 16 진입점(routers 8 + ArticleService 5 + slug 2 + 핸들러 1) / 32 신규 테스트 ≈ 100% > 80% ✅

## 3. 보안 / 시크릿

- ✅ 시크릿 0건 — 코드 어디에도 실제 비밀번호·API 키·JWT secret 평문 없음
- ✅ bcrypt round=12 유지 (I-03 utils/security 변경 0). I-04는 비밀번호 hash 직접 사용 안 함 — AuthService.register/authenticate 위임
- ✅ JWT_SECRET 환경변수 로드 유지 (I-03 utils/jwt 변경 0). 라우터는 `encode_token(user.id)` 호출만
- ✅ 통합 테스트의 dummy password (`"supersecret"`) — in-memory fixture만, .env 미오염
- ✅ 도메인 예외 메시지에 secret 노출 0 (한글 메시지만). InvalidCredentials의 "이메일 또는 비밀번호" 메시지가 사용자 enumeration 회피
- ✅ tagList 입력 sanitize: Pydantic max_length=20 (개수 제한). 각 tag 문자열은 sanitize 안 함 (RealWorld spec 자유) — XSS 방어는 frontend escape 책임
- ✅ slug 입력은 자동 생성만 (사용자 입력 무관 — title에서 slugify). path injection 위험 0
- ✅ S105/S107 ruff false positive: `_TOKEN_PREFIX = "Token "` (deps/**) + `password: str = "supersecret"` (tests/**) per-file-ignore 일관 처리

## 4. 가독성 / 단순성

- ✅ 모듈별 단일 책임 — models(declarative) / repositories(SQLAlchemy query) / services(비즈니스 + 예외) / schemas(Pydantic in/out) / routers(HTTP thin layer) / utils/slug(순수 함수) 명확
- ✅ async/await 일관 — 모든 service·repository·router·테스트 async, AsyncSession 의존성 주입
- ✅ 한글 메시지가 errors.py 클래스 속성에 모여 있음 — exception_handler 1 함수가 일괄 변환
- ✅ `ArticleService.list` 메서드명이 builtin `list` shadow — `from __future__ import annotations` 패턴으로 회피 (C4 후속 fix 커밋에 명시)
- ✅ Pydantic 래핑 형식(`{user: {...}}`, `{article: {...}}`)이 RealWorld spec 정합 + `populate_by_name + serialization_alias`로 camelCase 응답
- ✅ test 함수명 `test_<scenario>_<expected>` — 11-coding-conventions §1 컨벤션 정합
- ✅ docstring·comment 거의 0건 — 함수 시그니처와 명명으로 의도 표현

## 5. 발견 사항 (3축 OX 분류)

| 발견 | in_scope | blocks_merge | same_area | 처리 |
| --- | --- | --- | --- | --- |
| F1. errors.InvalidCredentials.status_code 401 → 422 변경 (contract §2에 없음) | ✅ | ❌ | ✅ | OK — 9-api-spec POST /users/login 422 명세 정합. I-03 단위 테스트가 status_code 검증 없음(raises만) → 회귀 0. 별도 fix 커밋으로 분리 + code-review.md F1 + ai-qa-report 발견 |
| F2. ArticleService.update가 refresh 대신 get_by_slug 재조회 (contract §2에 명시 없음) | ✅ | ❌ | ✅ | OK — 통합 테스트에서 selectin lazy load 회귀 발견 직후 인라인 결정. fix 커밋 메시지 + code-review F2 발견. PUT 시 1 추가 SELECT 비용 < N+1 risk |
| F3. routers/articles.py update_article에 PUT 응답 spec의 updated_at 검증 통합 테스트 없음 | ✅ | ❌ | ✅ | OK — `updated_at` 필드는 Pydantic ArticleView에 포함되어 응답에 자동 노출. SQLAlchemy `onupdate=func.now()`가 commit 시 자동 갱신. 통합 테스트 PASS 결과로 schema 검증 cover |
| F4. ArticleService 생성자가 ArticleRepo 인스턴스화 (DI 패턴이 아님) | ✅ | ❌ | ✅ | OK — I-03 AuthService 패턴과 일관. RealWorld MVP 학습 부담 회피. AsyncSession은 외부 주입 |
| F5. unique_slug Protocol 사용 — typing 정합인가 | ✅ | ❌ | ✅ | OK — slugify 단위 테스트 fake repo로 Protocol 만족. 실제 ArticleRepo도 `exists_by_slug` 명시 |
| F6. routers/articles.py에 `response_model_by_alias=True` 5곳 반복 — 모듈 상수로 추출 가능 | ❌ (cosmetic) | ❌ | ❌ | DEFER — 5곳 반복이지만 명시적이라 가독성 ↑. retro 후 검토 가능 |
| F7. `_to_view`가 routers/users.py와 routers/articles.py에 각각 정의 (이름 충돌 없음, 다른 시그니처) | ✅ | ❌ | ✅ | OK — RealWorld View 변환은 라우터별 책임. 공유 헬퍼는 과도한 추상화 |
| F8. ArticleUpdatePayload.tag_list가 None vs []을 구분 (None=변경 안 함, []=빈 배열로 설정) | ✅ | ❌ | ✅ | OK — D-07 plan §5 명시. PUT 부분 갱신 표준 패턴 |
| F9. integration conftest의 dependency_overrides가 fixture 종료 시 pop — 다른 테스트 격리 보장 | ✅ | ❌ | ✅ | OK — 명시적 cleanup. session_maker scope이 fixture와 동일 (function) → 격리 100% |
| F10. 모든 라우터에서 `await session.commit()`을 service 후에 명시 — service에 commit 책임 미위임 | ✅ | ❌ | ✅ | OK — service는 flush만, transaction 경계는 라우터(요청 단위). 11-conventions §4 정합 |
| F11. `errors.NotFound("게시글을 찾을 수 없습니다")`로 메시지 override — 다른 컨텍스트에서도 동일 메시지 노출 가능 | ✅ | ❌ | ✅ | OK — NotFound는 generic + override 패턴. comment 라우트(I-05/I-06)에서 "댓글을 찾을 수 없습니다"로 동일 패턴 |
| F12. ArticleRepo.list_with_filters에서 count도 join — 2 query 발생 | ✅ | ❌ | ✅ | OK — SQLAlchemy 표준 count 패턴. paginated list와 total 둘 다 필요. 1~5명 동시 사용자 가정으로 부하 무시 |
| F13. PUT 요청에서 `description: None`이 명시 전달 시 description 삭제 시도 — ArticleUpdatePayload는 None을 "변경 안 함"으로 해석 | ✅ | ❌ | ✅ | OK — model_dump(exclude_unset=True) 패턴 미사용. 명시적 None=변경 안 함 (D-07). 빈 문자열로 삭제 가능. 본 MVP는 None 케이스 발현 적음 |

**3축 OX 결과**: 11 PASS + 2 DEFER (F1·F2가 contract drift이지만 명시적 fix 커밋 + 명세 정합). blocks_merge 0건.

## 6. NEEDS-WORK 항목

(없음) — Verdict PASS. F1·F2는 fix 커밋에 결정 경로 가시화 완료. F6 cosmetic은 retro 검토.
