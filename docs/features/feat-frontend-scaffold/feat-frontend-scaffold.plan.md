---
doc_type: feature-plan
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

# feat-frontend-scaffold — Implementation Plan

> P4 (ADR-0018). 3 commit DAG: C1 프로젝트 셋업 (package + Vite + Tailwind config) → C2 src/ 구조 (라우트+페이지+컴포넌트+store+api) → C3 docs sync (P13).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 3 commit DAG + ADR-0021 정규식 통과 (chore/feat/docs) + 빌드 검증 4단계 + 점진 합의 4건 |

## 1. 커밋 시퀀스 (DAG)

| # | 커밋 | 영향 파일 | 테스트 추가 | 회귀 위험 |
| --- | --- | --- | --- | --- |
| C1 | `chore(frontend): I-07 Vite + React + TS + Tailwind 프로젝트 셋업 (#7)` | `frontend/package.json` 신규 + `package-lock.json` (npm install 후) + `vite.config.ts` + `tsconfig.json` + `tsconfig.node.json` + `index.html` + `tailwind.config.js` + `postcss.config.js` + `.env.example` + `.gitignore` + `src/index.css` + `src/vite-env.d.ts` | (없음) | 0 — backend 무수정, 신규 워크스페이스 |
| C2 | `feat(frontend): I-07 6 라우트 placeholder + Header + auth store + api client (#7)` | `src/main.tsx` + `src/App.tsx` + `src/pages/{HomePage,ArticlePage,EditorPage,LoginPage,RegisterPage,ProfilePage}.tsx` + `src/components/Header.tsx` + `src/api/client.ts` + `src/store/auth.ts` + `src/types/api.ts` | (없음) | 0 — 모두 placeholder, 실 API 호출 0 |
| C3 | `docs(plan): feat-frontend-scaffold + LOCAL.md + 12-scaffolding + 14-wbs (#7)` | feature docs 8 + LOCAL.md §3·§4 + 12-scaffolding python.md §1·§5·§8 + 14-wbs v0.10 + INDEX v0.11 | (없음) | 0 — docs만 |

ADR-0021 정규식 통과 검증: `^(feat|fix|chore|test|docs|refactor|perf|style|build|ci|revert)\([a-z0-9-]+\): .+` — 3 커밋 모두 OK.

## 2. 의존성 그래프

```
C1 (프로젝트 셋업) ─→ C2 (src 구조)
                          │
                          ▼
                    C3 (docs sync, P13)
```

- **C1 → C2**: src/ 구조는 tsconfig.json + vite.config.ts에 의존. C1 npm install + Vite/Tailwind 동작 검증 후 C2 진입
- **C2 → C3**: 모든 코드·부팅 확인 후 docs sync

순환 없음.

## 3. 테스트 매핑

본 이슈는 WBS DoD N/A — 테스트 추가 0건. 검증은 *수동 부팅 확인*으로 대체:

| 커밋 | 테스트 추가 위치 | 시나리오 |
| --- | --- | --- |
| C1 | (없음 — TS 컴파일·`npm install` 검증으로 대체) | 의존성 해소 + TS strict 통과 (페이지 없는 빈 상태) |
| C2 | (없음 — 수동 브라우저 검증으로 대체) | `/` HomePage / `/article/foo` ArticlePage / `/editor` EditorPage / `/login` / `/register` / `/profile/foo` 모두 placeholder 텍스트 노출 + Header 공통 표시 + Tailwind 클래스 적용 확인 |
| C2 | (없음 — `npm run build` 산출 검증으로 대체) | 빌드 산출 `dist/` 생성 + 에러 0 |
| C3 | (없음 — docs validate-doc.sh 검증으로 대체) | 모든 산출 schema PASS |

> backend `pytest -v` 회귀: N/A (backend 무수정). I-06 PR #16 머지 후 77 passed 유지

## 4. 빌드·실행 검증 단계

```bash
# 1) 의존성 설치 (최초 1회)
cd frontend && npm install

# 2) TS 컴파일 + 빌드 검증
npm run build
# expect: dist/ 생성 + 에러 0

# 3) Dev 서버 부팅
npm run dev
# expect: "VITE v5.x ready in Nms" + "Local: http://localhost:5173/"
# expect: 브라우저에서 6 라우트 placeholder 진입 가능

# 4) Backend 동시 부팅 (proxy 검증)
# (다른 터미널)
cd backend && uv run uvicorn realworld.main:app --port 8000
# frontend에서 /api/articles 호출 시 :8000으로 프록시 — I-08부터 실 검증
```

## 5. 점진 합의 / 결정 발생 항목

- **(1) 패키지 매니저: pnpm → npm 결정**: pnpm 미설치 환경 제약 → npm 11.x 채택. lockfile은 `package-lock.json`. WBS I-07 Acceptance Criteria는 `pnpm install --frozen-lockfile` 명시이지만 환경 제약으로 `npm install --frozen-lockfile` 또는 `npm ci`로 대체 실행. ADR 신설 불필요 — 본 plan §5 + contract §1 + 14-wbs v0.10 변경 이력에서 trace
- **(2) 컴포넌트 라이브러리 미도입**: 10-lld-screen-design §3.4 결정 재확인. Tailwind utility-first + JSX 직접 구현. Header.tsx도 라이브러리 미사용
- **(3) zustand vs Redux/Jotai**: 12-scaffolding §1 (Issue #7) 기존 결정 zustand 채택 유지. 학습 부담 최소화 + RealWorld 학습 컨텍스트에서 zustand 충분
- **(4) Tailwind preset(`@tailwindcss/typography` 등) 미도입**: 본 MVP는 기본 utilities로 충분. 게시글 본문 마크다운 렌더링은 I-09에서 결정 (preset 추가 vs 직접 HTML)
- **(5) `package.json` `engines.node`**: 명시 안 함 — 학습 컨텍스트 + 1인 작업. Node 22+로 가정 (Vite 5 요구사항). README 또는 LOCAL.md에 메모만
