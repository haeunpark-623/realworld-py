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

# ADR 0004 — 스타일링 솔루션 Tailwind CSS 채택

- **상태**: Draft
- **결정일**: 2026-05-20
- **작성**: 박하은 <woosung.ahn@bespinglobal.com>

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 — 게이트 C에서 ADR-0038(스타일링 솔루션 강제) 충족 |

## 1. 컨텍스트

ADR-0038은 frontend layer가 있는 모든 newProject에 스타일링 솔루션 1개 채택을 강제한다. 후보는 schema에서 Tailwind / CSS Modules / styled-components / emotion / vanilla-extract / Sass 6종. 본 프로젝트는 ADR-0002(React + Vite SPA)와 짝을 이루는 결정.

컨텍스트:
- 10-lld-screen-design §3 디자인 토큰 4종(Color·Typography·Spacing·Component primitives)이 schema BLOCK
- 시간 부담 — 6 화면 + 컴포넌트 primitives 7종을 2일 안에
- F-04 UI 단위/통합 N/A 결정 (v0.2) — 스타일링 안정성은 골든패스 E2E 1회로 검증
- 컴포넌트 라이브러리(MUI/AntD) 미도입 결정(10-lld-screen-design §3.4)

## 2. 결정

**Tailwind CSS 3.x** 채택.

채택 효과:
- `frontend/package.json devDependencies`: `tailwindcss@^3.4`, `postcss@^8`, `autoprefixer@^10`
- `frontend/tailwind.config.js` 기본 설정 (custom theme 최소)
- `frontend/src/index.css`에 `@tailwind base; @tailwind components; @tailwind utilities;` 3 directive
- `frontend/src/main.tsx`에서 `import './index.css';` (entrypoint 적용)
- 10-lld-screen-design §3.1~§3.4 토큰을 Tailwind 표준 클래스로 매핑 (별도 custom theme 거의 없음)

## 3. 검토된 대안

### 채택안: Tailwind CSS 3.x

- **장점**:
  - Vite 공식 plugin 1개로 통합 — 학습 부담 최소
  - utility-first가 10-lld-screen-design §3 디자인 토큰을 *직접* 매핑 — 별도 디자인 토큰 시스템 불필요
  - 학습 곡선 완만 — 자주 쓰는 클래스 100개 이내 익히면 충분
  - 의존성 1개 (`tailwindcss` 단일 패키지가 PostCSS·autoprefixer 통합 호환)
  - 컴포넌트 primitives(Button·Input·Card)를 JSX + utility 조합으로 작성 → 컴포넌트 라이브러리 의존 0
  - 본 학습 컨텍스트와 일치 (사내 표준에 가까움)
- **단점**:
  - 클래스 이름이 길어 JSX가 다소 어지러움 — 학습 컨텍스트에서 허용
  - dynamic class name(런타임 결정 색상 등)에 약간의 제약 — 본 MVP는 정적 색상만이라 부담 없음

### 대안 1: CSS Modules (Vite 기본 지원)

- **장점**:
  - Vite 내장 지원 — 의존성 추가 0
  - 컴포넌트별 격리 — 클래스 충돌 없음
  - 표준 CSS 그대로 학습
- **단점 (불채택 이유)**:
  - 디자인 토큰을 CSS 변수로 별도 정의 + 모든 컴포넌트에서 import → 산출 부담 증가
  - 클래스 명명 추가 학습 (`.button--primary` 등 BEM 류) — 학습 부담
  - utility-first 패러다임 학습 효과 누락

### 대안 2: styled-components (CSS-in-JS)

- **장점**:
  - React와 강결합 — 컴포넌트 단위 스타일링 직관
  - 동적 props 기반 스타일링 자연
- **단점 (불채택 이유)**:
  - 런타임 비용 — NFR-02 FCP < 1.5s 미달 위험
  - SSR 통합 부담 (본 SPA에서는 무관)
  - 학습 부담 — Tailwind보다 가파른 곡선
  - 사내 표준에서 멀어짐

### 대안 3: vanilla-extract

- 본 학습 컨텍스트에 비해 도구 복잡도 과대. 불채택.

### 대안 4: Sass / Less

- 모던 React 컨텍스트에서 사용 빈도 감소. 본 학습 가치 약함. 불채택.

## 4. 결과 (Consequences)

### 긍정

- 디자인 토큰을 Tailwind 표준 클래스로 직접 사용 — 별도 토큰 시스템 불필요
- 의존성 1건 추가 (`tailwindcss`)로 모든 스타일링 해결
- JSX inline utility 작성으로 컴포넌트 작성 속도 빠름
- 학습 곡선 완만 — 2일 마감 컨텍스트 적합

### 부정 / 트레이드오프

- JSX 클래스 이름이 길어짐 — 학습 컨텍스트에서 허용. 필요 시 `clsx`로 조합 가능
- Tailwind 외 stylesheet 일관성 깨질 위험 — 본 프로젝트는 *Tailwind만* 사용 (별도 .css 0개) 원칙
- 디자인 토큰을 *Tailwind 표준에 종속* — 향후 디자인 시스템 변경 시 토큰 전체 재매핑 부담 (학습 컨텍스트에서 무시)

### 영향 받는 문서

- 10-lld-screen-design §3 디자인 토큰 (Tailwind 클래스로 매핑된 표 명시)
- 12-scaffolding/python.md §8 스타일링 솔루션 (Tailwind 결정 명시)
- ADR-0002 (React SPA) — 본 ADR이 동반 결정

## 5. 추적 / 재검토 시점

- **재검토 트리거**: 디자인 시스템이 정식 도입될 때 (디자인 토큰 별 시스템 필요), 또는 컴포넌트 라이브러리(MUI/AntD) 도입 시.
- **재검토 주기**: 본 학습 과제 1회성.
