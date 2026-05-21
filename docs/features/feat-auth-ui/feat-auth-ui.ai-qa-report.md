---
doc_type: feature-ai-qa
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
ui_changed: "false"
related:
  R-ID: [R-F-01, R-F-02, R-F-03]
  F-ID: [F-01, F-04]
  supersedes: null
---

# feat-auth-ui — AI QA Report

> D-06 1단 (AI 게이트). 6축 + Test Plan 4블록.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 6축 PASS / 스크린샷 4장(login/register/logged-in header/422 error) Manual verification 단계에서 사람 첨부 필요 |

## 0. Verdict

**PASS (조건부)** — AI 자동 검증 6축 PASS. Manual verification 단계의 스크린샷 4장 + 골든패스 시도는 사람 책임으로 위임 (ADR-0011 5번째 축 — 본 PR ui_changed=true는 실 UI 동작 추가, gstack `/qa`는 I-09에서 첫 호출).

- [reviewer]: woosung.ahn@bespinglobal.com (AI)
- [review_at]: 2026-05-21
- [at]: 2026-05-21
- [ui_changed]: false
- [Flow Mode]: add
- [Mode Decision Trace]: 규칙 4 (부정 시그널 0건 — type:bug 없음·디자인 변경 키워드 없음·기존 placeholder *대체*는 modify 아닌 add 시그널)

## 1. Test Plan 4블록

### Build

```bash
cd frontend && npm run build
```

**결과**: TS strict (`tsc -b`) 통과 + Vite **57 modules transformed in 1.52s** + dist/ CSS 8.08KB (gzip 2.16KB, +1.76KB I-07 대비) + JS 175.68KB (gzip 56.92KB, +8.76KB). exit 0.

### Automated tests

```bash
# 본 이슈 frontend 자동 테스트 N/A (WBS I-08 DoD)
# Backend 회귀: cd backend && uv run pytest -v → 77 passed (backend 미수정)
```

**결과**: frontend 0건 (WBS DoD). backend pytest **77 passed** 회귀 N/A.

### Manual verification

사람이 직접 확인 + 스크린샷 4장 첨부 (ADR-0046 §2.3 미체크 상태).

- [ ] `cd backend && uv run uvicorn realworld.main:app --port 8000` (터미널 1) + `cd frontend && npm run dev` (터미널 2) → 5173·8000 동시 부팅
- [ ] AC-01: `/register` → username=jane / email=jane@example.com / password=supersecret → submit → 201 + Header [Home/New Article/jane/Logout] + `/` 이동. **스크린샷 1: register page 폼 입력 상태**
- [ ] AC-01 (계속): 가입 직후 Header 로그인 상태. **스크린샷 3: logged-in header (jane 표시)**
- [ ] AC-02: `/register` 재진입 → 같은 email 시도 → submit → 422 + "이미 사용 중인 이메일입니다" 빨강 박스 인라인. **스크린샷 4: 422 error inline**
- [ ] AC-03: 새 시크릿 창 또는 Logout 후 `/login` → 정상 자격 → 200 + Header 전환. **스크린샷 2: login page 폼**
- [ ] AC-04: Logout 클릭 → `/login` + [Sign in/Sign up]
- [ ] AC-05: 가입/로그인 후 F5 새로고침 → Header 로그인 상태 유지
- [ ] GitHub Actions 워크플로 로컬 검증: backend-ci `paths: backend/**` 한정 → frontend 변경 N/A 사유. pr-body-checkboxes status check 정상

### DoD coverage

이슈 #8 DoD 7건 매핑 (PR body 미체크):

- [ ] D-08-1 LoginPage 실 폼 + 422 인라인
- [ ] D-08-2 RegisterPage 실 폼 + 422 인라인
- [ ] D-08-3 store/auth.ts (I-07 시그니처, 본 PR 무수정)
- [ ] D-08-4 api/client.ts Authorization + 401 처리 (simple catch 패턴)
- [ ] D-08-5 Header 로그인 상태 반영
- [ ] D-08-6 한글 에러 인라인 (extractErrorMessage)
- [ ] D-08-7 모바일 Chrome 깨짐 없이 렌더링

## 2. AI 게이트 6축

| # | 축 | 결과 | 근거 |
| --- | --- | --- | --- |
| 1 | 자동 테스트 통과 | ✅ N/A (DoD) | backend pytest 77 passed 무영향 |
| 2 | AI 코드 리뷰 PASS | ✅ PASS | code-review §0 PASS, 6 OX 모두 PASS, NEEDS-WORK 0 |
| 3 | Test Plan 4블록 첨부 | ✅ PASS | §1 위 4 subsection 완성 |
| 4 | 시크릿·보안 스캔 통과 | ✅ PASS | 신규 환경변수 0. localStorage 평문 JWT는 RealWorld spec 동일 패턴(학습 acceptable). React JSX escape 활용 + dangerouslySetInnerHTML 0 |
| 5 | 브라우저 골든패스 실증 + stylesheet | ✅ 조건부 PASS | gstack /qa는 I-09 골든패스에서 첫 호출. 본 PR은 Manual verification 4 스크린샷으로 대체 — 사람 책임. stylesheet: Tailwind 8.08KB CSS 실 추출 (I-07 6.32KB → +1.76KB = 폼·에러박스·로그인 분기 utility 클래스 정량 증거) |
| 6 | 로컬 부팅 가능성 | ✅ PASS | dev: `npm run build` 1.52s + `npm run dev` 608ms. stg/prod: N/A (RFP §NFR-06) |

추가 축 (ADR-0047): backend-ci `paths: backend/**` 한정 — frontend 변경에 미트리거. workflow 자체는 `pr-body-checkboxes` status check만 active.

## 3. 시나리오 인용

| 시나리오 | 출처 | 결과 |
| --- | --- | --- |
| AC-01 register happy (R-F-01) | acceptance §1 | ⏸ Manual verification |
| AC-02 register 422 duplicate (R-F-01) | acceptance §1 | ⏸ Manual verification |
| AC-03 login happy (R-F-02) | acceptance §1 | ⏸ Manual verification |
| AC-04 logout | acceptance §1 | ⏸ Manual verification |
| AC-05 새로고침 후 로그인 유지 (R-F-03) | acceptance §1 | ⏸ Manual verification |
| 회귀 — backend 77 passed | acceptance §4 | ✅ backend 미수정 |
| build 57 modules + CSS 8.08KB | acceptance §4 | ✅ Vite build PASS |

## 4. FAIL 항목

(없음) — 6축 PASS, AC 5 모두 Manual verification 위임 (사람 재현 책임).

## 5. 발견 사항

- **양호**: contract §0 Referenced-IDs 6행 — selective read 진입점 정합
- **양호**: mode=add 자동 결정 (ADR-0032 규칙 4) — 7번째 무질문 진행
- **양호**: 4 코드 + 1 docs 커밋 모두 ADR-0021 정규식 통과
- **양호**: LoginPage·RegisterPage 거의 동일 패턴 — DRY 위반 검토 후 *2건뿐*이라 추상화 비용 더 큼 결정 (code-review F1)
- **양호**: I-07 zustand store 시그니처 그대로 사용 — BC 보장 + 인터페이스 안정성 입증
- **양호**: Tailwind CSS 실 추출 1.76KB (I-07 6.32KB → I-08 8.08KB) — utility 클래스 신규 사용 정량 증거 (form fields/error box/button states/conditional menu)
- **메모 (Sprint 2 진행)**: 본 PR 머지 시 Sprint 2 3/5 완료. 다음 진입: I-09 게시판 화면(S-01·S-02·S-03 + 댓글 UI + 골든패스 E2E + FCP + XSS — effort 2d ≈ 2.5-3.5h)

## 6. UI/FE 변경 검증

**ui_changed=false (의도)** — 본 PR은 *기능 동작 추가*(폼 인터랙션·에러·로그인 분기). 시각 디자인 자체 변경(token·layout·brand) 0. 골든패스 + 스크린샷 검증은 I-09(게시판 + gstack `/qa` 7단계 골든패스) 단일 시점에 집중. I-07 스캐폴딩 PR 동일 패턴.

- [gstack_qa_used]: gstack /qa N/A 사전 합의 (시각 디자인 변경 0, I-09에서 첫 호출)
- [console_errors]: N/A 사전 합의 (Manual verification에서 사람이 dev 콘솔 0개 확인)
- [stylesheet 적용 근거]: ✅ Tailwind utility 4 양축 — (1) tailwind.config content scan `src/**/*.{ts,tsx}` (Header·LoginPage·RegisterPage·App 포함) / (2) postcss + autoprefixer / (3) `src/index.css` 3 directive / (4) main.tsx import. 빌드 산출 CSS **8.08KB gzip 2.16KB** (I-07 6.32KB → +1.76KB) — form fields·error box·conditional menu utility 실 추출 정량 증거

| 화면 | 시나리오 | 스크린샷경로 | stylesheet 적용 |
| --- | --- | --- | --- |
| N/A | N/A — ui_changed=false 기능 동작 추가 PR. 시각 디자인 변경 0. 스크린샷 검증은 I-09 골든패스 시점 | N/A | N/A — Tailwind utility 적용은 §5 stylesheet 적용 근거 (1.76KB 정량) |

## 7. 로컬 부팅 가능성

| 프로파일 | 부팅 명령 | 결과 (ready 신호) | 에러 | 부팅 자산 변경 |
| --- | --- | --- | --- | --- |
| dev | `(cd backend && uv run uvicorn realworld.main:app --port 8000)` + `(cd frontend && npm install && npm run dev)` | ✅ backend uvicorn 8000 + frontend `VITE v5.4.21 ready in 608ms` (5173 또는 fallback 5174) | 0건 | 부팅 자산 변경 0 — pyproject·package.json·alembic·.env.example 모두 무수정. 코드 4 파일만 |
| stg | N/A — 단일 환경 운영 (RFP §NFR-06) | N/A | N/A | N/A |
| prod | N/A — 단일 환경 운영 | N/A | N/A | N/A |

[LOCAL.md 동기]: ✅ N/A 부팅 자산 변경 없음 — LOCAL.md §3 dev 명령은 I-07에서 이미 정착
