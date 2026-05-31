---
doc_type: feature-plan
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-31
gate: feature
related:
  R-ID: [R-F-14]
  F-ID: [F-02]
  supersedes: null
---

# feat-tag-feed — Implementation Plan

> P4. 4 commit DAG: C1 backend tags 라우트 → C2 backend tag 필터 → C3 frontend → C4 docs.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-31 | woosung.ahn@bespinglobal.com | 초안 — 4 commit DAG + ADR-0021 통과 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `feat(backend): GET /api/tags 라우트 + TagsListResponse (#25)` | `routers/tags.py` 신규 + `schemas/tag.py` 신규 + `repositories/article.py` list_all_tag_names + `main.py` 라우터 등록 + `tests/integration/test_tags_routes.py` 신규 1건 | 통합 1 | 0 — 신규 라우트 |
| C2 | `feat(backend): articles list tag 필터 (R-F-14) (#25)` | `repositories/article.py` list_with_filters에 tag 인자 + `services/article.py::list` + `routers/articles.py::list_articles` + 단위 1 + 통합 1 | 단위 1 + 통합 1 | 0 — default None, BC neutral |
| C3 | `feat(frontend): HomePage 태그 칩 필터 UI (#25)` | `types/api.ts` TagsListResponse + `pages/HomePage.tsx` 태그 칩 영역 + selectedTag state + ?tag= 쿼리 | (없음) | 0 — 기존 페이지네이션 무변경 |
| C4 | `docs(plan): feat-tag-feed 8 산출 + INDEX v0.16 (#25)` | feature docs 8 + INDEX | (없음) | 0 |

ADR-0021 통과: feat(backend) 2 + feat(frontend) 1 + docs(plan) 1.

## 2. 의존성 그래프

```
C1 (backend tags 라우트) ─→ C3 (frontend types + HomePage)
                             ▲
                             │
C2 (backend tag 필터) ───────┘
                             │
                             ▼
                          C4 (docs sync)
```

- **C1·C2 독립**: 라우트와 필터는 다른 파일. 어느 순서로도 OK. C1 먼저 — 신규 라우트가 더 가시적
- **C1+C2 → C3**: frontend가 두 backend 변경 모두 의존
- **C3 → C4**: 모든 코드 PASS 후 docs

순환 0.

## 3. 테스트 매핑

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C1 통합 | `tests/integration/test_tags_routes.py::test_list_returns_tags` | seed 또는 article 작성 후 `GET /api/tags` → 200 + `{"tags": [...]}` 정렬 |
| C2 단위 | `tests/unit/test_article_service.py::test_list_with_tag_filter` | service.create 글 2건 (다른 태그) → service.list(tag="python") → 1건만 |
| C2 통합 | `tests/integration/test_articles_routes.py::test_list_with_tag_filter` | jane:python 글 + bob:react 글 작성 후 `GET /api/articles?tag=python` → articlesCount=1 |
| C3 | (없음 — 수동) | HomePage 진입 → 태그 칩 표시 → 칩 클릭 → 필터 적용 + 카드 1건만 → 해제 버튼 클릭 → 전체 복귀 |
| C4 | (validate-doc.sh) | 8 산출 schema PASS |

## 4. 빌드·실행 검증 단계

```bash
# 1) backend 회귀 + 신규 테스트
cd backend && uv run pytest -v
# expect: 약 80 passed (77 + 3 신규)

# 2) frontend 빌드
cd frontend && npm run build
# expect: 62+ modules + 에러 0

# 3) 동시 부팅 + 수동 시도
cd backend && uv run uvicorn realworld.main:app --port 8000
cd frontend && npm run dev
# 브라우저 / 진입 → 태그 칩 노출 → 'python' 클릭 → 필터 적용
# curl http://localhost:8000/api/tags
# expect: {"tags": ["fastapi", "python", "react", "realworld", "sqlalchemy"]} (seed 100건 시 5종)
```

## 5. 점진 합의 / 결정 발생 항목

- **(1) schemas/tag.py 별도 vs schemas/article.py 추가**: 별도 파일 — Tag는 도메인 한정이 더 명확. Article과 Tag는 별 책임
- **(2) tag 칩 UI 위치**: HomePage 상단 (h1 아래) — sidebar 패턴은 over-engineering (5종이라 칩 1줄로 충분)
- **(3) selectedTag state**: HomePage 로컬 state (URL 동기는 out of scope — 새로고침 시 필터 손실)
- **(4) `list_all_tag_names()` 정렬**: `ORDER BY name ASC` — UI에서 알파벳 정렬이 자연스러움
- **(5) `?tag=<name>` URL encoding**: encodeURIComponent (한글 태그 대비, 본 사이클은 영문 5종이지만 일관 패턴)
