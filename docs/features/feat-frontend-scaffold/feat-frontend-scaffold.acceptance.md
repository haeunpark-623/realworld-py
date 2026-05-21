---
doc_type: feature-acceptance
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

# feat-frontend-scaffold — Acceptance Criteria

> P6. WBS Issue #7 DoD Checklist 10건 매핑 + Given/When/Then 3건.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 3 AC + 10 DoD (D-07-1~10) + 수동 검증 시나리오 |

## 1. 인수 기준 (Given/When/Then)

| ID | Given | When | Then | 출처 |
| --- | --- | --- | --- | --- |
| AC-01 | fresh checkout 상태 + Node 22+ 설치 | `(cd frontend && npm install)` 실행 | 0 vuln 또는 known low 만 (npm audit) + `node_modules/` 생성 + `package-lock.json` commit 가능 | WBS I-07 AC |
| AC-02 | frontend 워크스페이스 셋업 완료 | `(cd frontend && npm run dev)` 실행 | Vite dev 서버가 5173 포트에 부팅 + 브라우저 `http://localhost:5173/`·`/article/foo`·`/editor`·`/login`·`/register`·`/profile/foo` 6 라우트 placeholder 진입 가능 + 각 페이지 Tailwind 클래스 1개 이상 시각적 적용 | WBS I-07 AC |
| AC-03 | frontend dev 서버 + backend dev 서버(:8000) 동시 부팅 | 브라우저 콘솔에서 `fetch('/api/health')` 호출 | Vite proxy 동작 → backend 응답 `{status: ok}` 200 (proxy 검증) | contract §3 |

## 2. Definition of Done (D-06)

WBS I-07 DoD Checklist 10건 매핑 — D-07-N 명명 (PR body 미체크, ADR-0046 §2.3):

- [ ] D-07-1 `pnpm create vite frontend --template react-ts` 또는 **수동 구성** (npm 채택 점진 합의)
- [ ] D-07-2 `package-lock.json` commit (npm install 결과, pnpm-lock.yaml 대체)
- [ ] D-07-3 `tailwind.config.js` + `postcss.config.js` + `src/index.css` 3 directive (@tailwind base/components/utilities)
- [ ] D-07-4 `src/main.tsx`에서 `import './index.css'`
- [ ] D-07-5 `src/App.tsx`에 react-router-dom 라우트 6개 placeholder
- [ ] D-07-6 `src/components/Header.tsx` (로고 + 메뉴, 로그인 상태 미적용 placeholder)
- [ ] D-07-7 `src/api/client.ts` fetch 래퍼 (Authorization 헤더 첨부 placeholder)
- [ ] D-07-8 `src/store/auth.ts` zustand store placeholder
- [ ] D-07-9 `vite.config.ts` proxy 설정 `/api → http://localhost:8000`
- [ ] D-07-10 `frontend/.env.example` (`VITE_API_BASE_URL=/api`) + frontend 5173 + backend 8000 동시 부팅 후 브라우저에서 6 라우트 진입 가능 확인

## 3. 비기능 인수

- **R-N-02 (FCP)**: 본 PR은 placeholder만이라 FCP 정량 측정 N/A. I-09 골든패스에서 gstack Performance 트레이스로 첫 측정 (FCP < 1.5s 임계)
- **R-N-04 (시크릿)**: `frontend/.env.example`만 commit. `frontend/.env`는 `.gitignore`에 포함 — 시크릿 노출 0
- **R-N-05 (XSS/SQLi)**: 본 PR placeholder는 dangerouslySetInnerHTML 미사용. React 기본 JSX escape 활용
- **R-N-06 (부팅 자산)**: package-lock.json + .env.example + LOCAL.md §3·§4 동기 갱신 — fresh checkout 5분 부팅 보장

## 4. 회귀 인수

- backend pytest **77 passed** 무영향 (frontend 변경, backend 미수정)
- backend dev 서버 부팅: 무영향 — `uv run uvicorn realworld.main:app` 그대로
- backend-ci.yml: 무영향 — `paths: backend/**` 한정 트리거
- LOCAL.md §3 기존 dev 부팅 명령(backend): 무수정. frontend 명령은 *추가*만
- alembic 마이그레이션: 무영향 — 0004 (head) 정합
