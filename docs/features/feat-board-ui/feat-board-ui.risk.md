---
doc_type: feature-risk
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-04, R-F-05, R-F-06, R-F-07, R-F-08, R-F-09, R-F-10, R-F-11, R-F-12, R-F-13, R-N-02, R-N-05]
  F-ID: [F-02, F-03, F-04]
  supersedes: null
---

# feat-board-ui — Feature Risk

> P7. 본 PR 한정 F-RISK 4건.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — F-RISK 4건 (시간 박스·gstack 가용성 Mid, 나머지 Low) |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| F-RISK-01 | 시간 박스 초과 — effort 2d ≈ 2.5-3.5h가 4h+ 늘어 I-10 종료 시간 박스 위협 | 4 | 3 | **Mid** |
| F-RISK-02 | gstack `/qa` 골든패스 실행 환경 미동작 (RISK-06) | 3 | 2 | Low |
| F-RISK-03 | Promise.all 부분 실패 시 ArticlePage error state 모호 | 2 | 2 | Low |
| F-RISK-04 | Modal focus trap 간소화 — a11y WCAG 부분 미달 | 1 | 3 | Low |

## 2. 리스크 상세

### F-RISK-01 — 시간 박스 초과 (Mid)

- **시나리오**: 6 commit DAG가 4h 이상 소요 → I-10 (회귀·PR 머지 0.5d, ~30-45분) 압박 → Sprint 2 18:00 마감 미달
- **완화**: 14-wbs §6.1 시점별 컷 결정 — 14:00 ProfilePage / 16:00 댓글 수정 UI / 17:00 골든패스 7→5 압축. AI 페어 가속(§0.1)으로 effort 2d가 ~2.5h로 환산 가능
- **단계적 롤아웃**: 본 PR 자체는 일괄 PR 머지. 컷은 commit 단위 skip + commit 메시지 표기

### F-RISK-02 — gstack /qa 가용성 (Low)

- **시나리오**: gstack `/qa` 도구 미사용 또는 환경 오류 시 골든패스 자동화 불가 → 수동 7단계 + 스크린샷 사람 첨부로 대체
- **완화**: WBS RISK-06 (gstack 가용성) + Sprint 1 종료 시점 dry-run 사전 점검 명시. 수동 fallback도 정합

### F-RISK-03 — Promise.all 부분 실패

- **시나리오**: ArticlePage `Promise.all([article, comments])` 중 comments만 실패 시 article 표시 + comments 비어있음. 사용자가 "댓글 없음"인지 "에러"인지 구분 못함
- **완화**: plan §5 (6) — article 404면 ArticlePage 404 메시지. comments 실패는 빈 배열 fallback + console.error 로깅 (사용자에게는 빈 댓글로 보임). 학습 컨텍스트 acceptable

### F-RISK-04 — Modal focus trap

- **시나리오**: Modal 열린 상태에서 Tab 키로 모달 밖 요소에 focus 이동 → 키보드 사용자 confusion
- **완화**: 10-lld §4 a11y "기본 시맨틱·라벨 수준만 강제, 풀 WCAG는 Out of Scope" 결정. ESC + 오버레이 클릭 닫기는 구현 → 키보드 사용자 escape 경로 보장

## 3. High 등급 단계적 롤아웃

(없음 — Mid 1건은 단계 컷 plan §5 §1 결정으로 흡수).

## 4. 데이터 영속성 변경

- localStorage: I-08 정착 키 무수정
- backend DB: 무영향
- 스크린샷 산출: `docs/features/feat-board-ui/screenshots/` 7장 + FCP/XSS 측정 결과 메모 — git tracked

## 5. 15-risk.md 갱신 항목

- RISK-01 (일정) 부분 발현 가능성 — Day 2 시점별 컷 결정으로 완화 (14-wbs §6.1)
- RISK-04 (F-04 회귀 안전망) 본 PR 골든패스로 첫 검증
- RISK-06 (gstack 가용성) — Sprint 1 dry-run 결과에 따라 fallback 결정
