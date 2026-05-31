---
doc_type: feature-code-review
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

# feat-tag-feed — Code Review

> P9. 3 코드 커밋(C1·C2·C3). PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-31 | woosung.ahn@bespinglobal.com | 초안 — PASS |

## 0. Verdict

**PASS** — 3 코드 커밋. pytest 81 passed + Vite build 61 modules. NEEDS-WORK 0.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (AI self-review)
- [review_at]: 2026-05-31

## 1. 컨트랙트 충실도

| Before/After | Before | After |
|---|---|---|
| schemas/tag.py | 없음 | C1 — TagsListResponse |
| routers/tags.py | 없음 | C1 — GET /api/tags |
| repositories/article.py | author 필터만 | C1 list_all_tag_names + C2 tag JOIN |
| services/article.py::list | author only | C2 — tag 인자 추가 |
| routers/articles.py::list_articles | author only | C2 — tag 쿼리 |
| main.py | 3 라우터 | C1 — tags_router 추가 |
| test_tags_routes.py | 없음 | C1 — 2건 |
| test_articles_routes.py::test_list_with_tag_filter | 없음 | C2 — 1건(3 분기) |
| test_article_service.py::test_list_with_tag_filter | 없음 | C2 — 1건 |
| types/api.ts | TagsListResponse 없음 | C3 — 추가 |
| HomePage.tsx | 페이지네이션만 | C3 — 태그 칩 + selectedTag state |

contract §3 Call Sites 4행 BC neutral 정합.

## 2. 테스트 커버리지

- backend pytest **81 passed in 13.16s** (77 + 단위 1 + 통합 3)
- TS strict + Vite build 61 modules in 1.31s
- 단위: ArticleService tag 필터 / 통합: GET /api/tags (2분기) + ?tag= (3분기)
- frontend 수동: Manual verification (HomePage 칩 클릭 + 필터 + 해제)

## 3. 보안 / 시크릿

- tag name은 backend Tag 모델 + ORM 차단. 라우트는 auth optional (RealWorld spec)
- frontend: encodeURIComponent로 한글·특수문자 안전 처리
- 신규 환경변수 0

## 4. 가독성 / 단순성

- routers/tags.py 13줄 — 단일 라우트
- list_with_filters tag 분기 — 기존 author 분기와 동형 패턴
- HomePage 태그 영역 — 조건부 렌더 + 단순 ternary

## 5. 발견 사항 (3축 OX 분류)

| 발견 | in_scope | blocks_merge | same_area | 처리 |
|---|---|---|---|---|
| F1: list_with_filters tag JOIN 중복 — DISTINCT 필요? | ⭕ | ❌ | ⭕ | 통합 테스트로 articlesCount 정합 검증. article-tags M2M 1:1 매칭이라 중복 0 |
| F2: tags 로드 실패 silent — 사용자에게 알리지 않음 | ⭕ | ❌ | ⭕ | 의도. 핵심 UX 영향 0 (칩 영역만 미노출) |
| F3: selectedTag URL 동기 안 함 (새로고침 시 리셋) | ⭕ | ❌ | ⭕ | 의도 plan §5 (3) |
| F4: tagParam 직접 string 합 — URLSearchParams 미사용 | ⭕ | ❌ | ⭕ | INFO. 학습 컨텍스트 acceptable. limit/offset 패턴 일관 |

NEEDS-WORK 0.

## 6. NEEDS-WORK 항목

(없음)
