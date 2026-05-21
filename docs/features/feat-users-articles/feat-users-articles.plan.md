---
doc_type: feature-plan
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

# feat-users-articles — Implementation Plan

> Issue #4 / Sprint 1 / I-04. 10 커밋 DAG (feat 5 + test 3 + chore 1 + docs 1). ADR-0018 selective read — contract §0 5행만 진입. critical path = C1→C2→C3→C4→C5→C6→C7→C8→C9.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 10 커밋 DAG (Article 모델·repo·service / slug util / Pydantic 스키마 / 라우터 / 예외 핸들러 / 통합 테스트 + 단위 테스트) |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `feat(backend): I-04 Article + Tag 모델 + Alembic 0003` | `models/article.py` (Article, Tag, article_tags M2M) + `migrations/versions/0003_articles_tags.py` (autogenerate) + `models/__init__.py` re-export | (다음 커밋 단위 테스트) | Low — schema 추가만 |
| C2 | `feat(backend): I-04 utils/slug + ArticleRepo selectinload` | `utils/slug.py` (slugify + unique_slug) + `repositories/article.py` (5 메서드, selectinload) | (다음 커밋 단위 테스트) | Low — repo 신규 |
| C3 | `test(backend): I-04 utils/slug 5 케이스` | `tests/unit/test_slug.py` (slugify 3 + unique_slug 2) | 단위 5 PASS | None |
| C4 | `feat(backend): I-04 ArticleService 5 메서드 + 작성자 검증` | `services/article.py` (list/get_by_slug/create/update/delete + Forbidden) | (다음 커밋 단위 테스트) | Low — service 신규 |
| C5 | `test(backend): I-04 ArticleService 8 케이스` | `tests/unit/test_article_service.py` (list / get / create + slug 충돌 / update 본인·타인 / delete 본인·타인 / NotFound) | 단위 8 PASS | None |
| C6 | `feat(backend): I-04 Pydantic 스키마 + users/articles 라우터` | `schemas/user.py` + `schemas/article.py` + `schemas/__init__.py` + `routers/users.py` (3) + `routers/articles.py` (5) + `routers/__init__.py` | (다음 커밋 통합 테스트) | Medium — 8 라우트 신규 |
| C7 | `feat(backend): I-04 main.py 라우터 등록 + RealWorldError 예외 핸들러` | `main.py` (include_router 2 + exception_handler 1) | (smoke test) | Low — main.py 1 함수·2 줄 |
| C8 | `chore(backend): I-04 ruff per-file-ignores routers/** B008` | `pyproject.toml` (`[tool.ruff.lint.per-file-ignores]` 추가) | ruff PASS | None — lint 설정만 |
| C9 | `test(backend): I-04 users/articles 통합 테스트 14건+` | `tests/integration/__init__.py` + `tests/integration/conftest.py` (AsyncClient fixture) + `tests/integration/test_users_routes.py` (7+) + `tests/integration/test_articles_routes.py` (12+) | 통합 19+ PASS, 전체 42+ PASS | None — 테스트 추가 |
| C10 | `docs(feat): I-04 feat-users-articles 8종 산출` | `docs/features/feat-users-articles/*.md` 8 파일 (brief/contract/plan/eng-review/acceptance/risk/code-review/ai-qa-report) | (문서) | None |

각 커밋 메시지는 ADR-0021 정규식 `^(feat|fix|chore|docs|test|refactor)\([a-z][a-z0-9,_-]*\): .+`. 본 PR 머지 시 커밋 body에 `Closes #4` + R-ID/F-ID 매핑 + 부팅 자산 메모 (ADR-0046 §2.4).

## 2. 의존성 그래프

```
C1 (Article + Tag + Alembic 0003)
   ↓
C2 (utils/slug + ArticleRepo) ← C1 의존 (Article 모델 import)
   ↓
C3 (test_slug)             ← C2 의존 (slug import)
   ↓
C4 (ArticleService)        ← C2·C1 의존 (Repo + Model + errors.NotFound/Forbidden import)
   ↓
C5 (test_article_service)  ← C4 의존 (ArticleService + AsyncSession fixture)
   ↓
C6 (Schemas + Routers)     ← C4 의존 (ArticleService) + I-03 deps/auth.require_auth + AuthService 의존
   ↓
C7 (main.py 등록 + 예외 핸들러) ← C6 의존
   ↓
C8 (ruff per-file-ignores) ← C6·C7 후속 (false positive 발견 직후만 분리 커밋)
   ↓
C9 (통합 테스트)            ← C7·C8 의존 (main.app 부팅 + httpx)
   ↓
C10 (docs)                 ← C1~C9 완료 후 산출 일괄 작성
```

DAG 순환 0건. critical path = C1 → C2 → C4 → C6 → C7 → C9 (테스트 통과 시점). C3·C5·C8·C10은 분기.

## 3. 테스트 매핑

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C3 | `tests/unit/test_slug.py` | slugify 영문 / slugify 공백·특수문자·한글 → kebab / slugify 빈 입력 → fallback / unique_slug 충돌 없음 → base / unique_slug 충돌 2회 → `-2` `-3` |
| C5 | `tests/unit/test_article_service.py` | list_returns_articles_with_author / get_by_slug_returns_article / get_by_slug_missing_raises_not_found / create_assigns_unique_slug_on_conflict / update_by_author_succeeds / update_by_other_raises_forbidden / delete_by_author_succeeds / delete_by_other_raises_forbidden |
| C9 | `tests/integration/test_users_routes.py` | register_returns_user_with_token / register_duplicate_email_returns_422 / register_short_password_returns_422 / login_returns_user_with_token / login_invalid_credentials_returns_422 / current_user_with_jwt_returns_user / current_user_without_jwt_returns_401 |
| C9 | `tests/integration/test_articles_routes.py` | list_returns_articles_and_count / list_with_author_filter_returns_only_authors_articles / list_with_unknown_author_returns_empty / detail_returns_article / detail_missing_returns_404 / create_returns_201_with_article / create_without_auth_returns_401 / create_duplicate_title_assigns_suffix_slug / update_by_author_succeeds / update_by_other_returns_403 / delete_by_author_returns_204 / delete_by_other_returns_403 |

**커버리지 매핑**: ArticleService 5 메서드 + utils/slug 2 함수 + routers/users 3 함수 + routers/articles 5 함수 + 예외 핸들러 = 16 진입점 / 단위 13 + 통합 19+ = 32 테스트 ≈ 100% > 80% (13/01-strategy §1).

## 4. 빌드·실행 검증 단계

```
cd backend && uv sync --frozen
# 60 packages → 60+ (변경 0 — alembic·httpx·sqlalchemy·pydantic·passlib·python-jose·bcrypt 모두 I-01에 도입됨)

uv run alembic upgrade head
# alembic 0002 → 0003 진행. articles + tags + article_tags 3 테이블 생성

uv run ruff check . && uv run ruff format --check .
# ruff lint PASS (per-file-ignores: errors.py N818 + deps/** B008 S105 + routers/** B008 + tests/** S101/S105/S106)
# ruff format PASS

uv run pytest -v
# 단위 13 신규 (test_slug 5 + test_article_service 8) + 통합 19+ 신규 (test_users_routes 7+ + test_articles_routes 12+)
# 합산 ≥ 42 (기존 20 + 신규 ≥ 22) PASS

uv run python -c "from realworld.main import app; print(len(app.routes))"
# 10+ 라우트 출력 (1 health + 3 users + 5 articles + 1 openapi.json + 1 docs)
```

위 5 step 모두 exit 0 + 통합 테스트 timeout 5s 이내. CI workflow `backend-ci`는 동일 명령을 실행 (ADR-0047 양축 검증).

## 5. 점진 합의 / 결정 발생 항목

- **D-01**: alembic autogenerate vs 수기 migration → autogenerate 채택. Article·Tag·article_tags 3 테이블 정형이라 자동 결과 신뢰. 후속 수정 시 점검
- **D-02**: tag M2M 연결 테이블 — secondary table 패턴 (Tag·Article 양측 relationship). Tag.articles back_populates 미정의 (조회 방향 단방향). 본 MVP는 article→tags 조회만 필요
- **D-03**: slug 정규화 — 한글·일본어 등 비-ASCII는 `unicodedata.normalize('NFKD')` 후 ASCII drop. 결과가 빈 문자열이면 fallback `"article"` + UNIQUE suffix. 본 MVP는 영문 위주라 발현 드뭄
- **D-04**: 빈 tagList 처리 — `[]` 명시 또는 omitted 둘 다 허용. Pydantic Field default=[]. tag 미존재 시 INSERT, 존재 시 select-or-create 패턴
- **D-05**: GET /api/articles의 optional 인증 — 본 MVP는 favorited 필드 Out of Scope이므로 인증 헤더 무시. require_auth 미적용. 09-api-spec §3 GET /api/articles 명시
- **D-06**: 통합 테스트 fixture — in-memory aiosqlite + ASGITransport(app)로 외부 서버 부팅 없이 검증. JWT 발급은 헬퍼 함수 (utils/jwt.encode_token 직접 호출)
- **D-07**: PUT 부분 갱신 — Pydantic ArticleUpdate 모든 필드 optional. None인 필드는 변경하지 않음 (`model_dump(exclude_unset=True)` 패턴)
- **D-08**: slug UNIQUE 충돌 시 `-2` `-3` 진행 — repo에 별도 카운터 함수 (`count_by_slug_base`). 동시성 race는 04-srs §R-F-06 Failure-3에 Out 명시 (재시도 1회 후 422 fallback)
