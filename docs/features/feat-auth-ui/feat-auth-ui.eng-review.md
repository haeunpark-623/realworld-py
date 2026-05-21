---
doc_type: feature-eng-review
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

# feat-auth-ui — Engineering Review

> P5 plan-eng-review. PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — PASS, 6 OX 모두 PASS, simple catch 패턴·loadFromStorage 위치·errors body 첫 행만 결정 명시 |

## 0. Verdict

**PASS** — contract §0 6행·§2 6행 + plan 5 commit DAG. P8 implement 진입 허용.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (self-review)
- [review_at]: 2026-05-21

## 1. Contract 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| §0 Referenced-IDs 6행 (ADR-0018) | ✅ | SRS R-F-01~03 / PRD F-01·F-04 / 10-lld-screen §2 S-04·S-05 + §1.1 / 09-api-spec §3 / 12-scaffolding §1 / Test catalog N/A 명시 |
| §1 변경 의도 명확 | ✅ | I-07 placeholder → 실 구현. simple catch 패턴 인라인 명시 |
| §2 Before/After 6행 | ✅ | LoginPage·RegisterPage·Header·App.tsx·types/api.ts + store/auth.ts 무수정(I-07 시그니처 그대로) |
| §3 Call Sites 4행 | ✅ | apiFetch·useAuthStore·backend 라우트·CORS 모두 무수정 명시 |
| §4 BC neutral | ✅ | frontend 내용 변경, 외부 인터페이스 무수정. backend 무영향 |
| §5 Rollback 1-commit revert | ✅ | squash merge → 4 파일 + 1 helper 자동 revert. localStorage 잔존은 수동 처리 명시 |

## 2. Plan 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| §1 5 commit DAG | ✅ | C1 헬퍼 → C2 Login → C3 Register → C4 Header+App → C5 docs. ADR-0021 정규식 통과 |
| §2 의존성 그래프 — 순환 없음 | ✅ | 선형 진행 |
| §3 테스트 매핑 — WBS DoD N/A | ✅ | 수동 부팅 검증으로 대체 (스키마 (없음) 표기) |
| §4 빌드·실행 검증 5단계 (build·동시 부팅·시도·회귀) | ✅ | UC-01 골든패스 시도 명시 — (a)~(e) 5 단계 |
| §5 점진 합의 5건 (catch 패턴·storage 키·컴포넌트 추출·errors 첫 행·loadFromStorage 위치) | ✅ | 후속 ADR 0건 |

## 3. UX 검토

- 10-lld-screen-design §2 S-04·S-05 정합 — email/password·username 3 필드
- §3.1 Color 토큰: 422 에러 인라인 시 `bg-red-50 text-red-600 border-red-300` (Tailwind 기본 + 디자인 토큰 정합)
- §3.4 Component primitives — Input·Button은 본 PR scope out (I-09). 폼 직접 작성으로 충분
- a11y: `<label htmlFor>` + `<input id>` 매핑 + 422 에러 시각+텍스트 동시 (§4 강제)

## 4. 6단계 폴더링 충족

- `docs/features/feat-auth-ui/feat-auth-ui.{brief,contract,plan,eng-review,acceptance,risk,code-review,ai-qa-report}.md` — `feat-` 접두 (mode=add)
- 코드: `frontend/src/pages/` + `components/` + `App.tsx` + `types/api.ts` — 기존 구조 reuse

## 5. frontmatter / Manifest 검증

- 모든 산출 date=2026-05-21 / author=woosung.ahn@bespinglobal.com / R-F-01·02·03 + F-01·04 정합

## 6. 발견 사항 (3축 OX)

| Q | 답 | 처리 |
| --- | --- | --- |
| F1: store/auth.ts 무수정으로 I-07 placeholder 시그니처 그대로 사용 — token expire 자동 갱신 부재 | ⭕ in_scope / ❌ no blocks_merge / ⭕ same_area | INFO. 본 PR scope out — backend JWT 7일 expiry. 만료 시 401 catch → logout |
| F2: errors body 첫 행만 표시 — 다중 검증 에러 누락 | ⭕ / ❌ / ⭕ | INFO. backend Pydantic은 보통 첫 에러만 반환 (RealWorldError 형식). 다중 에러 케이스는 I-09 폼 검증 강화 시 결정 |
| F3: simple catch 패턴 — 4xx 모든 케이스를 LoginPage/RegisterPage가 직접 handle | ⭕ / ❌ / ⭕ | INFO. interceptor over-engineering 회피. 본 PR scope out |
| F4: loadFromStorage를 App.tsx mount useEffect 1회로만 호출 — token 만료 자동 검증 부재 | ⭕ / ❌ / ⭕ | INFO. I-09 골든패스 진입 시 GET /api/user 호출로 token 검증 결정 |
| F5: Header logged-in 메뉴 {user.username} 클릭 시 `/profile/{username}` 이동 — ProfilePage P2 컷 후보 | ⭕ / ❌ / ⭕ | INFO. 14-wbs §0.3 P2 컷 후보. 본 PR은 link 노출만 + ProfilePage placeholder는 I-07 그대로 유지 |
| F6: ui_changed=true — ADR-0011 스크린샷 강제 충족 가능? | ⭕ / ❌ / ⭕ | 의도. Manual verification에 스크린샷 4장(login·register·logged-in header·422 error) 첨부 책임을 사람에게 위임. PR description에 명시 |

NEEDS-WORK 0건.

## 7. NEEDS-WORK 항목

(없음) — 6 OX 모두 PASS. P6 acceptance 진입 허용.
