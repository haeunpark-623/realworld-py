---
doc_type: feature-risk
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

# feat-frontend-scaffold — Feature Risk

> P7. 본 PR 한정 F-RISK 4건. 모두 Low. mode=add 신규 워크스페이스라 blast radius minimal.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — F-RISK 4건 모두 Low. High 0건 |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| F-RISK-01 | npm 채택으로 WBS I-07 AC `pnpm install --frozen-lockfile` 불일치 — fresh checkout 시 명령 혼선 | 2 | 2 | Low |
| F-RISK-02 | Vite dev proxy 동작 미검증 — I-08에서 401·CORS 에러 발현 | 2 | 1 | Low |
| F-RISK-03 | Tailwind 3 directive 미적용 — 페이지 placeholder 시각 무반응 | 2 | 1 | Low |
| F-RISK-04 | Node 버전 핀 부재 — 다른 Node 18·20·22 환경에서 빌드 실패 | 1 | 2 | Low |

## 2. 리스크 상세

### F-RISK-01 — npm vs pnpm 명령 불일치

- **시나리오**: WBS I-07 Acceptance Criteria는 `pnpm install --frozen-lockfile` 명시. 실제 사용은 `npm install` (또는 `npm ci`). fresh checkout 시 사용자가 pnpm을 시도하면 lockfile 미일치 에러
- **완화**: LOCAL.md §3 + 12-scaffolding §5 + 14-wbs 변경 이력(v0.10)에서 npm 채택을 명시. README.md에서도 명령 통일 (I-10에서 작성)
- **트리거 시점**: P10 ai-qa-report 부팅 검증 시 즉시 발견

### F-RISK-02 — Vite proxy 동작 미검증

- **시나리오**: `server.proxy['/api'] = 'http://localhost:8000'` 설정만 두고 본 PR에서 실제 `/api/*` 호출 미검증. I-08 LoginPage에서 첫 호출 시 proxy 미동작·CORS 위반 발현 가능
- **완화**: P10 Manual verification에 `fetch('/api/health')` 또는 backend Swagger 직접 호출 1회 추가. backend CORS 기본 origin에 5173 포함 (I-01 정착) 재확인
- **트리거 시점**: Manual verification 단계 (사람 책임)

### F-RISK-03 — Tailwind 미적용 placeholder

- **시나리오**: `index.css` 3 directive 누락 또는 `main.tsx` import 누락 시 페이지 placeholder 텍스트만 보이고 Tailwind 클래스 무반응. ADR-0038 5번째 축 stylesheet 적용 근거 미충족 → AI 게이트 BLOCK 가능
- **완화**: ai-qa-report.md §6에 [stylesheet 적용 근거] 명시 + Manual verification에 "Tailwind 클래스 시각적 적용 확인" 체크박스. tailwind.config.js content 경로 정확성 + postcss.config.js + index.css 3 directive 모두 검증
- **트리거 시점**: P8 implement 부팅 검증

### F-RISK-04 — Node 버전 핀 부재

- **시나리오**: `package.json` engines.node 명시 안 함. 다른 사용자가 Node 16 등으로 npm install 시도 시 vite 5 호환 에러 발생 가능
- **완화**: LOCAL.md §1 사전 요구사항에 "Node 22 LTS" 명시. 학습 컨텍스트 1인 작업이라 환경 충돌 가능성 낮음. README.md(I-10)에서 재명시
- **트리거 시점**: 다른 환경 fresh checkout 시 (본 사이클에서는 N/A)

## 3. High 등급 단계적 롤아웃

(없음) — 4 F-RISK 모두 Low. 단계적 롤아웃 plan 강제 N/A.

## 4. 데이터 영속성 변경

- **신규 테이블/마이그레이션**: 0
- **localStorage 사용**: 본 PR 0 — store/auth.ts는 placeholder. I-08에서 첫 localStorage 사용 (`token` key)
- **데이터 손실 가능성**: 0

## 5. 15-risk.md 갱신 항목

(없음) — 기존 8 RISK-ID에 본 변경 영향 없음. RISK-04(F-04 회귀 안전망)는 본 PR이 frontend 워크스페이스 자체를 처음 도입하는 단계이므로 회귀 N/A. 15-risk.md v0.1 무수정 유지.
