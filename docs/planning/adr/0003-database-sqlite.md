---
doc_type: adr
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: [R-N-01, R-N-04, R-N-06]
  F-ID: [F-02, F-03]
  supersedes: null
---

# ADR 0003 — 데이터베이스 SQLite 채택 (단일 환경 운영)

- **상태**: Draft
- **결정일**: 2026-05-20
- **작성**: 박하은 <woosung.ahn@bespinglobal.com>

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — 게이트 C에서 SQLite vs PostgreSQL 결정, SQLite 채택 |

## 1. 컨텍스트

본 프로젝트는 *단일 환경 운영*(RFP §NFR-06, dev 1 profile)이며 1~5명 동시 사용자 학습 컨텍스트. 데이터 모델은 User·Article·Comment·Tag 4개 테이블 + 단순 관계. 게이트 B(v0.2)에서 잔여 결정으로 남았던 항목.

- 부팅 ≤ 5분 충족 (RFP §6 DoD §1) — 외부 DB 컨테이너 추가 시 첫 부팅 시간 증가 위험
- 학습 컨텍스트 — DB 설치·운영 학습이 본 과제 핵심은 아님 (SQL·ORM 사용 학습이 핵심)
- 외부 서비스 의존 0건 원칙 (06-architecture §3)
- 단일 writer 가정 — SQLite의 단일 writer 제약은 부담 없음
- 100건 게시글 + ~10건 댓글/글 규모 — 어떤 DB도 부담 없음

## 2. 결정

**SQLite** 채택. 파일 기반 (`backend/data/realworld.db`), SQLAlchemy 2.x + `aiosqlite` 비동기 드라이버.

채택 효과:
- `DATABASE_URL=sqlite+aiosqlite:///./data/realworld.db` 설정
- `backend/data/` 디렉토리는 .gitignore (DB 파일 commit 금지)
- Docker compose 등 추가 컨테이너 0건 — `uv sync` 직후 바로 부팅 가능
- SQLAlchemy 2.x `AsyncSession`으로 백엔드 코드는 PostgreSQL과 *동일*하게 작성 → 향후 PostgreSQL 전환 시 `DATABASE_URL`만 교체
- Alembic 마이그레이션 패턴은 PostgreSQL 동일 — 학습 가치 동일

## 3. 검토된 대안

### 채택안: SQLite (file-based)

- **장점**:
  - 외부 컨테이너 0건 — 부팅 ≤ 5분 충족
  - 학습 컨텍스트 + 단일 환경 운영에 충분
  - 파일 백업·이동·삭제 단순
  - CI에서도 별 DB 서비스 설정 불필요 (워크플로 simplification)
  - SQLAlchemy + Alembic 학습 효과는 PostgreSQL과 동일
- **단점**:
  - 동시 쓰기 제약 — 학습 컨텍스트에서 무시 가능
  - 일부 PostgreSQL 전용 타입(JSON·ARRAY·UUID 등) 학습 불가 — 본 MVP에서 미사용이라 문제 없음
  - 운영 환경 시나리오 학습 효과 약함 — 후속 학습 과제로 미룸

### 대안 1: PostgreSQL (Docker compose)

- **장점**:
  - 운영 정합성 — 사내 표준 운영 DB
  - 동시 쓰기·격리 수준 학습
  - JSON·ARRAY·트리거 등 풍부한 기능 학습
- **단점 (불채택 이유)**:
  - Docker 컨테이너 추가 → 부팅 ≤ 5분 충족 위험 (Docker pull 시간 가변)
  - DB 환경 변수·연결 풀 설정 등 *학습 외 부담* 증가
  - 본 MVP 규모에서 *과대* — 학습 가치 대비 부담 큼
  - CI 워크플로 복잡도 증가 (services·healthcheck 등)

### 대안 2: SQLite + 후속 PostgreSQL 전환

- 본 결정과 동일. SQLAlchemy 추상화로 향후 전환 학습이 가능하다는 점이 본 채택안의 추가 장점.

## 4. 결과 (Consequences)

### 긍정

- 부팅 명령 `uv sync && uv run alembic upgrade head && uv run uvicorn ...` 3 단계 — 학습자 진입 부담 최소
- 외부 의존 0건 원칙 유지 (06-architecture §3)
- CI 워크플로 단순화 — services 블록 없음
- 향후 PostgreSQL 전환은 `DATABASE_URL` 1줄 + 일부 타입 조정으로 가능 (별 학습 과제)

### 부정 / 트레이드오프

- 운영 환경 시나리오 학습 부재 — 트랜잭션 격리·동시 쓰기 충돌·연결 풀 등 학습 누락
- 일부 PostgreSQL 전용 기능 학습 누락 (JSON 쿼리, RLS 등)
- SQLite의 동시 쓰기 제약은 학습 컨텍스트에서는 무시 가능하지만 *운영 시*는 즉시 한계

### 영향 받는 문서

- 06-architecture §Stack Decision + §2.1 (SQLite 명시)
- 08-lld-module-spec §1·§3 (Repository SQLAlchemy 가정 — DB 종류 비의존)
- 12-scaffolding/python.md §1 (data/ 디렉토리) + §6 (`DATABASE_URL`) + §7 (스키마 적용)
- LOCAL.md §1 (DB 설치 0건) + §2 단계 4 (`alembic upgrade head` 단일 명령) + §4 (자산 표)
- 13-test-design 01-strategy §2 도구 선택 (sqlite:///:memory: 인메모리 통합 테스트)

## 5. 추적 / 재검토 시점

- **재검토 트리거**:
  - 동시 사용자 시나리오 학습이 필요해질 때 (별 과제)
  - 게시글 수가 1만 건+로 증가할 때 (현재 100건 시드 가정)
  - JSON·ARRAY 등 PostgreSQL 전용 기능이 새 요구사항으로 들어올 때
- **재검토 주기**: 본 학습 과제 1회성. 후속 과제 `realworld-py-v2`에서 PostgreSQL 채택 가능.
