---
doc_type: feature-risk
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

# feat-tag-feed — Feature Risk

> P7. 3 F-RISK 모두 Low.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-31 | woosung.ahn@bespinglobal.com | 초안 — 3 F-RISK 모두 Low |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| F-RISK-01 | JOIN article_tags + tags 시 중복 row — DISTINCT 누락 시 같은 글 N번 반환 | 2 | 2 | Low |
| F-RISK-02 | 빈 tags=[] DB — HomePage 칩 영역 처리 | 1 | 1 | Low |
| F-RISK-03 | `?tag=` 미존재 태그 — 빈 결과인지 에러인지 | 1 | 2 | Low |

## 2. 리스크 상세

### F-RISK-01 — JOIN 중복

- **시나리오**: `list_with_filters` tag 필터 시 article ↔ article_tags ↔ tags JOIN. article 1건이 article_tags 1행만 가지므로 중복 가능성 낮지만 SQLAlchemy 결과셋에서 selectinload(Article.tags) 와 함께 사용 시 unique() 누락 가능
- **완화**: 기존 패턴(`scalars().unique().all()`) 그대로 사용. 통합 테스트로 articlesCount 정합 검증

### F-RISK-02 — 빈 tags

- **시나리오**: DB에 Tag 0건일 때 GET /api/tags → 200 + `{"tags": []}`. HomePage 칩 영역 미노출
- **완화**: HomePage 조건부 렌더 `{tags.length > 0 && ...}`. seed 100건 환경에서는 5종 보장

### F-RISK-03 — 미존재 태그 필터

- **시나리오**: `?tag=nonexistent` → JOIN 결과 0건 → 200 + `{"articles": [], "articlesCount": 0}`. 404가 아닌 empty (RealWorld spec 정합)
- **완화**: 통합 테스트로 빈 결과 케이스 검증 (별도 또는 기존 unknown_author 패턴 동일)

## 3. High 등급 단계적 롤아웃

(없음)

## 4. 데이터 영속성 변경

- DB 스키마 무수정 — alembic 0004 (head) 그대로
- 신규 인덱스 0 — 기존 article_tags pk + ix_tags_name 활용

## 5. 15-risk.md 갱신 항목

(없음) — follow-up 신규 기능, 기존 risk 영향 0
