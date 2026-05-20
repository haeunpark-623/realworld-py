---
doc_type: brief
version: v0.2 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: A
related:
  R-ID: []
  F-ID: []
  supersedes: null
---

# realworld-py — Project Brief

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.2 | 2026-05-20 | woosung.ahn@bespinglobal.com | 게이트 A·B 사용자 결정 반영 — 단위 테스트 정량 ADR-0015 정책값 채택 / FastAPI / SPA / 게이트 C 사전 결정 |
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-init` Phase 1/4, RFP.md 흡수) |

## 1. 한 줄 정의

RealWorld(Conduit) 스펙을 베이스로 한 **게시판 웹 애플리케이션**을 Python 백엔드로 2일 내 풀 사이클(요구→설계→구현→검증) 완주한다. 1차 학습 과제로, AI 페어(agent-toolkit)와의 협업 사이클 자체가 핵심 산출이다.

## 2. 배경 / 문제 정의

- 사내 "웹 개발 뉴비 과제" — 신규 입사자가 풀 사이클을 한 번 완주해 보는 학습 과제.
- 기존 RealWorld 레퍼런스(Conduit)는 다양한 언어/프레임워크 구현을 제공하지만 *팔로우·즐겨찾기·태그 피드* 등 부가 기능까지 포함해 2일 학습 범위로는 과대하다.
- 따라서 **MVP를 Auth + Article + Comment + 최소 UI**로 좁히고, 부가 기능은 명시적으로 Out of Scope 처리.
- 동시에 **AI 게이트 6축**(ADR-0011 + ADR-0037)·**부팅 자산 동기화**(ADR-0040)·**브랜치 전략**(ADR-0044) 등 agent-toolkit이 강제하는 품질·운영 규칙을 1회 따라가 보는 것이 학습의 본 목적.

## 3. 핵심 사용자 / 이해관계자

| 구분 | 주체 | 관심사 |
|---|---|---|
| 1차 사용자 — 비회원 방문자 | 임의의 웹 방문자 | 게시글 열람, 댓글 읽기 |
| 1차 사용자 — 가입 사용자 | 회원가입을 한 사용자 | 글·댓글 CRUD, 자기 글 관리 |
| 2차 이해관계자 — 과제 검토자 | 사내 멘토 / 리뷰어 | 학습 사이클 완주 여부, 산출물 품질 |
| 2차 이해관계자 — 본인(개발자) | 박하은 (woosung.ahn) | AI 협업 사이클 1회 완주, 산출물 14종 생성 경험 |

> 관리자 페르소나는 1차 학습 과제 범위에서 제외 (Out of Scope, RFP §2 명시).

## 4. 목표 (성공 정의)

| KPI | 측정 방법 | 목표값 | 달성 시점 |
|---|---|---|---|
| 풀 사이클 완주 | NEW_PROJECT 4 Phase(`/flow-init` → `/flow-design` → `/flow-wbs` → `/flow-bootstrap`) + FEATURE 사이클 1회 이상 완주 | 4 Phase + 1 FEATURE 모두 완주 | 2026-05-22 |
| 로컬 부팅 가능성 | fresh checkout 후 `LOCAL.md` §3 부팅 명령으로 dev 서버 기동까지 소요 시간 | ≤ 5분 | 2026-05-22 |
| 골든패스 통과 | 회원가입 → 로그인 → 게시글 작성 → 댓글 작성 → 게시글 수정 → 삭제 시나리오를 gstack `/qa`로 브라우저 실증 | 1회 PASS + 스크린샷 첨부 | 2026-05-22 |
| 단위 테스트 커버리지 (핵심 비즈니스 로직) | pytest --cov, 대상 = 인증·권한·CRUD 핵심 서비스 모듈 | ≥ 80% (ADR-0015 §2.3 정책) | 2026-05-22 |
| AI 게이트 6축 통과 | `qa-test --ai` 6축(contract·plan·acceptance·risk·UI 실증·3 profile 부팅) 전부 PASS | 6/6 | 2026-05-22 |
| ADR 작성 | 핵심 결정 2건 — (1) 백엔드 프레임워크, (2) 프론트엔드 렌더링 방식 | ADR 2건 이상 | 2026-05-21 (게이트 C 시점) |
| PR squash merge | `main`에 squash merge된 PR | 1건 이상 | 2026-05-22 |

> 위 정량값은 RFP §NFR-05의 기준과 차이가 있다. ADR-0015 §2.3(툴킷 정책)을 따라 ≥ 80%로 상향했고, Open Questions §1에서 사용자 컨펌을 요청한다.

## 5. 비목표 (Out of Scope)

- 사용자 팔로우 / 팔로잉 피드 (RealWorld spec의 follow-related endpoints 전부)
- 게시글 즐겨찾기(favorite) / 좋아요 수
- 태그별 피드 / 인기 태그 사이드바
- 프로필 이미지 업로드
- 비밀번호 찾기 / 이메일 검증 메일 발송
- 다국어 / 다크모드
- 클라우드 배포 — 로컬 부팅만 필수. dev/stg/prod 3 profile은 단일 환경 운영으로 N/A 처리(RFP §NFR-06, ADR-0037 §단일 환경 운영 허용 절)
- 관리자 페르소나 / 모더레이션 기능
- 실시간(WebSocket) 알림 / 푸시

## 6. 일정 (대략)

| 일자 | Phase | 활동 |
|---|---|---|
| 2026-05-20 (Day 0) | 준비 | RFP·툴킷 설치 완료. `/flow-init` 본 메타 진행 → 01·02·03·04·05 산출. Gate A·B 휴먼 검토 |
| 2026-05-21 (Day 1 오전) | `/flow-design` (Phase 2/4) | HLD·LLD·코드 규약·API·테스트 설계 (06~13). Gate C 휴먼 검토 + ADR 2건 작성 |
| 2026-05-21 (Day 1 오후) | `/flow-wbs` + `/flow-bootstrap` | WBS 분해 + sprint-bootstrap으로 GitHub Issue·Milestone 등록. mode=sprint 전환 |
| 2026-05-21 ~ 22 | `/flow-feature` 반복 | 이슈 단위로 FEATURE 사이클 — change-contract → plan → implement → review → qa-test → PR squash merge |
| 2026-05-22 | 마감·회고 | DoD 7개 항목 점검, `/retro` 1회, README/LOCAL.md 마무리 |

## 7. 리스크 (초기 식별)

| ID | 리스크 | 영향 | 완화책 |
|---|---|---|---|
| RISK-01 | 뉴비 + 2일 일정 → MVP 일부 기능 미완성 가능성 | Mid | MVP를 RFP에서 이미 최소화(F-01~F-04만). `/flow-wbs`에서 시간 박스 추가 분해. F-04 UI 영역은 가장 마지막에 시간 남는 만큼만 진행 |
| RISK-02 | 백엔드 프레임워크 결정 지연(FastAPI vs Django vs Flask) → 설계가 멈춤 | High | `/flow-design` Phase 2/4의 ADR 첫 작업으로 트레이드오프 표 + 1회 결정. 결정 후 번복 금지 |
| RISK-03 | 인증·권한 로직 보안 결함(JWT secret 노출, bcrypt 미적용 등) | High | bcrypt + JWT 환경변수 강제. `/cso` 보안 점검을 PR 단계마다 통과. CLAUDE.md "보안 절대 규칙" 6개 항목 100% 준수 |
| RISK-04 | NFR-02 퍼포먼스 미달 (API p95 ≥ 200ms 또는 FCP ≥ 1.5s) | Low | 게시글 100건 시드 + ORM eager loading + slug/created_at 인덱스. 게시판이라 트래픽·복잡 쿼리 없음 |
| RISK-05 | 부팅 자산 동기 누락(LOCAL.md ↔ migrations ↔ .env.example) → AI 게이트 6축 BLOCK | Mid | dev 1 profile만 운영하므로 부팅 자산 1세트만 관리. PR마다 같은 커밋에서 동기 갱신. 단일 환경은 N/A 사유 명시 |
| RISK-06 | 학습 목표가 산출물 14종 생성에 매몰돼 실제 동작 코드 부족 | Mid | 골든패스 1회 통과(`/qa`)를 DoD §3 최우선으로 두고, 산출 문서는 BLOCK 통과 수준에서 멈춘다(과잉 작성 금지) |

## 8. Open Questions

1. ~~단위 테스트 정량 목표~~ — **결정 (v0.2, 2026-05-20)**: ADR-0015 §2.3 정책값(≥ 80%) 채택. RFP §NFR-05 60% 값으로의 예외 ADR 신설 안 함. 적용 범위는 04-srs §R-N-06 명시(*인증·권한·CRUD 핵심 서비스 모듈* 한정).
2. ~~백엔드 프레임워크~~ — **결정 (v0.2, 2026-05-20)**: **FastAPI** 채택. 사유: SPA(REST API 자연 결합), Pydantic 검증·OpenAPI 자동 생성으로 09-api-spec 산출 부담 감소, `uv run` 부팅 단순. `/flow-design`에서 ADR로 정식화.
3. ~~프론트엔드 렌더링 방식~~ — **결정 (v0.2, 2026-05-20)**: **SPA** 채택 (React + Vite + REST API 호출). FastAPI와 자연 결합. NFR-02 FCP 1.5s 미달 리스크는 게이트 C에서 코드 스플리팅·번들 크기 점검 강제. `/flow-design`에서 ADR로 정식화.
4. **데이터베이스** — SQLite (개발 편의) vs PostgreSQL (운영 정합). 게이트 C에서 ADR로 확정. *학습 컨텍스트 + 단일 환경 운영 가설은 SQLite 유리, 운영 시나리오 학습성은 PostgreSQL 유리*.
5. **테스트 도구 보강** — pytest 확정, fixtures·factory 도구(pytest-factoryboy 등) 채택 여부는 게이트 C(`docs/planning/13-test-design`)에서 결정.
