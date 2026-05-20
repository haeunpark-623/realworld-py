---
doc_type: index
version: v0.6
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: ""
related: { R-ID: [], F-ID: [], supersedes: null }
---

# realworld-py — docs/planning Index

> Phase 1~4/4 NEW_PROJECT 메타 모두 완료. mode=sprint 진입. Sprint 1 Issue #1 머지 완료(PR #11). Issue #2 PR #12 머지 대기 (status:in-review).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
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
