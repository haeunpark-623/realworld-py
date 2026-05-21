---
doc_type: feature-contract
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

# feat-frontend-scaffold — Change Contract

> P3 (ADR-0018). §0 Referenced-IDs로 선택적 정본 진입. mode=add — frontend 워크스페이스 신규 도입.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — §0 6행 + §2 Before/After 16행 + §3 Call Sites 3행 + BC neutral + Rollback 1-commit revert |

## 0. 참조 정본 ID (Referenced-IDs)

| 종류 | 정본 위치 | 영향 ID |
| --- | --- | --- |
| SRS | `docs/planning/04-srs/04-srs.md` §6 R-N-02 (FCP < 1.5s) | R-N-02 |
| PRD | `docs/planning/05-prd/05-prd.md` §3 F-04 (UI 모듈) | F-04 |
| LLD-Screen | `docs/planning/10-lld-screen-design/10-lld-screen-design.md` §1 화면 인벤토리 6종 + §3 디자인 토큰 (Color/Typography/Spacing/Component primitives) | (none) |
| Scaffolding | `docs/planning/12-scaffolding/python.md` §1 frontend 트리 + §5 빌드·실행 + §8 스타일링 솔루션 Tailwind | (none) |
| ADR | `docs/planning/adr/0002-frontend-spa.md` React+Vite+TS / `adr/0004-styling-tailwind.md` Tailwind | (none) |
| Test Catalog | N/A — 본 이슈 테스트 시나리오 0건 (WBS DoD N/A 명시) | (none) |

## 1. 변경 의도

frontend 워크스페이스를 신규 도입해 I-08(auth UI) + I-09(게시판) 진입 기반 마련. Vite + React 18 + TypeScript + Tailwind 3 + react-router-dom v6 + zustand. 6 라우트 placeholder + Header + api client + auth store + Vite proxy. 부팅은 backend(8000)와 frontend(5173) 분리.

**환경 결정**: pnpm 미설치 → **npm 11.x 채택**. lockfile은 `package-lock.json`. 점진 합의 — ADR 신설 없이 본 contract + plan §5 + 14-wbs 변경 이력에서 trace.

## 2. Before / After

| 항목 | Before | After |
| --- | --- | --- |
| `frontend/` 디렉토리 | 없음 | 신규 Vite 워크스페이스 |
| `frontend/package.json` | 없음 | 신규 — name realworld-frontend / type module / scripts dev·build·preview / deps react ^18.3 + react-dom ^18.3 + react-router-dom ^6.28 + zustand ^4.5 / devDeps vite ^5.4 + @vitejs/plugin-react ^4.3 + typescript ^5.6 + @types/react ^18.3 + @types/react-dom ^18.3 + tailwindcss ^3.4 + postcss ^8.4 + autoprefixer ^10.4 |
| `frontend/package-lock.json` | 없음 | 신규 (npm install 후 commit) |
| `frontend/vite.config.ts` | 없음 | 신규 — `@vitejs/plugin-react` + `server.proxy['/api'] = http://localhost:8000` |
| `frontend/tsconfig.json` + `tsconfig.node.json` | 없음 | 신규 — strict + ES2022 + JSX react-jsx |
| `frontend/index.html` | 없음 | 신규 — `<div id="root">` + `<script type="module" src="/src/main.tsx">` |
| `frontend/tailwind.config.js` | 없음 | 신규 — content `./index.html` + `./src/**/*.{ts,tsx}` |
| `frontend/postcss.config.js` | 없음 | 신규 — tailwindcss + autoprefixer |
| `frontend/.env.example` | 없음 | 신규 — `VITE_API_BASE_URL=/api` |
| `frontend/.gitignore` | 없음 | 신규 — node_modules/ + dist/ + .env |
| `frontend/src/main.tsx` | 없음 | 신규 — `import './index.css'` + StrictMode + App |
| `frontend/src/App.tsx` | 없음 | 신규 — BrowserRouter + Header + 6 Routes placeholder |
| `frontend/src/index.css` | 없음 | 신규 — `@tailwind base; @tailwind components; @tailwind utilities;` |
| `frontend/src/vite-env.d.ts` | 없음 | 신규 — `/// <reference types="vite/client" />` |
| `frontend/src/pages/{HomePage,ArticlePage,EditorPage,LoginPage,RegisterPage,ProfilePage}.tsx` | 없음 | 신규 6 placeholder — 각 페이지 `<h1>{화면명}</h1>` + Tailwind 클래스 1+ |
| `frontend/src/components/Header.tsx` | 없음 | 신규 — 로고 + 메뉴 placeholder |
| `frontend/src/api/client.ts` | 없음 | 신규 — `apiFetch<T>(path, init)` fetch 래퍼 + Authorization 헤더 placeholder |
| `frontend/src/store/auth.ts` | 없음 | 신규 — zustand store placeholder (user/token + login/logout/loadFromStorage actions) |
| `frontend/src/types/api.ts` | 없음 | 신규 — RealWorld spec 응답 타입 placeholder (UserResponse/ArticleResponse 등) |

## 3. 호출자·의존자 (Call Sites)

| 위치 | 영향 | 조치 |
| --- | --- | --- |
| 사용자 CLI: `(cd frontend && npm install && npm run dev)` | 신규 부팅 자산 | LOCAL.md §3 + 12-scaffolding §5에 명령 추가 (양축 동기, ADR-0040) |
| backend `realworld.main` CORS 허용 | dev origin `http://localhost:5173` | 무수정 — 기존 `CORS_ORIGINS` 기본값에 5173 포함 (I-01 정착) |
| GitHub Actions `backend-ci.yml` | frontend 변경 미감지 | 무수정 — `paths: [backend/**, docs/**]` 트리거 (I-01). frontend-ci 별도는 본 PR scope out |

## 4. Backward Compatibility

**BC neutral** — 신규 워크스페이스만 추가, backend·docs 무수정.

- backend 영향: 0 — pytest 77 passed 회귀 N/A (backend 미변경)
- 기존 `.env.example`(backend)·alembic·LOCAL.md 본문 부팅 자산: 0 변경 (LOCAL.md §3에 frontend 명령 *추가*만)
- CI: backend-ci 트리거 `paths: backend/**` 한정이라 frontend 파일 변경 시 미실행 — pr-body-checkboxes status check만 active

## 5. Rollback 전략

**1-commit revert로 충분**.

- 코드 revert: `git revert <PR commit>` — squash merge 단일 commit 되돌리기. frontend/ 일괄 제거
- 부팅 자산 revert: LOCAL.md §3 frontend 명령 자동 revert 포함. backend 부팅 영향 0
- 데이터 영속성 영향: 0 (frontend stateless, localStorage는 I-08부터)

리스크 등급 Low — F-RISK risk.md에서 4건 식별.

## 6. 비목표

- **컴포넌트 라이브러리 도입**: 10-lld-screen-design §3.4 결정 — Tailwind utility-first 직접 구현
- **테스트 인프라(Vitest 등)**: 본 이슈 WBS DoD N/A. I-09 골든패스 E2E만 도입
- **frontend-ci 워크플로**: 본 PR scope out — I-10에서 결정 가능
- **Service Worker / PWA**: out of scope (RFP §3)
- **다국어 i18n**: out of scope (10-lld-screen-design §5 Open Q 4)
