---
doc_type: feature-risk
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

# feat-users-articles — Feature Risk

> Issue #4 / Sprint 1 / I-04. 7 FRISK (6 Low + 1 Medium). High 등급 0 → 단계적 롤아웃 N/A.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 7 FRISK 식별. High 등급 0건 |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| FRISK-01 | alembic autogenerate가 모델 변경 일부 누락 (M2M secondary 등 미감지) | 3 | 2 | Low |
| FRISK-02 | slug 동시 race (동일 title 동시 POST 2회) → UNIQUE 충돌 → 한쪽 500 | 2 | 1 | Low |
| FRISK-03 | selectinload 누락으로 통합 테스트에서 N+1 발현 + 응답 시간 ↑ | 2 | 2 | Low |
| FRISK-04 | exception_handlers가 RealWorldError subclass별 분기 잘못 → 모두 500 | 4 | 1 | Medium |
| FRISK-05 | Pydantic v2 RealWorld 래핑 형식 (`{user: {...}}`)이 자동 검증과 충돌 | 2 | 1 | Low |
| FRISK-06 | tag 다대다 — 빈 tagList 시 빈 배열 응답 vs null 응답 일관성 | 1 | 2 | Low |
| FRISK-07 | 통합 테스트 fixture isolation 부재 → 테스트 간 DB state 누수 | 2 | 2 | Low |

## 2. 리스크 상세

### FRISK-01 — alembic autogenerate 누락

- **원인**: M2M secondary table은 SQLAlchemy declarative + Table() 패턴이라 autogenerate가 가끔 association table을 빠뜨림
- **완화**: alembic upgrade 후 `sqlite3 backend/dev.db ".schema"`로 3 테이블 + FK + UNIQUE 직접 확인. autogenerate 결과를 *수기 검토* 후 commit
- **fallback**: 누락 시 수기 `op.create_table('article_tags', ...)` 보강 후 0003 재생성

### FRISK-02 — slug 동시 race

- **원인**: UNIQUE 제약 + 카운터 패턴은 트랜잭션 격리 없으면 race
- **완화**: 04-srs §R-F-06 Failure-3에 Out 명시. 본 MVP는 1~5명 동시 사용자 가정으로 발현 거의 0. SQLite는 직렬 write라 자체 보호
- **fallback**: 발현 시 422 응답 (드물게)

### FRISK-03 — N+1 회피

- **원인**: ArticleRepo.list_with_filters가 author 또는 tags를 lazy load하면 N+1
- **완화**: `selectinload(Article.author)` + `selectinload(Article.tags)` 명시. 통합 테스트에서 SQLAlchemy echo로 query count 확인
- **검증**: pytest fixture에서 `engine.echo = True` 옵션 + count 어서션 (선택적, 본 MVP는 visual 확인)

### FRISK-04 — exception_handler 분기

- **원인**: `@app.exception_handler(RealWorldError)` 1개 핸들러가 `exc.status_code` 속성 기반 분기. 잘못 처리 시 모두 500
- **완화**: 단위 테스트로 6 도메인 예외 → 6 status code 매핑 검증. 통합 테스트로 실제 422/401/403/404 응답 확인
- **fallback**: 발현 시 핸들러 로직 수정 + 통합 테스트 추가

### FRISK-05 — Pydantic v2 래핑

- **원인**: RealWorld spec `{"user":{...}}` 형식은 Pydantic 자동 검증과 충돌 가능 (root model)
- **완화**: 명시적 wrapper class — `class UserResponseWrapper(BaseModel): user: UserResponse`. 라우터 함수 return 시 `UserResponseWrapper(user=...).model_dump()`
- **검증**: 통합 테스트가 응답 JSON 구조 직접 어서션

### FRISK-06 — 빈 tagList 일관성

- **원인**: 빈 배열 vs null은 클라이언트(React) 처리 차이
- **완화**: 항상 빈 배열 `[]` 반환. Pydantic Field default_factory=list. PUT 시 None은 omit, `[]`는 명시적 삭제

### FRISK-07 — 통합 테스트 fixture isolation

- **원인**: in-memory aiosqlite가 함수 scope면 격리, session scope면 누수
- **완화**: pytest-asyncio + sqlalchemy AsyncEngine을 function scope fixture로 — 매 테스트마다 새 DB. 14건+ 테스트라 시간 부담 무시 가능
- **검증**: 테스트 순서 무관하게 PASS 확인 (`pytest -p no:randomly`로 한번, default 순서로 한번)

## 3. High 등급 단계적 롤아웃

해당 없음 — High 등급 FRISK 0건. FRISK-04 Medium은 단위·통합 테스트로 사전 검증 충분.

## 4. 데이터 영속성 변경

- **신규 테이블 3개**: `articles`, `tags`, `article_tags`
- **기존 테이블 0개 변경**: `users` 변경 없음. User.id가 articles.author_id FK target일 뿐
- **FK 정책**: Article.author_id → users.id ON DELETE CASCADE (R-F-08 댓글 CASCADE와 일관)
- **인덱스**: articles.slug UNIQUE + articles.author_id INDEX (R-F-12 author 필터 성능)
- **마이그레이션 가역성**: alembic downgrade 0002로 0003 revert 가능. dev SQLite는 데이터 손실 허용

## 5. 15-risk.md 갱신 항목

- 본 PR이 15-risk RISK-01 (일정 = MVP 마감 2026-05-22) Mitigation Plan 단계 5/8 완료 — Sprint 1 backend 마감 진행
- FRISK-04 Medium은 15-risk RISK-03 (보안) 카테고리와 무관 (예외 처리 정확성은 보안이 아닌 동작 정확성). 별도 등록 불필요
- 후속 P13 docs-update에서 14-wbs Issue #4 status:in-review 전이 기록만 갱신
