---
doc_type: feature-eng-review
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

# feat-frontend-scaffold — Engineering Review

> P5 plan-eng-review. contract + plan 자기검토. PASS — NEEDS-WORK 0.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — PASS. 6 OX 모두 PASS. npm 채택 점진 합의 명시 |

## 0. Verdict

**PASS** — contract §0 6행·§2 16행 + plan 3 commit DAG. P8 implement 진입 허용.

- [verdict]: PASS
- [reviewer]: woosung.ahn@bespinglobal.com (self-review, generator)
- [review_at]: 2026-05-21

## 1. Contract 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| §0 Referenced-IDs 6행 (ADR-0018) | ✅ | SRS R-N-02 / PRD F-04 / 10-lld-screen-design §1·§3 / 12-scaffolding §1·§5·§8 / ADR-0002·0004 / test catalog N/A 명시 |
| §1 변경 의도 명확 | ✅ | I-08·I-09 진입 기반 + npm 채택 점진 합의 인라인 명시 |
| §2 Before/After 16행 | ✅ | package + vite + tsconfig + index.html + tailwind/postcss + .env + .gitignore + 6 pages + Header + api + store + types |
| §3 Call Sites 3행 (CLI / backend CORS / CI) | ✅ | backend·CI 무수정 명시. 양축 sync (LOCAL.md + 12-scaffolding) 명시 |
| §4 BC neutral | ✅ | backend 무수정, frontend 신규 워크스페이스 |
| §5 Rollback 1-commit revert | ✅ | git revert + frontend/ 일괄 제거. 데이터 영향 0 |

## 2. Plan 검토

| 항목 | 결과 | 근거 |
| --- | --- | --- |
| §1 3 commit DAG (C1 셋업 → C2 src → C3 docs) | ✅ | 모든 커밋 메시지 ADR-0021 정규식 통과 (chore/feat/docs) |
| §2 의존성 그래프 — 순환 없음 | ✅ | C1 → C2 → C3 선형 |
| §3 테스트 매핑 — WBS DoD N/A | ✅ | 수동 부팅 검증으로 대체 (스키마 BLOCK 회피 위해 (없음) 표기) |
| §4 빌드·실행 검증 4단계 (npm install·build·dev·proxy) | ✅ | LOCAL.md §3 동기 명시 |
| §5 점진 합의 5건 (pnpm→npm·CL 미도입·zustand·Tailwind preset·engines) | ✅ | 후속 ADR 0건. code-review 인라인 메모로 충분 |

## 3. UX 검토

mode=add scaffolding — 실제 UX 동작 0. placeholder만이라 ux-flow-design 별도 호출 N/A. 10-lld-screen-design §1 화면 인벤토리(S-01~S-06)와 라우트 매핑 1:1 정합 확인.

## 4. 6단계 폴더링 충족

본 PR 산출 위치:
- `docs/features/feat-frontend-scaffold/feat-frontend-scaffold.{brief,contract,plan,eng-review,acceptance,risk,code-review,ai-qa-report}.md` — `feat-` 접두 + 평면 명명 (document-manifest §3.2)
- 코드: `frontend/` 워크스페이스 신규 (1수준 폴더)

## 5. frontmatter / Manifest 검증

- brief: doc_type=feature-brief, R-N-02 + F-04 ✅
- contract: doc_type=feature-contract, §0 BLOCK 통과 ✅
- plan: doc_type=feature-plan, §1·§2·§3·§4·§5 BLOCK 통과 ✅
- eng-review (본 문서): doc_type=feature-eng-review, R-N-02 ✅
- 모든 산출 date=2026-05-21 / author=woosung.ahn@bespinglobal.com 정합

## 6. 발견 사항 (3축 OX)

ADR-0008 in_scope / blocks_merge / same_area 3축:

| Q | 답 | 처리 |
| --- | --- | --- |
| F1: pnpm → npm 변경이 backend-ci.yml 또는 정합성에 영향? | ⭕ in_scope / ❌ no blocks_merge / ⭕ same_area | INFO. backend-ci `paths: backend/**` 한정이라 npm 무관. 12-scaffolding §1 트리에서 lockfile 명칭만 갱신 |
| F2: Tailwind preset 미도입 — 게시글 본문 마크다운 렌더링 시 영향? | ⭕ / ❌ / ⭕ | INFO. I-09 게시판 진입 시 결정 — `@tailwindcss/typography` 추가 vs 직접 HTML (학습 부담 작은 쪽) |
| F3: Vite proxy `/api → :8000` 하드코딩 — 환경별 분기? | ⭕ / ❌ / ⭕ | INFO. dev 1 profile 운영(RFP §NFR-06)이라 분기 불필요. 운영용 빌드는 `VITE_API_BASE_URL`로 override |
| F4: zustand store가 placeholder만 — I-08에서 인터페이스 break 위험? | ⭕ / ❌ / ⭕ | INFO. I-08 진입 시 zustand store 본격 구현하므로 placeholder 시그니처(`user/token`)는 일관 유지. 인터페이스 안정성 충분 |
| F5: Tailwind 토큰을 tailwind.config에 extend 안 함 (기본 팔레트 활용) | ⭕ / ❌ / ⭕ | 의도. 10-lld-screen-design §3 Tailwind 기본값 채택 선언과 정합 |
| F6: Node engines 명시 안 함 — fresh checkout 시 호환 위험? | ⭕ / ❌ / ⭕ | INFO. Vite 5는 Node 18+ 요구. LOCAL.md §1 "Node 22 LTS" 메모로 충분 (학습 컨텍스트) |

NEEDS-WORK 0건.

## 7. NEEDS-WORK 항목

(없음) — 6 OX 모두 PASS. P6 acceptance 진입 허용.
