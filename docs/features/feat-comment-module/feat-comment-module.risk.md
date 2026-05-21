---
doc_type: feature-risk
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-08, R-F-09, R-F-10, R-F-11, R-F-13]
  F-ID: [F-03]
  supersedes: null
---

# feat-comment-module — Feature Risk

> P7. 본 PR 한정 F-RISK 4건. 모두 Low. mode=add minimal blast radius.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — F-RISK 4건 모두 Low. High 0건 |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| F-RISK-01 | CASCADE 미동작 — Article 삭제 시 comments 고아 row 발생 | 2 | 1 | Low |
| F-RISK-02 | R-F-13 PUT comment 비표준 URL — RealWorld 외부 클라이언트 호환 안 됨 | 1 | 3 | Low |
| F-RISK-03 | Comment.author lazy="joined" — 댓글 다수 시 JOIN 비용 누적 | 2 | 1 | Low |
| F-RISK-04 | Alembic 0004 head 미적용 시 GET /comments 500 (테이블 부재) | 2 | 1 | Low |

## 2. 리스크 상세

### F-RISK-01 — CASCADE 미동작

- **시나리오**: `comments.article_id FK ondelete=CASCADE` 명시 누락 시 Article 삭제가 IntegrityError로 실패하거나 (FK 무시) comments 고아 row 발생
- **완화**: contract §2 (D-06-1 명시) + AC-06 통합 테스트(`test_delete_cascades_comments`)로 schema-level 검증. SQLite는 PRAGMA `foreign_keys=ON` 필요 — DB 부팅 시 자동 설정 확인 (기존 article_tags M2M CASCADE 동작 = 검증된 패턴)
- **트리거 시점**: P8 implement 중 — D-06-1 + D-06-8 미통과 시 즉시 발견

### F-RISK-02 — R-F-13 PUT 비표준 URL

- **시나리오**: PUT `/api/articles/{slug}/comments/{id}` — RealWorld spec에 없는 URL. Conduit FE 클라이언트(외부 호환)는 호출 안 함
- **완화**: 본 프로젝트 frontend는 자체 구현(I-09)이라 외부 호환 N/A. 04-srs §6.6 + 09-api-spec §3 287 사용자 결정 명시. 후속 RealWorld 호환성 필요 시 ADR로 deprecation 경로 결정
- **트리거 시점**: P10 ai-qa-report — workflow 검증 시 spec 정합성 명시

### F-RISK-03 — Comment.author lazy="joined" JOIN 비용

- **시나리오**: 한 게시글의 댓글 100건 이상 시 JOIN 비용 누적 (Article과 동일 패턴)
- **완화**: RealWorld 사용 시나리오는 한 게시글 댓글 평균 5~10건 — JOIN 1회로 sufficient. 100건 이상 케이스는 본 MVP out of scope. 미래 측정 필요 시 selectinload 전환 (1줄 변경)
- **트리거 시점**: 운영 단계 — 본 MVP에서는 측정 불필요

### F-RISK-04 — Alembic 0004 head 미적용 시 500

- **시나리오**: `uv run alembic upgrade head` 누락 시 GET /comments 호출이 `no such table: comments`로 500 응답
- **완화**: LOCAL.md §3 + 12-scaffolding §5 빌드·실행 절차에 `uv run alembic upgrade head` 명시 (I-01부터 정착). P10 AI QA Test Plan 4블록에 마이그레이션 step 포함
- **트리거 시점**: fresh checkout 부팅 시 — `0004 (head)` 정합 확인

## 3. High 등급 단계적 롤아웃

(없음) — 4 F-RISK 모두 Low. 단계적 롤아웃 plan 강제 N/A. ADR-0032·ADR-0046·branch-strategy.md 기본 정책으로 충분.

## 4. 데이터 영속성 변경

- **신규 테이블**: `comments` 1개 — id PK / body TEXT NOT NULL / author_id FK CASCADE users / article_id FK CASCADE articles / created_at / updated_at
- **신규 인덱스**: `ix_comments_article_id` (list_by_article 쿼리 최적화)
- **기존 테이블 무변경**: users / articles / tags / article_tags / alembic_version 모두 그대로
- **데이터 손실 가능성**: 신규 테이블이라 0. downgrade 시 comments drop만 (article 삭제 시 비활성 데이터)

## 5. 15-risk.md 갱신 항목

(없음) — 기존 8 RISK-ID에 본 변경 영향 없음. RISK-03(SQLAlchemy async)는 Article/User 이미 검증된 패턴 재사용으로 영향 적음. 15-risk.md v0.1 무수정 유지.
