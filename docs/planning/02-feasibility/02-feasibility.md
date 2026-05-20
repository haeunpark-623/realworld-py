---
doc_type: feasibility
version: v0.2 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: A
related:
  R-ID: []
  F-ID: []
  supersedes: null
---

# realworld-py — Feasibility

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.2 | 2026-05-20 | woosung.ahn@bespinglobal.com | 게이트 A·B 사용자 결정 반영 — 백엔드 FastAPI / 프론트엔드 SPA(React+Vite) 채택. §2 표·§6 추천에 마킹 |
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-init` Phase 1/4, ADR-0013 ≤ 1장 강제) |

## 1. 시장·환경 검토

- **시장 사용 여부 N/A** — 본 프로젝트는 사내 학습 과제로, 외부 사용자/시장 진입을 목표하지 않는다.
- **레퍼런스 풍부** — RealWorld(Conduit) 스펙은 60+ 언어/프레임워크 구현체가 공개되어 있어 막힘 시 비교 학습 가능. 단, 그대로 카피하지 않고 "본인 작성" 원칙은 유지.
- **법·라이선스** — RealWorld 스펙은 학습 용도 사용 허용. 본인 작성 코드의 저작권은 본인 보유.

## 2. 기술 타당성

| 영역 | 후보 | 본 학습 컨텍스트 적합도 | 비고 |
|---|---|---|---|
| 백엔드 언어 | Python (강제) | — | RFP §NFR-01에서 확정 |
| 백엔드 프레임워크 | **FastAPI ✅ (채택)** / Django / Flask | Pydantic + OpenAPI 자동 생성으로 SPA·09-api-spec 친화 | 게이트 B 사용자 결정 (v0.2). `/flow-design`에서 ADR로 정식화 |
| 데이터베이스 | SQLite / PostgreSQL | SQLite = 로컬 부팅 ≤ 5분 충족 유리. PostgreSQL은 운영 정합성 우수 | 단일 환경 운영(RFP §NFR-06)이므로 SQLite도 충분. 게이트 C 확정 |
| 프론트엔드 | Jinja2 + HTMX (서버 렌더링) / **React + Vite ✅ (SPA, 채택)** | FastAPI REST와 자연 결합. ADR-0038 스타일링 솔루션 채택 강제 | 게이트 B 사용자 결정 (v0.2). FCP 1.5s 미달 리스크는 코드 스플리팅으로 게이트 C에서 점검 |
| 인증 | JWT + bcrypt | 표준 패턴. Python 생태계 라이브러리 충분 (`pyjwt`, `passlib[bcrypt]`, FastAPI의 `OAuth2PasswordBearer`, Django의 `django.contrib.auth`) | RFP §NFR-04 강제 |
| 테스트 | pytest (+ pytest-cov, httpx/TestClient 또는 pytest-django) | 표준. 풍부한 fixture/factory 생태계 | 게이트 C `13-test-design`에서 확정 |
| 린트·포맷 | ruff + black + (선택) mypy | ruff 1개로 lint·import 정렬·일부 자동수정. 2일 마감에 부담 적음 | 게이트 C `11-coding-conventions`에서 확정 |
| 빌드·실행 | `uv run` 또는 `python -m` 직호출 | `uv`(Astral) = 의존성·가상환경·실행 통합. 부팅 ≤ 5분 충족 유리 | LOCAL.md §3 + `12-scaffolding/python.md` §5에서 양축 동기 (ADR-0040·0041) |
| CI | GitHub Actions 1개 워크플로 (pytest) | 무료 한도 안에서 충분. ADR-0047 매 PR 로컬 + GitHub 양축 검증은 `act`로 로컬 reproduce 가능 | 단일 워크플로면 act 호환 손쉬움 |

**결론**: 기술 타당성 OK. 어떤 프레임워크 조합도 2일 안에 MVP 완주 가능선 안에 있다. 핵심 리스크는 *결정 지연* 자체(RISK-02).

## 3. 비용·리소스 추정

| 항목 | 추정 |
|---|---|
| 개발 인력 | 1명 (박하은) + AI 페어(agent-toolkit) |
| 개발 시간 | ≈ 16h (2일 × 8h 가정, 회의/휴식 제외) |
| 클라우드 비용 | 0원 (로컬 부팅만 필수, 클라우드 배포 Out of Scope) |
| 외부 서비스 | 0건 (이메일·SMS·결제 등 외부 의존 없음) |
| AI 사용 비용 | Claude Code 토큰 비용 (회사 계정, 본 학습 과제 범위 내 흡수) |
| 학습 도구 비용 | 0원 (Python·pytest·SQLite·Postgres 모두 무료, Docker 옵션) |
| GitHub | 0원 (개인/회사 계정 무료 한도) |

**결론**: 비용은 사실상 시간 16h가 전부. 외부 의존이 없어 비용 리스크 0.

## 4. 기대 효과

- **학습 효과 (1차)** — agent-toolkit 풀 사이클(NEW_PROJECT 4 Phase + FEATURE 사이클)을 1회 완주하는 경험. AI 게이트 6축, 부팅 자산 동기, 브랜치 전략, ADR 작성 등 *툴킷 규칙*을 몸으로 익힘.
- **산출 효과 (2차)** — 동작하는 게시판 + 14종 산출 문서가 향후 다른 프로젝트 시 *템플릿/체크리스트*로 재사용 가능.
- **조직 효과 (3차)** — 뉴비 온보딩 표준 코스로 본 사이클을 재사용. 후속 신규 입사자는 본 산출을 참고로 자기 RFP를 작성하면 됨.

## 5. 검토된 대안

| 대안 | 설명 | 평가 |
|---|---|---|
| A1. RealWorld 풀 spec 구현 | follow·favorite·tag feed까지 모두 | ✘ 2일 마감 초과 가능성 매우 높음. RFP §3 Out of Scope로 정리됨 |
| A2. 다른 언어로 학습 (Node·Go) | Python 제약 우회 | ✘ RFP §NFR-01에서 Python 강제 — 사내 학습 목표상 변경 불가 |
| A3. 노코드 도구로 구현 (Bubble·Retool 등) | 코드 없이 게시판 | ✘ 학습 목표 = "AI 활용 풀 *코드 개발* 사이클" — 노코드는 학습 목표 불일치 |
| A4. AI 없이 직접 구현 | agent-toolkit 미사용 | ✘ "AI 활용" 학습이 본 과제 핵심. 툴킷 사용이 의무 |
| **B. MVP만 구현 + 툴킷 풀 사이클 (RFP 채택안)** | F-01~F-04 + agent-toolkit | ✅ 일정·학습 목표·리소스 모두 부합. **추천** |

## 6. 추천

**B (MVP만 + agent-toolkit 풀 사이클)** 채택. 다음 메타 `/flow-design`으로 넘어가 *DB*와 *세부 라이브러리 조합*을 ADR로 확정한다.

### 6.1 게이트 B 시점 사전 결정 (v0.2)

RISK-02(프레임워크 결정 지연)를 줄이기 위해 게이트 B 검토에서 다음을 사전 결정했다. `/flow-design`은 본 결정을 ADR로 정식화만 하면 된다.

| 항목 | 결정 | 사유 |
|---|---|---|
| 백엔드 프레임워크 | **FastAPI** | SPA·09-api-spec 친화. Pydantic·OpenAPI 자동 생성으로 산출 부담 감소 |
| 프론트엔드 렌더링 | **SPA (React + Vite)** | FastAPI REST와 자연 결합. 학습성 우수 |
| 단위 테스트 정량 | **ADR-0015 §2.3 정책값(≥ 80%) 채택** | RFP 값 예외 ADR 신설 안 함. 04-srs §R-N-06 범위(*인증·권한·CRUD 핵심 서비스*) 한정 |
| 게시글 삭제 방식 | **hard delete** | 학습 컨텍스트 단순성. 운영 시나리오 학습은 후속 과제 |
| slug 충돌 규칙 | **숫자 suffix** (예: `my-post-2`, `my-post-3`) | 단순성. nanoid 등 추가 의존 회피 |
| F-03 댓글 수정 | **MVP 포함** | RealWorld spec 일부. SRS·PRD에 R-F-13 신규 추가 |
| F-04 UI 단위 테스트 | **N/A 확정** | E2E 1회로 대체. 학습 범위 단순화 |

### 6.2 게이트 C에서 결정할 잔여 항목

- **데이터베이스**: SQLite vs PostgreSQL (ADR 후보)
- **스타일링 솔루션**: ADR-0038 강제 — Tailwind / CSS Modules / styled-components 등 1개 채택
- **세부 라이브러리**: SQLAlchemy / Alembic / passlib / pyjwt 등 조합
- **테스트 fixture·factory 도구**: pytest-factoryboy 등 채택 여부
