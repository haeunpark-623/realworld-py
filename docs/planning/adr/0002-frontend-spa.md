---
doc_type: adr
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: [R-N-02, R-N-05]
  F-ID: [F-04]
  supersedes: null
---

# ADR 0002 — 프론트엔드 React SPA + Vite 채택

- **상태**: Draft
- **결정일**: 2026-05-20
- **작성**: 박하은 <woosung.ahn@bespinglobal.com>

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — 게이트 B(v0.2) 사용자 결정, 게이트 C ADR 정식화 |

## 1. 컨텍스트

본 프로젝트는 F-04 UI를 브라우저에서 동작시켜야 한다. 후보 2종:

- **A**: 서버 렌더링 (Jinja2 + HTMX) — Django/Flask와 자연 결합
- **B**: SPA (React/Vue + REST API) — FastAPI REST와 자연 결합

게이트 B(v0.2)에서 사용자는 ADR-0001(FastAPI) 채택과 함께 SPA를 사전 결정. 본 ADR은 그 결정을 정식화 + 세부(React + Vite + TypeScript)를 확정한다. 컨텍스트:

- ADR-0001 — FastAPI 채택 (REST API)
- 05-prd F-04 UI — 6개 화면(홈·상세·글쓰기·로그인·회원가입·프로필)
- NFR-02 FCP < 1.5s — 번들 크기 관리 필요
- ADR-0038 — 스타일링 솔루션 채택 강제 (별도 ADR-0004로 분리)
- F-04 UI 단위/통합 테스트 N/A 결정 (v0.2)

## 2. 결정

**React 19 + Vite 5 + TypeScript 5.x (SPA)** 채택.

채택 효과:
- `frontend/` 워크스페이스를 Vite + React 템플릿으로 부트스트랩
- TypeScript strict 모드 (`tsconfig.strict=true`) 적용
- 라우팅은 `react-router-dom` v6
- 상태 관리는 `zustand` (auth store만 — devtoolkit.config.yaml 기본값 유지)
- API 호출은 fetch 래퍼(`api/client.ts`) — axios 미도입
- pnpm 패키지 매니저
- 컴포넌트 라이브러리 0건 (utility-first CSS만, ADR-0004 Tailwind 참조)

## 3. 검토된 대안

### 채택안: React + Vite + TypeScript

- **장점**:
  - 가장 풍부한 학습 자료·커뮤니티 (Vue/Svelte 대비)
  - Vite의 빠른 dev 서버 + HMR — 학습 피드백 사이클 짧음
  - TypeScript strict 모드로 09-api-spec 응답 타입을 직접 매핑 가능 → 컴파일 타임 검증
  - JSX 기본 escape로 R-N-05 XSS 방어 자동
  - React 19의 자동 batching·use Suspense 등 신기능 학습 가치
- **단점**:
  - 학습 곡선이 Vue/Svelte보다 약간 가파름
  - React 19는 비교적 최신이라 일부 패턴 자료 부족 가능 (다만 React 18 자료와 호환)

### 대안 1: Vue 3 + Vite + TypeScript

- **장점**:
  - 학습 곡선이 React보다 부드러움
  - SFC(Single File Component) 구조 직관적
  - 본 학습 컨텍스트와 잘 맞음
- **단점 (불채택 이유)**:
  - 한국 사내 신규 입사자가 *기본기로 익혀야 할 것*은 통상 React가 우위 — 학습 효과 우선
  - 본 회사 사내 컨벤션 가정 시 React가 더 자주 마주칠 stack
  - Vue 3 Composition API 학습 부담은 React Hooks와 유사 — 결정 차별점 약함

### 대안 2: Svelte + SvelteKit

- **장점**:
  - 가장 가벼움 — 번들 크기 최소
  - 학습 곡선 가장 부드러움
- **단점 (불채택 이유)**:
  - 한국 사내 활용도 낮음 — 학습 효과 약함
  - SvelteKit은 SSR 통합이라 본 학습 목표(SPA + REST 분리)와 어긋남

### 대안 3: 서버 렌더링 (Jinja2 + HTMX + FastAPI)

- **장점**:
  - 단일 stack — 학습 단순성 최대
  - JS 의존 0
  - 부팅 자산 최소
- **단점 (불채택 이유)**:
  - 사내 학습 컨텍스트가 *모던 풀스택* — SPA·REST 분리 학습이 본 과제 핵심
  - FastAPI + Jinja2 결합은 가능하지만 RealWorld spec 레퍼런스가 SPA가 다수
  - HTMX는 학습 효과는 있으나 *현재 사내 표준* 스택 아님

## 4. 결과 (Consequences)

### 긍정

- TypeScript 타입으로 09-api-spec 응답을 컴파일 타임 검증
- Vite HMR로 dev 사이클 빠름 (코드 변경 → 1초 이내 브라우저 반영)
- JSX 자동 escape로 XSS 방어 무료
- React Hooks 학습 효과 — 사내 표준 stack 익숙도 향상
- pnpm 워크스페이스 + Vite로 monorepo 운영 자연스러움

### 부정 / 트레이드오프

- 단일 stack 대비 부팅 자산 2배 (`frontend/`, `backend/` 분리)
- CORS 설정 필요 (or Vite proxy)
- JWT 보관 위치(localStorage) 보안 트레이드오프 — XSS 시 토큰 탈취 가능. 학습 컨텍스트에서 허용
- F-04 UI 단위/통합 테스트 N/A 결정 — 회귀 안전망이 골든패스 E2E 1회뿐

### 영향 받는 문서

- 06-architecture §1·§2.1 (Frontend SPA 컨테이너 명시)
- 07-hld §1 M-FE-* 4개 모듈
- 10-lld-screen-design 전체 (SPA + Tailwind 가정)
- 11-coding-conventions §1·§3.2 (TS 명명·관용구)
- 12-scaffolding/python.md §1·§4·§5·§8 (frontend/ 트리·스타일링)
- ADR-0004 (Tailwind) — 본 ADR 결정에 의존
- 13-test-design 02-catalog F-04 (E2E gstack 1회 결정)
- LOCAL.md §1·§2·§3.1 (pnpm·Vite 명령)

## 5. 추적 / 재검토 시점

- **재검토 트리거**: NFR-02 FCP < 1.5s 미달 시 코드 스플리팅 도입(별 결정), 또는 후속 학습 과제에서 Next.js(SSR) 등으로 재도전.
- **GitHub Issue 라벨**: `decision:reverse` (변경 시).
- **재검토 주기**: 본 학습 과제 1회성.
