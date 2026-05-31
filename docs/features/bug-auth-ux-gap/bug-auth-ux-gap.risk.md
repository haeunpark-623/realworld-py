---
doc_type: feature-risk
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-22
gate: feature
related:
  R-ID: [R-F-01, R-F-02, R-F-03]
  F-ID: [F-01, F-04]
  supersedes: null
---

# bug-auth-ux-gap — Feature Risk

> P7. 3 F-RISK 모두 Low.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-22 | woosung.ahn@bespinglobal.com | 초안 — 3 F-RISK 모두 Low |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| F-RISK-01 | RequireAuth가 token 로드 race condition으로 첫 진입 시 false negative | 3 | 2 | Low |
| F-RISK-02 | `window.location.assign` 전체 새로고침 — 다른 비동기 작업 중단 | 2 | 2 | Low |
| F-RISK-03 | onInvalid 핸들러가 모든 invalid 케이스 cover 못함 (특수 문자 등) | 1 | 2 | Low |

## 2. 리스크 상세

### F-RISK-01 — RequireAuth race condition

- **시나리오**: App.tsx mount useEffect loadFromStorage가 비동기? — 실제로는 동기 (zustand set은 동기). 그러나 React strict mode dev에서 첫 render 시 store가 아직 빈 상태일 가능성. 새로고침 직후 token 있는 사용자가 `/editor` 진입 시 false negative로 `/login` 잠시 보일 수 있음
- **완화**: loadFromStorage는 main.tsx에서 createRoot 호출 *전*에 동기 실행 가능. 또는 App.tsx 첫 render 전에 store init. 현재 패턴(App mount useEffect)으로도 zustand set이 동기라 첫 render 후 즉시 반영 — 사용자 인지 가능성 거의 0
- **트리거 시점**: P8 implement 부팅 확인 + Manual verification

### F-RISK-02 — 전체 새로고침 부수 효과

- **시나리오**: 401 시 `window.location.assign("/login")`은 전체 페이지 리로드. EditorPage에서 입력 중인 폼 데이터 손실
- **완화**: 401 발생 시점이 *세션 만료*라 폼 데이터 손실은 자연스러운 trade-off. drafts 자동 저장은 out of scope. 사용자에게 "세션 만료" 토스트 표시는 후속 학습

### F-RISK-03 — onInvalid cover 부족

- **시나리오**: 특수 문자 입력 시 (e.g. email type에 `@@@`) HTML5 validation이 invalid 판정 → setCustomValidity 호출되지만 한글 메시지 길이가 short — 디테일 누락
- **완화**: 기본 3 invalid 케이스(빈 값 / minLength 미달 / email format)만 cover. 그 외는 HTML5 default 영문이라도 비기능 영향 최소

## 3. High 등급 단계적 롤아웃

(없음) — 3건 모두 Low.

## 4. 데이터 영속성 변경

- localStorage: 401 시 `realworld.token` + `realworld.user` 자동 삭제 (logout 호출)
- backend DB: 영향 0

## 5. 15-risk.md 갱신 항목

- RISK-04 (F-04 회귀 안전망): 본 PR이 PRD acceptance gap closure — 회귀 안전망 강화