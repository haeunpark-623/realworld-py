# realworld-py

RealWorld(Conduit) 게시판 풀스택 구현 — Python(FastAPI) + React(Vite) — **AI 페어 개발 학습 과제** (2026-05-20~2026-05-21, 2일 ~16h).

## 프로젝트 개요

- **목표**: AI(Claude Code + agent-toolkit) 활용한 풀 사이클 개발(요구 분석 → 설계 → 구현 → 검증 → 배포 준비)을 2일 안에 1회 완주
- **결과**: Sprint 1·2 × 10 이슈 모두 머지 — backend(인증·게시글·댓글) + frontend(6 화면 SPA) + 골든패스 E2E + LOCAL.md 부팅 가이드 완비
- **상세**: [`docs/planning/INDEX.md`](docs/planning/INDEX.md) (Phase 1~4/4 산출 14건 + ADR 4건)

## 기술 스택

- **백엔드**: FastAPI 0.115 + Python 3.11 + Pydantic v2 + SQLAlchemy 2 async + Alembic + SQLite (aiosqlite) + bcrypt + JWT(python-jose HS256) + uv 패키지 매니저
- **프론트엔드**: React 18.3 + Vite 5.4 + TypeScript 5.6 strict + Tailwind CSS 3.4 + react-router-dom 6.28 + zustand 4.5 + npm 11
- **테스트**: pytest 8 + pytest-asyncio + httpx + aiosqlite (단위 42 + 통합 32 + health 3 = 77 passed)
- **인프라**: 로컬 dev 1 profile 운영 (stg/prod N/A — RFP §NFR-06). GitHub Actions backend-ci pytest 워크플로 1개

## 빠른 시작

부팅 가이드 정본: **[`LOCAL.md`](LOCAL.md)** (5분 부팅 절차 + 함정 안내 + Troubleshooting).

```bash
# 1) 의존성 설치
(cd backend && uv sync)
(cd frontend && npm install)

# 2) .env 준비
cp backend/.env.example backend/.env   # JWT_SECRET을 랜덤 값으로 채움
cp frontend/.env.example frontend/.env

# 3) DB 스키마 적용
(cd backend && uv run alembic upgrade head)

# 4) seed 데이터 (선택, R-N-01 측정용)
(cd backend && uv run python -m scripts.seed_articles)

# 5) 동시 부팅 (2 터미널)
(cd backend && uv run uvicorn realworld.main:app --reload --port 8000)
(cd frontend && npm run dev)
```

브라우저: <http://localhost:5173> · API 문서: <http://localhost:8000/docs>.

## 사이클 산출

| Phase | 산출 | 위치 |
| --- | --- | --- |
| 1/4 의도·요구 | 01 Project Brief / 02 Feasibility / 03 User Scenarios / 04 SRS / 05 PRD | [`docs/planning/`](docs/planning/) |
| 2/4 설계 | 06 Architecture / 07 HLD / 08 LLD Module / 09 LLD API / 10 LLD Screen / 11 Conventions / 12 Scaffolding / 13 Test Design | [`docs/planning/`](docs/planning/) |
| 3/4 운영 | 14 WBS / 15 Risk | [`docs/planning/`](docs/planning/) |
| 4/4 외부 등록 | GitHub Milestones + Issues + Labels + Projects v2 (Sprint 1·2 × 10 이슈) | GitHub |
| ADR | 0001 FastAPI / 0002 React+Vite / 0003 SQLite / 0004 Tailwind | [`docs/planning/adr/`](docs/planning/adr/) |
| 사이클 회고 | 2026-05-21 cycle retro | [`docs/planning/retro/`](docs/planning/retro/) |

## 회고

본 사이클(2일 ~16h)의 잘된 점·개선점·메모: **[`docs/planning/retro/2026-05-21-cycle.md`](docs/planning/retro/2026-05-21-cycle.md)**.

## 변경 이력

릴리즈 노트: **[`CHANGELOG.md`](CHANGELOG.md)** (v0.1.0 first release).

## 라이선스

학습 과제. 외부 배포·상업 사용 out of scope (RFP §5).