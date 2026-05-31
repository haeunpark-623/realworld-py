---
doc_type: index
version: v0.15
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-22
gate: ""
related: { R-ID: [], F-ID: [], supersedes: null }
---

# realworld-py — docs/planning Index

> **2일 사이클 완주 + 차세대 follow-up 진입** — Sprint 1·2 10/10 머지 완료 (PR #11~#20). 본 PR #22(Issue #21)는 PRD §3 F-01 실패 path acceptance gap 3건 closure — 비로그인 차단·한글 폼 에러·JWT 만료 자동 logout. 다음: F-TAG-FEED / F-FAVORITE / F-FOLLOW 신규 기능 follow-up.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.15 | 2026-05-22 | woosung.ahn@bespinglobal.com | **Follow-up bug PR #22 open** — Sprint 1·2 10/10 머지 후 PRD acceptance gap closure. Issue #21 (bug/auth-ux-gap-issue-21). fix(frontend) 3 + docs(plan) 1 = 4 커밋. 3건 동시 fix: (A) RequireAuth 컴포넌트 + App.tsx 3 라우트 wrap(/editor·/editor/:slug·/profile/:username) — 비로그인 차단(PRD F-02 실패-2) / (B) LoginPage·RegisterPage·EditorPage·CommentItem 4 폼 onInvalid 한글 메시지 — F-04 §5 한글 원칙 / (D) api/client.ts 401 자동 logout + /login(PRD F-01 실패-3). I-08 simple catch 패턴 회귀 결정 — contract §1·plan §5·retro 양축 trace. 빌드 61 modules + CSS 10.91KB 변경 0(시각 무변경 정량 증거). 회귀: backend 77 passed. 다음: F-TAG-FEED 신규 기능 |
| v0.14 | 2026-05-21 | woosung.ahn@bespinglobal.com | **사이클 종료 PR #20 open** — Issue #9 머지 완료(PR #19) + 마지막 Issue #10 작업 진입 (status:in-review). 14-wbs v0.13. feat-closing-cycle 8 산출 + README.md + CHANGELOG.md v0.1.0(Keep a Changelog 형식) + retro `docs/planning/retro/2026-05-21-cycle.md`(5+5+5 형식). 보안 자동 점검 4 항목 PASS — `.env` git 0건 / JWT 평문 0건 / secret 평문 0건 / CORS=`http://localhost:5173` wildcard 미사용. backend pytest **77 passed** 회귀 안정. 본 PR 머지 시 **Sprint 1·2 10/10 — AI 페어 학습 과제 2일(16h) 완주** |
| v0.13 | 2026-05-21 | woosung.ahn@bespinglobal.com | Sprint 2 Issue #8 머지 완료(PR #18) + Issue #9 작업 진입 + PR #19 open (status:in-review). 14-wbs v0.12 (I-09 status:in-review). feat-board-ui 8 산출. **Sprint 2 핵심 마일스톤** — 6 화면 실 동작(HomePage 목록+페이지네이션+4 상태 / ArticlePage 본문+댓글 UI+작성자 액션+삭제 모달 / EditorPage 새 글+수정 / ProfilePage R-F-12) + 3 신규 컴포넌트(ArticleCard·CommentItem 인라인 편집 R-F-13·Modal). **P2 컷 후보 3종 모두 본 PR 채택** — 시간 박스 fit. 빌드 60 modules in 1.14s + CSS 10.91KB(+2.83KB I-08 대비). 골든패스 7단계 + FCP/XSS Manual verification. 다음: I-10 (Sprint 2 마지막 — /cso·README·CHANGELOG·/retro) |
| v0.12 | 2026-05-21 | woosung.ahn@bespinglobal.com | Sprint 2 Issue #7 머지 완료 (PR #17) + Issue #8 작업 진입 + PR #18 open (status:in-review). 14-wbs v0.11 (I-08 status:in-review). feat-auth-ui 8 산출 + types/api.ts ErrorBody·extractErrorMessage + LoginPage·RegisterPage 실 폼(controlled inputs + 422 한글 에러 인라인) + Header logged-in/out 분기 + App.tsx mount loadFromStorage. store/auth.ts·api/client.ts 무수정(I-07 시그니처 그대로). build 57 modules in 1.52s + CSS 8.08KB(+1.76KB I-07 대비). ui_changed=false (시각 디자인 변경 0). 다음: I-09 게시판 |
| v0.11 | 2026-05-21 | woosung.ahn@bespinglobal.com | Sprint 2 Issue #6 머지 완료 (PR #16) + Issue #7 작업 진입 + PR #17 open (status:in-review). 12-scaffolding v0.8 (§1 frontend 트리 npm 채택 + §5.2·§5.3 부팅 명령 npm 갱신 + §6 VITE_API_BASE_URL=/api proxy + §7 lockfile package-lock.json). LOCAL.md v0.3 (§1·§2·§3.1·§4·§5.7 pnpm→npm 갱신, frontend 실 검증 표기). 14-wbs v0.10 (I-07 status:in-review). feat-frontend-scaffold 8 산출 + Vite 5.4 + React 18.3 + TS 5.6 + Tailwind 3.4 + react-router-dom 6.28 + zustand 4.5 + 6 페이지 placeholder + Header + api/store/types placeholder. npm install 140 packages + build 41 modules in 1.38s + dev ready in 346ms @ 5173. 다음: I-08 auth UI |
| v0.10 | 2026-05-21 | woosung.ahn@bespinglobal.com | Sprint 1 5/5 완료 (Issue #5 PR #15 머지) → Sprint 2 진입. Issue #6 작업 진입 + PR #16 open (status:in-review). 12-scaffolding v0.7 (§1 트리 models/comment + repositories/comment + services/comment + schemas/comment + routers/comments + alembic 0004 + tests 추가). 14-wbs v0.9 (I-06 status:in-review). feat-comment-module 8 산출 + Comment 모델(article_id FK CASCADE + author lazy=joined) + CommentService 4 메서드 + 4 라우트 nested (R-F-13 PUT 비표준 포함) + 단위 11 + 통합 12 + CASCADE 1 = 회귀 53→77 passed. CommentRepo.add·CommentService.update lazy load 충돌 해소 — get_by_id() fresh reload 패턴(I-04 F2 재사용) |
| v0.9 | 2026-05-21 | woosung.ahn@bespinglobal.com | Sprint 1 Issue #4 머지 완료(PR #14) + Issue #5 작업 진입 + PR #15 open (status:in-review). 12-scaffolding v0.6 (§1 트리 scripts/__init__·scripts/seed_articles·tests/integration/test_performance 표기). 14-wbs v0.8 (I-05 상태 in-review). feat-seed-performance 7 산출 + 멱등 seed (User 10 + Article 100 + Tag 5 + random.seed(42)) + R-N-01 측정 게이트 (warmup 10 + 측정 90 statistics.quantiles[18]) **p95=4.24ms PASS** (threshold 200ms, 마진 ~47배). selectinload N+1 회피(I-04) 정량 입증. 회귀: 53 passed (52 + 1). Sprint 1 5/5 완료 — Sprint 2 진입 가능 |
| v0.8 | 2026-05-21 | woosung.ahn@bespinglobal.com | Sprint 1 Issue #3 머지 완료 + Issue #4 작업 진입 + PR #14 open (status:in-review). 12-scaffolding v0.5 (§1 트리 models/article + repositories/article + services/article + utils/slug + schemas/ + routers/ + alembic 0003 + tests/integration/ 추가). 14-wbs v0.7 (I-04 상태 in-review). feat-users-articles 8 산출 + Article/Tag M2M + ArticleService 5 메서드 + 8 라우트 + RealWorldError handler inline + 단위 13 + 통합 19 = 52 passed |
| v0.7 | 2026-05-21 | woosung.ahn@bespinglobal.com | Sprint 1 Issue #2 머지 완료 + Issue #3 작업 진입 + PR #13 open (status:in-review). 12-scaffolding v0.4 (§1 트리 utils/services/deps/errors + 3 test 파일 추가). 14-wbs v0.6 (I-03 상태 in-review). feat-auth-service 8 산출 + AuthService + bcrypt + JWT + require_auth + 14 단위 테스트 |
| v0.6 | 2026-05-20 | woosung.ahn@bespinglobal.com | Sprint 1 Issue #1 머지 완료 + Issue #2 작업 진입 + PR #12 open (status:in-review). 12-scaffolding v0.3 (§1 트리에 test_user_repo.py 추가). 14-wbs v0.5 (I-02 상태 in-review) |
| v0.5 | 2026-05-20 | woosung.ahn@bespinglobal.com | Sprint 1 Issue #1 작업 진입 + PR #11 open (status:in-review). 12-scaffolding v0.2 정합 갱신 (§1 트리·§6 env 키 정합). 14-wbs v0.4 (I-01 상태 in-review) |
| v0.4 | 2026-05-20 | woosung.ahn@bespinglobal.com | `/flow-wbs` Phase 3/4 완료 — 15-risk(8건) + 14-wbs(Sprint 2 × Issue 10 + §7 sprint-bootstrap YAML) 작성. validate-doc.sh PASS |
| v0.3 | 2026-05-20 | woosung.ahn@bespinglobal.com | `/flow-design` Phase 2/4 완료 — 06·07·08·09·10·11·12·13 산출 8건 + ADR 4건 작성. validate-doc.sh 모두 PASS |
| v0.2 | 2026-05-20 | woosung.ahn@bespinglobal.com | 게이트 A·B 사용자 결정 반영 — 7건 Open Q 확정. 01·02·03·04·05 전부 v0.2 갱신 |
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | `/flow-init` Phase 1/4 완료. 01~05 5건 산출, validate-doc.sh 5/5 PASS |

## 산출 인벤토리

### Phase 1/4 — `/flow-init` (의도·요구)

| # | 폴더 / 파일 | layer | gate | status | 한 줄 요약 |
|---|---|---|---|---|---|
| 01 | [01-project-brief/](01-project-brief/01-project-brief.md) | 의도 | A ✅ | Draft v0.2 | 한 줄 정의·KPI·일정·리스크 6건 |
| 02 | [02-feasibility/](02-feasibility/02-feasibility.md) | 의도 | A ✅ | Draft v0.2 | 기술·비용·대안 5종 비교 + §6.1 게이트 B 사전 결정 7건 |
| 03 | [03-user-scenarios/](03-user-scenarios/03-user-scenarios.md) | 요구 | B ✅ | Draft v0.2 | 페르소나 2종 + UC-01~UC-12 + 비기능 시나리오 10건 |
| 04 | [04-srs/](04-srs/04-srs.md) | 요구 | B ✅ | Draft v0.2 | R-F-01~R-F-13 (기능 13) + R-N-01~R-N-06 (비기능 6) |
| 05 | [05-prd/](05-prd/05-prd.md) | 요구 | B ✅ | Draft v0.2 | F-01~F-04 + §1.1 기술 스택 사전 결정 + MVP Cut |

### Phase 2/4 — `/flow-design` (설계)

| # | 폴더 / 파일 | layer | gate | status | 한 줄 요약 |
|---|---|---|---|---|---|
| 06 | [06-architecture/](06-architecture/06-architecture.md) | Architecture | C | Draft v0.1 | Stack Decision 12행 + 시스템 컨텍스트 + 컨테이너 3개 |
| 07 | [07-hld/](07-hld/07-hld.md) | HLD | C | Draft v0.1 | 9개 모듈 분해 + 골든패스 데이터 흐름 + 비기능 대응 표 |
| 08 | [08-lld-module-spec/](08-lld-module-spec/08-lld-module-spec.md) | LLD | C | Draft v0.1 | 백엔드 5개 모듈 LLD + 외부 인터페이스 + 에러 처리 + 테스트 진입점 |
| 09 | [09-lld-api-spec/](09-lld-api-spec/09-lld-api-spec.md) | LLD | C | Draft v0.1 | RealWorld API 12개 엔드포인트 + Request/Response 상세 |
| 10 | [10-lld-screen-design/](10-lld-screen-design/10-lld-screen-design.md) | LLD | C | Draft v0.1 | S-01~S-06 화면 + 디자인 토큰 4종 (Color/Typography/Spacing/Component primitives) |
| 11 | [11-coding-conventions/](11-coding-conventions/11-coding-conventions.md) | 코드 규약 | C | Draft v0.1 | Python + TypeScript 명명 규칙 + 에러 코드 + Lint/Format + Import 정책 |
| 12 | [12-scaffolding/python.md](12-scaffolding/python.md) | 코드 규약 | C | Draft v0.1 | 디렉토리 트리 + Layered 패턴 + 모듈 경계 + 환경변수 + 부팅 자산 + Tailwind |
| 13 | [13-test-design/](13-test-design/INDEX.md) | 검증 | C | Draft v0.1 | 5절 분할 — 01-strategy / 02-catalog (R-/F- fan-in + 레벨 매트릭스) / 03-regression / 04-performance / 05-delivery-format |

### Phase 3/4 — `/flow-wbs` (운영)

| # | 폴더 / 파일 | layer | gate | status | 한 줄 요약 |
|---|---|---|---|---|---|
| 15 | [15-risk/](15-risk/15-risk.md) | 운영 | operations | Draft v0.1 | RISK-01~08, 5 카테고리(일정/기술/보안/외부 의존/운영). High 2건(일정·보안) 단계적 롤아웃 |
| 14 | [14-wbs/](14-wbs/14-wbs.md) | 운영 | operations | Draft v0.1 | Sprint 2개 × Issue 10개, R-/F-ID 100% 매핑, §7 sprint-bootstrap YAML (project + sprints) |

### ADR — 게이트 C 결정 4건

| ID | 결정 | 위치 | 상태 |
|---|---|---|---|
| ADR-0001 | 백엔드 프레임워크: FastAPI | [0001-backend-framework.md](adr/0001-backend-framework.md) | Draft |
| ADR-0002 | 프론트엔드: React + Vite + TypeScript (SPA) | [0002-frontend-spa.md](adr/0002-frontend-spa.md) | Draft |
| ADR-0003 | 데이터베이스: SQLite (단일 환경 운영) | [0003-database-sqlite.md](adr/0003-database-sqlite.md) | Draft |
| ADR-0004 | 스타일링 솔루션: Tailwind CSS | [0004-styling-tailwind.md](adr/0004-styling-tailwind.md) | Draft |

## 게이트 상태

| 게이트 | 상태 | 비고 |
|---|---|---|
| A (팀장 컨펌, 의도) | PASS | 01·02 사용자 결정 완료 (v0.2) |
| B (팀 합의, 요구) | PASS | 03·04·05 사용자 결정 완료 (v0.2), 7개 Open Q 확정 |
| C (개발팀 검토, 설계) | PASS | 06~13 + ADR 4건 작성 완료 (v0.3) |
| WBS 검수 (운영) | PENDING (휴먼 검토) | 14·15 작성 완료 (v0.4). 사용자 검수 후 `/flow-bootstrap` 호출 |

## 잔여 Open Questions (게이트 C 검토 + WBS 단계)

| 출처 | Question | 비고 |
|---|---|---|
| 01 §8.5 | 테스트 fixture·factory 도구 (pytest-factoryboy 등) | 13/01-strategy §2에서 미도입 결정 (학습 부담 회피). WBS에서 재검토 가능 |
| 03 §5.3 | 페이지네이션 cursor vs limit/offset | 13에서 limit/offset 가정 유지 |
| 03 §5.4 | 비로그인 회원가입 유도 배너 | 10-lld-screen-design §5.1에서 후속 결정으로 미룸 |
| 04 §6.4 | R-N-02 FCP 측정 자동화 | 13/04-performance §1.2에서 gstack `/qa` 1회 명시 |
| 04 §6.5 | R-F-12 P2 컷 후보 | WBS 단계에서 sprint 분배 시 결정 |
| 10 §5.1 | 모바일 반응형 햄버거 메뉴 | 시간 여유 시 추가, 본 MVP는 기본 흐름만 |
| 13/05 | 고객 납품 ID 채번 (TC-/SC-/IT-) 활성화 | 본 학습 과제는 미사용. 후속 과제에서 |

## 다음 단계

1. ~~사용자 게이트 A·B 휴먼 검토~~ — **완료** (v0.2)
2. ~~Phase 2/4 `/flow-design` 산출 + 게이트 C 검토~~ — **완료** (v0.3)
3. ~~Phase 3/4 `/flow-wbs` 산출~~ — **완료** (v0.4)
4. **현재 단계 — 사용자 WBS 검수**: 14·15 검토 (Sprint 구성·이슈 추정·R-/F-ID 매핑·리스크 카테고리)
5. **다음 메타 호출**: `/flow-bootstrap` Phase 4/4 — git commit + PR + sprint-bootstrap → GitHub Issue·Milestone 실 등록 + `mode=sprint` 전환

## 참고

- 본 산출은 `.claude/schemas/<doc_type>.schema.yaml` 형식 정본을 따른다 (ADR-0010)
- 13은 폴더 분할 모드(ADR-0030) — 5 sub-file + INDEX.md
- 게이트 C 결정 4건 ADR로 정식화 (ADR-0001~0004)
- LOCAL.md 본문 채움 완료 (ADR-0040 — 12-scaffolding/python.md §7과 양축)
- CLAUDE.md ## 기술 스택 placeholder 채움 완료
- devtoolkit.config.yaml tech_stack 갱신 완료
