---
doc_type: risk
version: v0.2 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: operations
related:
  R-ID: [R-N-01, R-N-02, R-N-03, R-N-04, R-N-05, R-N-06]
  F-ID: [F-01, F-02, F-03, F-04]
  supersedes: null
---

# realworld-py — Risk Register

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.2 | 2026-05-20 | woosung.ahn@bespinglobal.com | 마감 16h 기준 §3.1 단계적 컷 결정 시점 갱신 — 14-wbs §6.1과 동기 |
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-wbs` Phase 3/4, RFP §7 + 01 §7 + ADR-0001~0004 트레이드오프 통합 — 8건) |

## 1. 리스크 일람

| RISK-ID | 제목 | 영향(1~5) | 가능성(1~5) | 등급 | 영향 받는 Sprint/Issue | 대응 |
|---|---|---|---|---|---|---|
| RISK-01 | 2일 마감 + 1인 뉴비 — MVP 일부 미완성 | 3 | 4 | High | Sprint 1·2 전반 | 시간 박스 + P2 컷 후보 명시 (R-F-12·F-04 일부) |
| RISK-02 | 인증·시크릿 보안 결함 | 5 | 2 | High | Sprint 1 (I-02·I-03) | bcrypt + JWT 환경변수 + `/cso` 매 PR 점검 + Sprint 2 마지막 회귀 |
| RISK-03 | SQLAlchemy 2.x async API 학습 부담 | 2 | 3 | Mid | Sprint 1 (I-01·I-03·I-04) | 공식 튜토리얼 30분 사전 학습 + AsyncSession fixture를 conftest.py 1곳에 집중 |
| RISK-04 | F-04 UI 회귀 안전망 부재 (E2E 1회만) | 3 | 3 | Mid | Sprint 2 (I-09) | 골든패스 7단계 스크린샷 강제 + Sprint 2 마지막에 PR 시 골든패스 재실행 |
| RISK-05 | 산출물 매몰 — 코드 < 문서 진행 | 2 | 3 | Mid | Sprint 1·2 전반 | DoD §3 골든패스 통과를 P0로 두고 산출 문서는 BLOCK 통과 수준에서 멈춤 (과잉 작성 금지) |
| RISK-06 | gstack `/qa` 도구 가용성 | 3 | 2 | Mid | Sprint 2 (I-09) | Sprint 1 끝 시점에 `/qa` 1회 dry-run으로 도구 환경 사전 점검 |
| RISK-07 | R-N-01·R-N-02 성능 미달 (p95 ≥ 200ms 또는 FCP ≥ 1.5s) | 2 | 2 | Low | Sprint 1 (I-05·I-07) · Sprint 2 (I-09) | eager loading + 인덱스 + Vite 코드 스플리팅 사전 적용. 측정값 미달 시 게이트 C에서 추가 ADR |
| RISK-08 | 부팅 자산 동기 누락 (LOCAL.md ↔ 12-scaffolding §7 ↔ 실제) | 2 | 2 | Low | Sprint 2 후반 PR | 매 PR에서 부팅 자산 변경 시 같은 커밋에 LOCAL.md + 12-scaffolding §7 동기 갱신. AI 게이트 6번째 축이 lint |

> 등급 계산: 영향 × 가능성 → 1~6 Low · 7~14 Mid · 15~25 High. RISK-01·02는 곱이 12·10이지만 *시스템 차원 영향*이 커서 High로 격상.

## 2. 리스크 상세

### RISK-01: 2일 마감 + 1인 뉴비, MVP 일부 미완성

- **카테고리**: 일정
- **설명**: 16h 작업 시간 + 학습 곡선(FastAPI·SQLAlchemy 2.x async·React·Vite·Tailwind 동시) → WBS의 ~10개 이슈가 모두 통과하지 못할 가능성.
- **영향**: DoD §3 골든패스 미통과 시 *사이클 완주* 자체가 깨짐. AI 게이트 6축 통과 실패.
- **가능성**: 학습 곡선 + 결정 지연 가능성으로 *높음*. 게이트 B에서 결정 7건은 닫았으나 구현 단계 결정(slug 정규식·CORS 설정·migration 충돌 등)이 누적 가능.
- **현재 상태**: 모니터링
- **트리거 신호**: Sprint 1 종료 시점에 backend 통합 테스트 미통과 / 게시글 100건 시드 실패 / API p95 측정 시점 도달 못함
- **완화 전략**:
  - WBS 단계에서 P2 컷 후보 명시 — R-F-12(내 프로필) / S-06(Profile 화면) / F-04의 모바일 반응형
  - Sprint 1 끝 시점에 backend 5개 라우트 통합 테스트 통과를 *마일스톤*으로
  - Sprint 2 끝 30분 전엔 PR 머지·골든패스 실증으로 강제 종료
- **대응 이슈**: 14-wbs §2 Sprint 1 마지막 issue 마일스톤 + Sprint 2 마지막 issue

### RISK-02: 인증·시크릿 보안 결함

- **카테고리**: 보안
- **설명**: bcrypt 적용 누락, JWT secret 평문 commit, JWT 만료 검증 미적용 등 보안 결함이 머지될 가능성. 학습 컨텍스트라도 *보안 절대 규칙*(CLAUDE.md) 위반은 차단.
- **영향**: R-N-03·R-N-04 미충족 → DoD 미달. PR 단계 `/cso` BLOCK으로 머지 차단.
- **가능성**: 단위 테스트 + `/cso` + Pre-commit 훅이 3중 점검하므로 *낮음*. 단, *간과로 인한* 누락은 가능.
- **현재 상태**: 모니터링
- **트리거 신호**: `.env` 파일 staged / `git diff`에 평문 secret / JWT exp 검증 누락 / bcrypt 미적용
- **완화 전략**:
  - `.env*` PreToolUse 훅 Write 차단 (settings.json 정책 정본)
  - 매 PR `/cso` 보안 점검 자동 실행 + grep으로 secret 패턴 0건 확인
  - I-02·I-03 단위 테스트에서 bcrypt 마커(`$2b$`) + JWT exp 클레임 검증
- **대응 이슈**: I-02 (User 모델), I-03 (Auth 서비스), I-10 (보안 점검 + 회귀)

### RISK-03: SQLAlchemy 2.x async API 학습 부담

- **카테고리**: 기술
- **설명**: SQLAlchemy 2.x async API(`AsyncSession`, `select(...)` 2.x 스타일)는 비교적 신생 — 일부 학습 자료가 1.x 스타일이라 혼동 가능. Alembic + async 조합도 패턴 자료 부족.
- **영향**: I-01·I-03·I-04에서 구현 시간 초과 → RISK-01 가속.
- **가능성**: 학습 곡선 자체는 가파르지 않으나 *처음 만나는 패턴*에서 30분~1시간 막힘 발생 가능.
- **현재 상태**: 모니터링
- **트리거 신호**: 단위 테스트에서 `MissingGreenlet` 류 비동기 에러 / Alembic autogenerate 결과가 비어있음 / fixture에서 `await session.commit()` 누락 에러
- **완화 전략**:
  - I-01 진입 직전 SQLAlchemy 2.x async 공식 튜토리얼 30분 사전 학습 (작업 시간 외)
  - `conftest.py`에 AsyncSession fixture 1곳에 집중 작성 — 각 테스트는 fixture만 받음
  - 막힘 1시간 초과 시 `/investigate` 호출
- **대응 이슈**: I-01 (스캐폴딩), I-03 (Auth 서비스)

### RISK-04: F-04 UI 회귀 안전망 부재

- **카테고리**: 기술
- **설명**: F-04 UI는 단위·통합 테스트 N/A 결정 (v0.2). 회귀 안전망은 골든패스 E2E 1회뿐. 사소한 UI 회귀(버튼 disabled 누락, 폼 유효성 오류 안 보임 등)는 E2E 단일 시나리오로 잡히지 않음.
- **영향**: Sprint 2 후반에 회귀 발견 시 마감 시간 초과.
- **가능성**: 6 화면 동시 구현 + 짧은 시간 → *중간*.
- **현재 상태**: 모니터링
- **트리거 신호**: 골든패스 도중 단계 fail / 폼 에러 메시지 미노출 / 모바일 Chrome에서 레이아웃 깨짐
- **완화 전략**:
  - 골든패스 7단계(가입→로그인→글 작성→댓글 작성→댓글 수정→글 수정→글 삭제) 스크린샷 강제 — 단계별 PASS·FAIL 시각 확인
  - 13/02-catalog F-04 §E2E 정의된 시나리오 그대로 gstack `/qa`로 실행
  - Sprint 2 마지막 시점에 `/qa` 1회 + 수동 6 화면 보행 1회로 cross-check
- **대응 이슈**: I-09 (댓글 UI + 프로필 + 골든패스 E2E)

### RISK-05: 산출물 매몰 — 코드 < 문서

- **카테고리**: 운영
- **설명**: 사이클 완주 학습이 본 과제 목적이지만, 본 사이클의 산출 문서 14종 + ADR 4종 + WBS + Risk를 작성하느라 *실제 동작 코드*가 부족할 위험. 게이트별 산출은 BLOCK 통과 수준에서 멈추고 코드 작성 시간을 확보.
- **영향**: DoD §3 골든패스 미통과 → 사이클 완주 실패.
- **가능성**: 본 게이트 A·B·C 작성에 이미 ~1d 사용. Sprint 1·2 (10d effort)이 16h 안에 안 들어감 → 중간.
- **현재 상태**: 모니터링 (현재 게이트 C 산출 완료, 코드 작성 진입 전)
- **트리거 신호**: Sprint 1 종료(2026-05-21 오전)에 backend router 1개도 통합 테스트 미통과
- **완화 전략**:
  - 게이트 C 이후 문서 작성은 *PR description + change-contract*만 — 별 산출 14종 후속 갱신 안 함
  - Sprint 2 시작 시점에 backend 5개 라우트 통합 통과를 마일스톤으로
  - 어떤 산출이든 BLOCK 통과 수준에서 멈춤 (정량 KPI 표·서술 단락 추가 자제)
- **대응 이슈**: Sprint 1 마일스톤 (backend integration green), I-10 (회귀 + 최종 docs-update)

### RISK-06: gstack `/qa` 도구 가용성

- **카테고리**: 외부 의존
- **설명**: gstack `/qa` 골든패스 E2E는 DoD §3 + AI 게이트 5번째 축. gstack 자체가 외부 도구라서 환경 설정·브라우저 자동화 의존성이 사전 점검되지 않으면 Sprint 2 마지막에 fail 발견 시 마감 미달.
- **영향**: DoD §3 미충족 → 사이클 완주 실패.
- **가능성**: 사내 표준 도구지만 *처음 사용*이라 학습·환경 설정 부담. 중간.
- **현재 상태**: 식별
- **트리거 신호**: `/qa` 첫 실행 시 브라우저 부팅 실패 / chromedriver 버전 불일치 / playwright 설치 누락
- **완화 전략**:
  - Sprint 1 종료 시점에 `/qa` dry-run 1회 — http://example.com 같은 간단 사이트로 도구 환경 사전 점검 (작업 시간 외)
  - 막힘 시 `/help`로 fallback 또는 수동 6 화면 보행 + 수동 스크린샷 첨부 (스크린샷이 더 중요)
- **대응 이슈**: I-09 (골든패스 E2E)

### RISK-07: R-N-01·R-N-02 성능 미달

- **카테고리**: 기술
- **설명**: API p95 < 200ms (R-N-01) 또는 FCP < 1.5s (R-N-02) 미달 가능성. N+1 쿼리·번들 크기 등.
- **영향**: 비기능 요구사항 미달 → AI 게이트 통과 가능하나 산출 KPI 미달.
- **가능성**: SQLite + 100건 시드 + eager loading 사전 적용으로 *낮음*. 다만 측정 환경(로컬 머신 성능)에 따라 변동.
- **현재 상태**: 식별
- **트리거 신호**: I-08(시드 + p95 측정 테스트)에서 측정값 ≥ 200ms / gstack Performance 트레이스에서 FCP ≥ 1500ms
- **완화 전략**:
  - 사전 적용: `selectinload(Article.author)` + `articles.created_at` 인덱스 + Vite 기본 코드 스플리팅
  - 미달 시 빠른 fallback: 페이지네이션 limit 기본값 줄이기 (20 → 10), React.lazy로 페이지 chunk 분리
  - 본 학습 과제는 측정 결과 기록이 우선 — 측정값 미달이라도 *원인 파악 + 후속 ADR* 노트로 통과 가능
- **대응 이슈**: I-05 (Article repo + 인덱스), I-08 (시드 + 측정), I-09 (FCP 측정 E2E)

### RISK-08: 부팅 자산 동기 누락

- **카테고리**: 운영
- **설명**: 부팅 자산(LOCAL.md ↔ `12-scaffolding/python.md §7` ↔ 실제 `.env.example`·`alembic/versions/`·`uv.lock`)이 *같은 PR에서 동시 갱신*되어야 한다 (ADR-0037 v1.1 + ADR-0040). 단일 환경 운영이라 누락 가능성은 낮으나, fresh checkout 부팅이 깨지는 경우 사이클 완주 영향.
- **영향**: AI 게이트 6번째 축 BLOCK → PR 머지 차단.
- **가능성**: 단일 환경 운영 + 워크스페이스별 .env 분리로 *낮음*.
- **현재 상태**: 식별
- **트리거 신호**: fresh checkout 후 LOCAL.md §3 명령 실행 시 부팅 실패
- **완화 전략**:
  - 매 PR description에 "부팅 자산 변경 사항 1줄 요약" 강제 (변경 없으면 'N/A')
  - Sprint 2 마지막 PR에서 fresh checkout 시뮬레이션 1회 — git worktree로 별도 디렉토리에 clone 후 LOCAL.md §3 명령 그대로 실행
- **대응 이슈**: I-10 (회귀 + 최종 docs-update)

## 3. High 리스크 단계적 롤아웃

본 프로젝트는 *로컬 부팅만 필수*이며 클라우드 배포 Out of Scope이므로 *프로덕션 롤아웃 단계 자체가 없다*. 따라서 본 절은 "High 리스크 2건(RISK-01·02)에 대한 단계적 도입·검증 절차"로 재해석한다.

### 3.1 RISK-01 (일정) — 시간 박스 단계적 컷 (16h 마감 기준)

본 리스크는 *deadline pressure*. **2일 × 8h = 16h 순 작업 시간** 안에 ~10d effort(AI 페어 가속 환산 ~16h)를 압축. 시간이 *정확히* 맞아 떨어지므로 *결정 지연*이 가장 큰 위험. 다음 6 단계 결정 시점에서 *15분 timer*로 즉시 컷:

| 단계 | 결정 시점 | 조건 | 컷 액션 |
|---|---|---|---|
| 1 | Day 1, 16:30 | I-04(users + articles router) 통합 테스트 미완 | I-05(시드 + p95) 즉시 컷 → I-04 마무리에 시간 재배분. R-N-01 측정은 후속 학습 과제로 |
| 2 | Day 1, 18:00 (Sprint 1 종료) | backend 5 라우트 통합 미통과 | Day 2 09:00~09:30 backend 마무리 → I-09의 R-F-12 ProfilePage 컷 결정. `/qa` dry-run 컷 (Day 2 17:00 골든패스 본 실행에서 도구 첫 사용) |
| 3 | Day 2, 14:00 | I-08(인증 화면 + AuthStore) 미완 | I-09의 R-F-12 ProfilePage 컷 (헤더 [내 프로필] 메뉴 자체 미노출). I-09 시간 1h+ 확보 |
| 4 | Day 2, 16:00 | I-09의 댓글 작성·삭제 UI 미완 | 댓글 수정 UI(R-F-13의 FE) 컷 — backend API(PUT /api/articles/{slug}/comments/{id})는 유지. 14-wbs §4 추적성 유지 |
| 5 | Day 2, 17:00 | 골든패스 7단계 진입 못함 | 5단계로 압축 (가입 → 로그인 → 글 작성 → 댓글 작성 → 글 삭제). 댓글 수정·글 수정 단계 제외 |
| 6 | Day 2, 17:50 | I-10(보안 점검 + README + 머지) 미완 | PR description 간소화 (`/cso` 자동 보고서만 첨부) + `/retro`는 회고 메모로 대체. 강제 squash merge 우선 |

본 컷은 *기능 제거*이고, 14-wbs §4 추적성 매트릭스의 R-/F-ID 매핑은 그대로 유지. 미완 항목은 후속 사이클(`realworld-py-v2` 또는 PR 추가)에서 보강.

### 3.1.1 시간 박스 운영 원칙

- **결정 시점에 정확히** — 17:00이 되면 15분 안에 컷 결정. 지연 금지
- **AI 페어 가속이 깨지면 컷 가속** — 같은 막힘이 30분+ 지속되면 즉시 컷 후보 진행 (전체 진도 → 컷 진도 전환)
- **회고 메모 강제** — 컷 발생 시 `docs/planning/retro/2026-05-22-cycle.md`에 컷 사유 + 후속 과제 1줄. retro 자체 생략 시에도 GitHub PR description에라도

### 3.2 RISK-02 (보안) — 단계적 점검

보안 결함은 *조기 발견*이 핵심. 3 단계 점검:

| 단계 | 시점 | 액션 |
|---|---|---|
| 1 | I-02·I-03 PR 시점 | 단위 테스트로 bcrypt 마커(`$2b$`) 검증 + JWT exp 클레임 디코드 검증 |
| 2 | I-04 PR 시점 | `/cso` 보안 점검 1회 — `.env` staging 시도 / secret-like 패턴 grep / passlib·python-jose 취약 버전 점검 |
| 3 | Sprint 2 종료 시점 (I-10) | 전체 commit history grep 1회 — `JWT_SECRET=eyJ...` 류 평문 0건 확인. `/cso` 최종 보고서 PR description 첨부 |

이 단계 어디서든 결함 발견 시 *즉시 BLOCK*. 마이그레이션 + 강제 재로그인 패턴은 본 학습 과제 dev DB에선 *DB 파일 삭제 + 재시드*로 대체 가능.
