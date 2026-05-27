---
doc_type: feature-risk
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-27
gate: feature
related:
  R-ID: []
  F-ID: []
  supersedes: null
---

# bug-ci-lint-title — Feature Risk

> P7. 2 F-RISK 모두 Low.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-27 | woosung.ahn@bespinglobal.com | 초안 |

## 1. 본 변경의 리스크

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 |
| --- | --- | --- | --- | --- |
| F-RISK-01 | `GH_REPO` env 미적용 케이스 — gh CLI 일부 버전이 인식 안 함 | 2 | 1 | Low |
| F-RISK-02 | 본 PR 제목 자체 ADR-0021 정합 — 만약 정합 안 되면 자기 자신 BLOCK | 3 | 1 | Low |

## 2. 리스크 상세

### F-RISK-01 — gh CLI 버전 호환

- **시나리오**: GitHub Actions runner의 gh CLI가 GH_REPO env를 인식 못함 → 동일 에러 재발
- **완화**: gh CLI 2.x+ 공식 지원 — runner는 최신 유지. 만약 발현 시 follow-up으로 actions/checkout 대체 가능
- **트리거 시점**: AC-02 Manual 재현 시 즉시 발견

### F-RISK-02 — 자기 자신 BLOCK

- **시나리오**: 본 PR 제목 `fix(ci): ...`이 regex 통과 안 함 (예: ci가 type:area 매칭 안 됨)
- **완화**: regex 분석 — `^(feat|fix|chore|docs|test|refactor)\([a-z][a-z0-9,_-]*\): .+$`. `ci`는 area 부분이라 `[a-z][a-z0-9,_-]*`에 매칭 — 통과 확실

## 3. High 등급 단계적 롤아웃

(없음 — 모두 Low)

## 4. 데이터 영속성 변경

- 0 — workflow YAML 1줄

## 5. 15-risk.md 갱신 항목

(없음) — workflow infra UX 개선
