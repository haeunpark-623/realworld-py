---
doc_type: feature-code-review
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

# feat-frontend-scaffold — Code Review

> P9. Generator≠Evaluator self-review. 2 코드 커밋(C1·C2) 검토. PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — PASS, 6 OX 모두 PASS, NEEDS-WORK 0. build/dev 양쪽 PASS |

## 0. Verdict

**PASS** — 2 코드 커밋 모두 contract §2 16행 매핑. build 41 modules + dev 346ms ready. NEEDS-WORK 0건.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (AI self-review)
- [review_at]: 2026-05-21

## 1. 컨트랙트 충실도

contract §2 16행 매핑:

| Before/After 항목 | Before | After 구현 |
|---|---|---|
| `frontend/` | 없음 | C1 — 디렉토리 생성 |
| `frontend/package.json` | 없음 | C1 — name realworld-frontend / scripts dev·build·preview / deps 4 + devDeps 9 |
| `frontend/package-lock.json` | 없음 | C1 — npm install 140 packages 결과 |
| `frontend/vite.config.ts` | 없음 | C1 — @vitejs/plugin-react + proxy /api→:8000 |
| `frontend/tsconfig.json` + `tsconfig.node.json` | 없음 | C1 — strict + ES2022 + JSX react-jsx + noUnusedLocals + noUnusedParameters |
| `frontend/index.html` | 없음 | C1 — <div id="root"> + module script |
| `frontend/tailwind.config.js` | 없음 | C1 — content scan `./index.html`·`./src/**/*.{ts,tsx}` |
| `frontend/postcss.config.js` | 없음 | C1 — tailwindcss + autoprefixer |
| `frontend/.env.example` | 없음 | C1 — VITE_API_BASE_URL=/api |
| `frontend/.gitignore` | 없음 | C1 — node_modules + dist + .env + .vite |
| `frontend/src/main.tsx` | 없음 | C2 — StrictMode + BrowserRouter + import './index.css' |
| `frontend/src/App.tsx` | 없음 | C2 — 7 Routes (6 페이지 + /editor/:slug 수정 모드) + Header 공통 |
| `frontend/src/index.css` | 없음 | C1 — @tailwind base/components/utilities 3 directive + body font-family |
| `frontend/src/vite-env.d.ts` | 없음 | C1 — Vite 타입 + ImportMetaEnv 확장 |
| `frontend/src/pages/{HomePage,ArticlePage,EditorPage,LoginPage,RegisterPage,ProfilePage}.tsx` | 없음 | C2 — 6 placeholder + S-NN 주석 + Tailwind 클래스 1+ |
| `frontend/src/components/Header.tsx` | 없음 | C2 — 로고(Link to=/) + 4 메뉴 |
| `frontend/src/api/client.ts` | 없음 | C2 — apiFetch<T> + ApiError class + Authorization 헤더 placeholder |
| `frontend/src/store/auth.ts` | 없음 | C2 — zustand store + localStorage `realworld.token`·`realworld.user` |
| `frontend/src/types/api.ts` | 없음 | C2 — 6 type aliases (ProfileEmbed/User·Article·Comment Response 등) |

contract §3 Call Sites 3행 매핑:

| Call Site | 동작 검증 |
|---|---|
| 사용자 CLI: `(cd frontend && npm install && npm run dev)` | ✅ — npm install 140 packages in 24s + Vite ready in 346ms @ 5173 |
| backend CORS 5173 origin | ✅ — 무수정 (I-01 정착, CORS_ORIGINS 기본값에 5173 포함). I-08 실 검증 |
| backend-ci.yml `paths: backend/**` | ✅ — 무수정. frontend 변경에 트리거 안 함 (의도) |

contract §4 BC neutral, §5 Rollback 1-commit revert로 충분 — 모두 정합.

## 2. 테스트 커버리지

본 PR은 WBS DoD N/A — 자동 테스트 0건. 검증은 *수동 부팅*으로 대체:

- **build 검증**: `npm run build` → 41 modules transformed + dist/ index.html 0.40KB + assets/index-*.css 6.32KB + index-*.js 166.92KB. exit 0
- **dev 검증**: `npx vite --port 5173` → "VITE v5.4.21 ready in 346ms" + Local http://localhost:5173/. 5173 부팅 + 6 라우트 진입 + Tailwind 클래스 시각 적용 (Manual verification에서 사람 재현)
- **TS strict**: `tsc -b` 통과 (build 안에 포함). noUnusedLocals + noUnusedParameters 통과
- **backend 회귀**: N/A — backend 미수정. 77 passed 무영향

## 3. 보안 / 시크릿

- 신규 환경변수 1: `VITE_API_BASE_URL=/api` — placeholder, 시크릿 아님. `.env.example`에만 commit, 실 `.env`는 `.gitignore`
- localStorage 사용: `realworld.token` + `realworld.user` 키 — store/auth.ts placeholder. token 평문 저장은 RealWorld spec 동일 패턴 (RFP §3 학습 컨텍스트 acceptable). XSS 방어는 React JSX escape에 의존
- 외부 의존 추가: 4 deps + 9 devDeps. **npm audit moderate 2건** (esbuild + vite) — dev 서버 한정, 운영 영향 0 (vite는 production build에 미사용). 학습 컨텍스트 acceptable. 후속 vite 6+ upgrade 시 자동 해소
- 시크릿 노출 0 — 코드·로그·커밋 메시지에 평문 키 없음
- `dangerouslySetInnerHTML` 사용 0 — XSS 방어 (R-N-05)

`/cso` 점검 대상: vite/esbuild moderate만. 본 PR scope out (dev 도구). I-10에서 `/cso` 1회 실행 시 재검토.

## 4. 가독성 / 단순성

- 파일 평균 25줄 — 모두 placeholder 수준의 단일 책임
- React 18 함수형 컴포넌트 + hooks (useParams) — 클래스 컴포넌트 0
- `tsconfig.json` strict + noUnusedLocals + noUnusedParameters — TS 컴파일이 dead code 차단
- 주석 minimal — 각 페이지 첫 line `// S-NN 화면명` + 후속 이슈 진입 시점 명시 (I-08·I-09). 코드 자체 표현적
- 라우트는 App.tsx 단일 진입점 — 추후 nested layout 도입 시 그대로 확장 가능

## 5. 발견 사항 (3축 OX 분류)

ADR-0008 3축 OX:

| 발견 | in_scope | blocks_merge | same_area | 처리 |
|---|---|---|---|---|
| F1: npm audit 2 moderate (esbuild + vite < 8) | ⭕ in_scope | ❌ no | ⭕ same_area | INFO. dev 서버 한정 vuln, 운영 build에 미반영. I-10에서 vite 6+ upgrade 검토 가능 |
| F2: zustand 4 vs 5 (최신) | ⭕ / ❌ / ⭕ | INFO. zustand 4.5.5 stable. v5는 React 19 시점 release. React 18.3 + zustand 4 정합 |
| F3: TanStack Query 미도입 — fetch 쿼리 캐싱 N/A | ⭕ / ❌ / ⭕ | 의도. RealWorld 학습 컨텍스트에서 fetch 래퍼 직접 + zustand store로 충분. 향후 도입 ADR 검토 가능 |
| F4: Header에 로그인 상태 미반영 (placeholder) | ⭕ / ❌ / ⭕ | 의도. I-08에서 useAuthStore 구독해 [Sign in/Sign up] ↔ [Home/Editor/Profile/Logout] 분기 |
| F5: ApiError `body: unknown` 타입 | ⭕ / ❌ / ⭕ | 의도. backend RealWorldError 응답 형식(`{errors:{body:[...]}}`)은 I-08 LoginPage에서 narrow + 422 인라인 표시 |
| F6: 컴포넌트 라이브러리 미도입 — Button/Input 직접 구현 부담 | ⭕ / ❌ / ⭕ | 의도. 10-lld-screen-design §3.4 결정. Tailwind utility-first. I-08·I-09 진입 시 components/ 폴더에 추가 |

NEEDS-WORK 0건. blocks_merge=yes 0건.

## 6. NEEDS-WORK 항목

(없음) — 6 OX 모두 PASS. P10 ai-qa-report 진입 허용.
