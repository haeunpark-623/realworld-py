---
doc_type: feature-brief
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-N-02]
  F-ID: [F-04]
  supersedes: null
---

# feat-frontend-scaffold — Feature Brief

> Sprint 2 두 번째 이슈 (I-07). Vite + React + TS + Tailwind + react-router-dom + zustand 스캐폴딩. 6 라우트 placeholder + Header. I-08·I-09의 기반.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — mode=add 자동 결정. npm 채택(pnpm 미설치 점진 합의). 6 라우트 placeholder + Tailwind 3 directive |

## 1. 한 줄 의도

`frontend/`에 Vite + React 18 + TypeScript + Tailwind CSS 3 + react-router-dom + zustand 스캐폴딩을 추가하고 6 페이지 placeholder + 공통 Header + Vite proxy(`/api → :8000`) + zustand auth store placeholder + fetch api client를 도입해 I-08(auth UI) 진입 준비.

## 2. 사용자 가치

- **개발 사용자(나)**: backend dev(8000)와 frontend dev(5173) 동시 부팅 후 6 라우트(`/`·`/article/:slug`·`/editor`·`/login`·`/register`·`/profile/:username`)를 placeholder로 클릭해 라우팅 + 헤더 + Tailwind 기본 스타일 동작 확인 가능. R-N-02(FCP < 1.5s) 측정 기반 마련
- **시스템 안정성**: package-lock.json commit + Vite dev server proxy + .env.example로 fresh checkout 재현성 보장 (R-N-04 시크릿·R-N-06 부팅 자산)

## 3. 현재 상태 → 변경 후 상태

| 측면 | 현재 | 변경 후 |
| --- | --- | --- |
| `frontend/` 디렉토리 | 없음 | 신규 Vite + React + TS 워크스페이스 |
| 패키지 매니저 | (없음) | **npm 11.x** (pnpm 미설치 점진 합의. plan §5) |
| lockfile | (없음) | `frontend/package-lock.json` commit |
| 라우터 | (없음) | react-router-dom v6 + App.tsx에 6 라우트 placeholder |
| 상태 관리 | (없음) | zustand store placeholder (`store/auth.ts`) |
| 스타일링 | (없음) | Tailwind 3 + `tailwind.config.js` + `postcss.config.js` + `src/index.css` 3 directive + `main.tsx`에서 import |
| API 클라이언트 | (없음) | `api/client.ts` — fetch 래퍼 (Authorization 헤더 자동 첨부 placeholder) |
| 공통 컴포넌트 | (없음) | `components/Header.tsx` — 로고 + 메뉴 placeholder |
| Vite 설정 | (없음) | `vite.config.ts` — proxy `/api → http://localhost:8000` |
| 환경변수 | (없음) | `frontend/.env.example` — `VITE_API_BASE_URL=/api` |
| 부팅 명령 | backend 1개 | + `(cd frontend && npm install && npm run dev)` |

## 4. 모드 자동 감지 결과

**mode = add** (자동 결정, ADR-0032 규칙 4).

- 부정 시그널 0건: `type:bug` 라벨 없음 / UI/design *변경* 아닌 *초기 스캐폴딩* (design 모드 트리거 키워드 "다크모드/리브랜딩/token" 없음) / 기존 동작 변경 없음
- 라벨: `type:chore` + `area:frontend` (chore type은 mode 결정에 영향 없음 — ADR-0032 §2.1)
- 자동 결정 trace: 규칙 4 발동 → add 조용히 진행. I-01 PR #11 `feat/bootstrap-backend-issue-1` 선례 (chore type + feat/ branch prefix)

## 5. 영향 범위

**touched_areas**: 1 영역 (frontend) — Touched Areas 표 PR body 등록 N/A.

- `frontend/package.json` + `package-lock.json` — 신규
- `frontend/vite.config.ts` — 신규 (proxy 설정)
- `frontend/tsconfig.json` + `tsconfig.node.json` — 신규
- `frontend/index.html` — 신규
- `frontend/tailwind.config.js` + `postcss.config.js` — 신규
- `frontend/.env.example` + `.gitignore` — 신규
- `frontend/src/main.tsx` — 신규
- `frontend/src/App.tsx` — 신규
- `frontend/src/index.css` — 신규
- `frontend/src/vite-env.d.ts` — 신규
- `frontend/src/pages/{HomePage,ArticlePage,EditorPage,LoginPage,RegisterPage,ProfilePage}.tsx` — 신규 6 placeholder
- `frontend/src/components/Header.tsx` — 신규
- `frontend/src/api/client.ts` — 신규
- `frontend/src/store/auth.ts` — 신규
- `frontend/src/types/api.ts` — 신규
- `docs/planning/12-scaffolding/python.md` — §1 트리 + §5 빌드·실행 frontend 명령 추가 + §8 styling 솔루션 채택 명시 (P13)
- `LOCAL.md` — §3 frontend dev 부팅 명령 추가 + §4 부팅 자산 표 동기 (P13, ADR-0040)
- `docs/planning/14-wbs/14-wbs.md` v0.9 → v0.10 (I-07 in-review, P13)
- `docs/planning/INDEX.md` v0.10 → v0.11 (P13)

## 6. 비목표

- **테스트(단위·통합·E2E)**: out of scope — WBS DoD에 N/A 명시
- **실제 동작하는 API 호출**: out of scope — placeholder 페이지만, store/api는 빈 구조만. I-08에서 첫 실 동작
- **컴포넌트 라이브러리(MUI/AntD)**: out of scope (10-lld-screen-design §3.4 결정)
- **다크모드 토큰**: out of scope (10-lld-screen-design §5 Open Q 4)
- **풀 반응형**: out of scope — 기본 흐름만 (10-lld-screen-design §4)
- **frontend-ci 워크플로**: out of scope — backend-ci.yml만 유지. I-10에서 결정 가능

## 7. Open Questions

- **pnpm vs npm**: pnpm 가정(12-scaffolding §1·14-wbs I-07 AC)이었으나 환경 제약(pnpm 미설치)으로 **npm 채택**. 점진 합의로 처리 (plan §5). lockfile은 `package-lock.json`. 후속 ADR 불필요 — 학습 컨텍스트
