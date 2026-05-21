---
doc_type: feature-risk
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-01, R-F-02, R-F-03]
  F-ID: [F-01, F-04]
  supersedes: null
---

# feat-auth-ui — Feature Risk

> P7. 본 PR 한정 F-RISK 4건. 모두 Low.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 4 F-RISK 모두 Low |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| F-RISK-01 | Vite proxy 미동작 — frontend → backend `/api/*` 요청 실패 | 3 | 2 | Low |
| F-RISK-02 | localStorage 토큰 평문 저장 — XSS 시 탈취 | 2 | 1 | Low |
| F-RISK-03 | 422 errors body 형식 비표준 응답 시 `extractErrorMessage` 무방어 | 2 | 1 | Low |
| F-RISK-04 | App.tsx loadFromStorage 무한 루프 (useEffect deps 빠뜨림) | 3 | 1 | Low |

## 2. 리스크 상세

### F-RISK-01 — Vite proxy 미동작

- **시나리오**: `vite.config.ts` proxy 설정에도 backend 미부팅 또는 CORS 설정 누락 시 fetch 실패. LoginPage `/api/users/login` 호출이 4xx/5xx 응답 → UX 차단
- **완화**: contract §3 Call Sites — backend CORS_ORIGINS 기본값에 5173 포함(I-01 정착) 재확인. AC-01·03 Manual verification에서 사람이 backend·frontend 동시 부팅 확인
- **트리거 시점**: P8 통합 검증 — 사람이 골든패스 시도 시 즉시 발견

### F-RISK-02 — localStorage 토큰 평문

- **시나리오**: XSS 공격 시 `localStorage.getItem('realworld.token')` 탈취. JWT 7일 유효 — 탈취되면 7일간 임의 동작 가능
- **완화**: React JSX 기본 escape + `dangerouslySetInnerHTML` 0 + backend Pydantic 입력 검증. RealWorld spec 동일 패턴이라 학습 컨텍스트 acceptable. HttpOnly cookie 채택은 backend 변경 대형 → 후속 학습 과제
- **트리거 시점**: 운영 단계 — 본 학습 MVP는 N/A. 15-risk RISK-02 보안 카테고리 인지만

### F-RISK-03 — 422 errors body 비표준

- **시나리오**: backend가 `{errors:{body:[...]}}` 형식 외 응답 시 `extractErrorMessage` 가 빈 문자열 반환 → UX에서 "에러 발생" 같은 fallback 표시 없으면 사용자 혼동
- **완화**: `extractErrorMessage` fallback "알 수 없는 오류가 발생했습니다" 명시. backend 라우트 5종 모두 RealWorldError handler 통일(Issue #4 정착)이라 가능성 낮음
- **트리거 시점**: P8 implement — extractErrorMessage 작성 시 fallback 검증

### F-RISK-04 — loadFromStorage 무한 루프

- **시나리오**: `useEffect(() => loadFromStorage(), [])` 에서 deps 빈 배열 누락 시 매 render마다 호출 → zustand state 변경 → re-render → 무한 루프
- **완화**: deps 빈 배열 `[]` 명시 + `useAuthStore.getState()` 사용으로 hook 구독 회피 (getState는 정적 호출). React strict mode dev 환경에서 2번 호출되지만 무한 루프는 아님
- **트리거 시점**: P8 C4 implement — 빌드 실패 또는 브라우저 hang으로 즉시 발견

## 3. High 등급 단계적 롤아웃

(없음) — 4 F-RISK 모두 Low.

## 4. 데이터 영속성 변경

- **localStorage 키**: `realworld.token` + `realworld.user` (I-07 정의 + I-08 첫 실 사용)
- **데이터 손실 가능성**: 0 (revert 시 localStorage 잔존하지만 만료 또는 사용자 수동 clear로 자연 해소)
- **backend DB 영향**: 0

## 5. 15-risk.md 갱신 항목

(없음) — 기존 RISK-02(보안)에 F-RISK-02 부합하지만 학습 컨텍스트 acceptable 결정. RISK-04(F-04 회귀 안전망)는 I-09 골든패스에서 첫 실 검증.
