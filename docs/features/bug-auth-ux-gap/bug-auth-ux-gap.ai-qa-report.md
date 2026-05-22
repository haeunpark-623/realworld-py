---
doc_type: feature-ai-qa
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-22
gate: feature
ui_changed: "false"
related:
  R-ID: [R-F-01, R-F-02, R-F-03]
  F-ID: [F-01, F-04]
  supersedes: null
---

# bug-auth-ux-gap — AI QA Report

> D-06 1단. follow-up bug fix PR.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-22 | woosung.ahn@bespinglobal.com | 초안 — 6축 PASS / ui_changed=false |

## 0. Verdict

**PASS** — AI 자동 6축 통과.

- [reviewer]: woosung.ahn@bespinglobal.com (AI)
- [review_at]: 2026-05-22
- [at]: 2026-05-22
- [ui_changed]: false
- [Flow Mode]: bug
- [Mode Decision Trace]: 규칙 1 — type:bug 라벨 + PRD §3 F-01 실패 path 보강 시그널

## 1. Test Plan 4블록

### Build

```bash
cd frontend && npm run build
```

결과: TS strict pass + **61 modules in 1.23s** + CSS 10.91KB(변경 0) + JS 190.07KB gzip 60.29KB. exit 0.

### Automated tests

```bash
cd backend && uv run pytest -v
```

결과: backend pytest **77 passed** 회귀 N/A (backend 미수정). frontend N/A (WBS DoD).

### Manual verification

PR body 미체크 (ADR-0046 §2.3):

- [ ] AC-01: 비로그인 + `/editor` URL 직접 진입 → 즉시 `/login` 리다이렉트 (D-21-1·D-21-2)
- [ ] AC-02: 비로그인 + `/editor/{slug}` 또는 `/profile/{username}` → 즉시 `/login` (D-21-2)
- [ ] AC-03: 4 폼 빈 필드 submit → 한글 메시지 "○○을 입력해 주세요" (D-21-3)
- [ ] AC-04: 로그인 후 DevTools Application > Local Storage > realworld.token 수정(임의 문자열) → 새 글 작성 시도 → 401 → 자동 logout + /login (D-21-4)
- [ ] AC-05: 로그인 상태에서 모든 라우트 정상 진입 (회귀 0)
- [ ] AC-06: 정상 입력 폼 submit → POST/PUT 정상 (회귀 0)
- [ ] GitHub Actions: backend-ci `paths: backend/**` 한정 → frontend N/A. pr-body-checkboxes status check 정상

### DoD coverage

D-21-1~6 (6건):
- [ ] D-21-1 RequireAuth.tsx 신규
- [ ] D-21-2 App.tsx 3 라우트 wrap
- [ ] D-21-3 4 폼 onInvalid + CommentItem 인라인
- [ ] D-21-4 api/client.ts 401 분기
- [ ] D-21-5 backend pytest 77 passed
- [ ] D-21-6 frontend npm run build TS strict

## 2. AI 게이트 6축

| # | 축 | 결과 | 근거 |
| --- | --- | --- | --- |
| 1 | 자동 테스트 통과 | ✅ N/A | backend 77 passed 무영향, frontend WBS DoD N/A |
| 2 | AI 코드 리뷰 PASS | ✅ PASS | code-review §0 PASS |
| 3 | Test Plan 4블록 첨부 | ✅ PASS | §1 |
| 4 | 시크릿·보안 스캔 | ✅ PASS | 신규 env 0, 한글 string 상수만, XSS·CSRF 0 |
| 5 | 브라우저 골든패스 + stylesheet | ✅ N/A | docs only stylesheet 변경 0 (10.91KB 유지). 시각 디자인 동일 |
| 6 | 로컬 부팅 가능성 | ✅ PASS | dev: build 1.23s + dev 부팅. stg/prod: N/A |

추가 축 (ADR-0047): backend-ci `paths: backend/**` 한정 → frontend N/A 사유.

## 3. 시나리오 인용

| 시나리오 | 출처 | 결과 |
| --- | --- | --- |
| AC-01 비로그인 /editor 차단 | acceptance §1 | ⏸ Manual |
| AC-02 /editor/:slug + /profile/:username 차단 | acceptance §1 | ⏸ Manual |
| AC-03 빈 폼 한글 에러 | acceptance §1 | ⏸ Manual |
| AC-04 JWT 만료 자동 logout | acceptance §1 | ⏸ Manual |
| AC-05 로그인 회귀 | acceptance §1 | ⏸ Manual |
| AC-06 정상 submit 회귀 | acceptance §1 | ⏸ Manual |
| backend 77 passed | acceptance §4 | ✅ |

## 4. FAIL 항목

(없음)

## 5. 발견 사항

- **양호**: PRD §3 F-01 실패-3 + F-02 실패-2 + F-04 §5 한글 메시지 3건 acceptance gap closure 1 PR에 묶음
- **양호**: I-08 simple catch 패턴 결정 회귀를 contract §1 + plan §5 + retro 2026-05-21에 양축 trace — 학습 가치 보존
- **양호**: 3 commit DAG (api 401 → RequireAuth → onInvalid) + ADR-0021 통과
- **양호**: build CSS 10.91KB 변경 0 (한글 메시지는 string 변경) — 정량적으로 시각 디자인 무변경 입증

## 6. UI/FE 변경 검증

**ui_changed=false** — 시각 디자인 변경 0. 기능 동작 보강(인터셉터·가드·메시지)만.

- [gstack_qa_used]: gstack /qa N/A 사전 합의 (시각 변경 0)
- [console_errors]: N/A 사전 합의 (브라우저 미사용)
- [stylesheet 적용 근거]: ✅ Tailwind 4 양축 그대로 + CSS **10.91KB 변경 0** 정량 증거 (I-09 정착 토큰 그대로)

| 화면 | 시나리오 | 스크린샷경로 | stylesheet 적용 |
| --- | --- | --- | --- |
| N/A | N/A — 시각 디자인 변경 0 | N/A | N/A |

## 7. 로컬 부팅 가능성

| 프로파일 | 부팅 명령 | 결과 (ready 신호) | 에러 | 부팅 자산 변경 |
| --- | --- | --- | --- | --- |
| dev | `cd frontend && npm run build && npm run dev` | ✅ build 1.23s + Vite ready @ 5173 | 0건 | 부팅 자산 변경 0 |
| stg | N/A — 단일 환경 운영 | N/A | N/A | N/A |
| prod | N/A — 단일 환경 운영 | N/A | N/A | N/A |

[LOCAL.md 동기]: ✅ N/A 부팅 자산 변경 0
