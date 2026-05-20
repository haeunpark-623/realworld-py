---
doc_type: architecture
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-09, R-F-10, R-F-11, R-F-12, R-F-13, R-N-01, R-N-02, R-N-03, R-N-04, R-N-05, R-N-06]
  F-ID: [F-01, F-02, F-03, F-04]
  supersedes: null
---

# realworld-py — System Architecture

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, ADR-0031 본체 축소 — 시스템 컨텍스트·Stack·컨테이너 구조만) |

## Stack Decision

| 항목 | 결정 | 근거 |
|---|---|---|
| 언어 (backend) | Python 3.11 | RFP §NFR-01 강제 + FastAPI · SQLAlchemy 호환 stable. 3.12+는 일부 라이브러리 호환 미검증, 학습 안전성 우선 |
| 프레임워크 (backend) | FastAPI | 게이트 B 결정 (v0.2). Pydantic·OpenAPI 자동 생성으로 09-api-spec 산출 부담 감소 + REST·SPA 친화. [ADR-0001](../adr/0001-backend-framework.md) |
| 언어 (frontend) | TypeScript 5.x | SPA 학습성 + 타입 안전. React 19 권장 조합 |
| 프레임워크 (frontend) | React 19 + Vite 5 (SPA) | 게이트 B 결정 (v0.2). FastAPI REST와 자연 결합. [ADR-0002](../adr/0002-frontend-spa.md) |
| 데이터베이스 | SQLite (file-based) | 게이트 C 결정 (본 메타). 단일 환경 운영(RFP §NFR-06) + 부팅 ≤ 5분 충족 + Docker 의존 없음. SQLAlchemy + aiosqlite 드라이버. [ADR-0003](../adr/0003-database-sqlite.md) |
| ORM / 마이그레이션 | SQLAlchemy 2.x + Alembic | Python 생태계 표준. 학습성 우수. 비동기 지원 |
| 인증 | JWT + bcrypt (passlib + python-jose) | RFP §NFR-04 강제 (R-N-03·R-N-04). passlib 안정성, python-jose는 FastAPI 공식 예제 |
| 스타일링 | Tailwind CSS 3.x | 게이트 C 결정. Vite 공식 플러그인, utility-first, 디자인 토큰 매핑 용이. [ADR-0004](../adr/0004-styling-tailwind.md) |
| 패키지·실행 | uv (Astral) | 의존성·가상환경·실행 통합. `uv run` 단일 명령 부팅 |
| 테스트 | pytest + pytest-cov + httpx TestClient | R-N-06 ≥ 80% 측정 + FastAPI 통합 테스트 표준 |
| CI/CD | GitHub Actions 단일 워크플로 | RFP §NFR-06. pytest 실행만. ADR-0047 act 로컬 재현 |
| 인프라 | 로컬 dev 1 profile | RFP §NFR-06 단일 환경 운영 — dev/stg/prod 3 profile은 N/A |

## 1. 시스템 컨텍스트

```
                     ┌─────────────────────────────────────────────┐
                     │                Browser (Chrome)              │
                     │   ┌───────────────────────────────────┐     │
                     │   │  React SPA (Vite dev server)      │     │
                     │   │  http://localhost:5173            │     │
                     │   └───────────────┬───────────────────┘     │
                     └───────────────────┼─────────────────────────┘
                                         │ HTTPS X (로컬은 HTTP)
                                         │ Authorization: Token <JWT>
                                         ▼
                     ┌─────────────────────────────────────────────┐
                     │     FastAPI 서버 (uvicorn)                   │
                     │     http://localhost:8000                    │
                     │     /api/users · /api/articles · …           │
                     └───────────────────┬─────────────────────────┘
                                         │ SQLAlchemy ORM
                                         ▼
                     ┌─────────────────────────────────────────────┐
                     │     SQLite (./data/realworld.db)             │
                     │     User · Article · Comment · Tag           │
                     └─────────────────────────────────────────────┘

  외부 시스템 의존: 없음 (이메일·SMS·결제·푸시·OAuth Out of Scope)
  관측 / 로깅: stdout 로깅만, 외부 APM Out of Scope
```

- **사용자 경계**: Browser (Chrome 데스크톱/모바일)에서 직접 진입
- **클라이언트 ↔ 서버 경계**: HTTP, RealWorld spec(`Authorization: Token <JWT>`)
- **서버 ↔ DB 경계**: SQLAlchemy ORM (raw SQL 금지, R-N-05)
- **외부 시스템 경계**: 없음

## 2. 컨테이너 구조

본 프로젝트는 다음 3개 컨테이너(논리적 단위)로 구성된다.

### 2.1 컨테이너 인벤토리

| 컨테이너 | 기술 | 책임 | 포트(로컬) | 배포 단위 |
|---|---|---|---|---|
| Frontend SPA | React 19 + Vite 5 + TypeScript + Tailwind | UI 렌더링, JWT 보관(localStorage), REST API 호출, 클라이언트 라우팅 | 5173 (dev) | `frontend/` |
| Backend API | FastAPI + uvicorn + Python 3.11 | REST API 제공, 인증·권한·비즈니스 로직, ORM 트랜잭션 | 8000 | `backend/` |
| Database | SQLite (file) | User·Article·Comment·Tag 영속화 | — (file) | `data/realworld.db` |

> 컨테이너화(Docker)는 학습 컨텍스트에서 선택. dev는 native 부팅(uvicorn + vite) 기본.

### 2.2 컨테이너 간 통신

| 출발 → 도착 | 프로토콜 | 형식 | 인증 |
|---|---|---|---|
| Frontend → Backend | HTTP/1.1 | JSON (`Content-Type: application/json`) | `Authorization: Token <JWT>` (RealWorld spec, R-F-03) |
| Backend → SQLite | 파일 I/O (SQLAlchemy driver) | SQL | 파일 시스템 권한 |

### 2.3 모노레포 디렉토리 큰 그림

```
realworld-py/
├── backend/                  # FastAPI 서버 컨테이너 — 12-scaffolding/python.md §1 상세
├── frontend/                 # React SPA 컨테이너 — 12-scaffolding/typescript.md §1 (후속 생성)
├── data/                     # SQLite 파일 (gitignore)
├── docs/planning/            # 14 산출 문서
├── .github/workflows/        # CI (pytest)
├── LOCAL.md                  # 부팅 가이드
└── CLAUDE.md                 # 툴킷 지침
```

> 본 메타에서는 `12-scaffolding/python.md` 만 작성 (백엔드 학습 1차 목표). frontend SPA scaffolding은 `12-scaffolding/typescript.md`로 후속 작성(필요 시) — 본 프로젝트는 frontend 부담을 최소화하기 위해 가장 단순한 Vite 템플릿을 그대로 사용한다.

## 3. 외부 시스템 / 경계

| 외부 시스템 | 사용 여부 | 비고 |
|---|---|---|
| 이메일 / SMS | ❌ | 비밀번호 찾기·이메일 검증 Out of Scope (RFP §3) |
| 결제 | ❌ | N/A |
| OAuth Provider (Google/GitHub) | ❌ | 자체 JWT만 (R-F-02). OAuth 통합 Out of Scope |
| 외부 파일 저장소 (S3 등) | ❌ | 프로필 이미지 업로드 Out of Scope |
| 외부 로깅·APM (Sentry/Datadog) | ❌ | stdout 로깅만 |
| 외부 검색 (Elasticsearch) | ❌ | 게시글 100건 수준, DB LIKE로 충분(후속 검토) |
| 외부 CDN | ❌ | 로컬 부팅만 |

본 시스템은 *self-contained* 하다 — 외부 의존 0건. 학습 과제 본 목적에 부합한다.
