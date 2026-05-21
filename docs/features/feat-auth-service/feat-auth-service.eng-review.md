---
doc_type: feature-eng-review
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-21
gate: feature
related:
  R-ID: [R-F-01, R-F-02, R-F-03, R-N-03, R-N-04]
  F-ID: [F-01]
  supersedes: null
---

# feat-auth-service — Engineering Review

> P5 plan-eng-review. Brief + Contract + Plan 3종 검토. Verdict: PASS.

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-21 | woosung.ahn@bespinglobal.com | 초안 — 10 OX 모두 PASS, NEEDS-WORK 0건 |

## 0. Verdict

**PASS** — Contract Before/After 13행 + Call Sites 6행 + Plan 7 커밋 DAG 모두 적합. NEEDS-WORK 0건. P6 acceptance-criteria 진입 허용.

- [reviewer]: woosung.ahn@bespinglobal.com (AI)
- [review_at]: 2026-05-21

## 1. Contract 검토

- ✅ §0 Referenced-IDs 5행 모두 충족 — R-ID 5종 (R-F-01·R-F-02·R-F-03·R-N-03·R-N-04) + F-ID (F-01) + Module (08 §1·§3·§6) + Scaffolding (12 §1 utils/services/deps 폴더) + Conventions (11 §1·§2·§3)
- ✅ §2 Before/After 13행 — utils 3 (init/security/jwt) + errors / services 2 (init/auth) + UserRepo 확장 / deps 2 (init/auth) / db get_db_session / 단위 테스트 3 (security/jwt/auth_service) 모두 매핑
- ✅ §3 Call Sites 6행 — UserRepo / User 모델 / get_db_session / get_settings (기존 의존) + 후속 routers/users·articles (I-04 의존)
- ✅ §4 Backward Compatibility — neutral 명시 + UserRepo find_by_id 추가도 시그니처 변경 0이라 무영향 명시 + 의존성 0 신규 (passlib/python-jose 이미 I-01에 있음) + 환경변수 0 변경 (JWT_* 이미 I-01에 있음)
- ✅ §5 Rollback — revert PR + cascade revert (I-04와 묶임) + hotfix (config 값) 분기 명시
- ✅ §6 비목표 — 9개 항목 명시 (라우트·스키마·exception_handlers·작성자 권한·refresh token·OAuth·bcrypt round 튜닝·JWT 알고리즘·통합 테스트)

## 2. Plan 검토

- ✅ §1 7 커밋 DAG — 각 커밋 단일 책임 + critical path 명확 (C1→C2→C3→C4→C5→C6, C7 docs 병행). utils 2 모듈을 각각 별도 커밋으로 분리해 보안 단위 검증.
- ✅ §2 의존성 그래프 — errors → security → jwt → AuthService → require_auth 일방향. 시각화 완료
- ✅ §3 테스트 매핑 — 8 단위 테스트 시나리오 명시 (security 3 + jwt 3 + auth_service 8). R-N-03 bcrypt 마커 + R-N-04 JWT secret 검증 모두 포함. 기존 6건 회귀 무영향 명시
- ✅ §4 빌드·실행 검증 — C1~C6 단계별 + 전체 회귀 + ADR-0047 manual reproduction 5 step 모두 코드블록 명시
- ✅ §5 점진 합의 항목 6건 (JWT 만료 테스트 방식 / 헤더 prefix Token / DB 조회 비용 / errors 비HTTP / passlib warning / UserRepo find_by_id drift) — yagni 정책 + 후속 ADR 트리거 명시

## 3. UX 검토

**N/A** — backend-only. ui_changed=false. brief §5 영향 범위 표에서 "UI / FE: 영향 0" 명시.

## 4. 6단계 폴더링 충족

✅ ADR-0015 폴더 강제 충족:
- `docs/features/feat-auth-service/` 폴더 ✅
- `feat-auth-service.brief.md` + `.contract.md` + `.plan.md` 명명 정합 ✅ (`filename_pattern` 강제)
- 추가 산출 `.eng-review.md` (본 파일) + `.acceptance.md` + `.risk.md` 예정
- INDEX.md는 폴더 단위 자동 생성 대상 외 (feature 폴더는 산출 묶음 — ADR-0015 §2.2 예외)

## 5. frontmatter / Manifest 검증

✅ 3 산출 모두 `bash .claude/scripts/validate-doc.sh` PASS:
- `feat-auth-service.brief.md` — OK [feature-brief]
- `feat-auth-service.contract.md` — OK [feature-contract]
- `feat-auth-service.plan.md` — OK [feature-plan]

frontmatter 정합:
- doc_type: feature-{brief,contract,plan,eng-review,...} ✅ schema 28종 중 매핑
- version: v0.1 (Draft) ✅
- author: woosung.ahn@bespinglobal.com ✅ (이메일 형식)
- date: 2026-05-21 ✅
- gate: feature ✅
- related.R-ID: [R-F-01, R-F-02, R-F-03, R-N-03, R-N-04] ✅
- related.F-ID: [F-01] ✅

## 6. 발견 사항 (3축 OX)

| Q | 답 | 처리 |
| --- | --- | --- |
| Q1. Contract §0 5행이 selective read 진입점으로 정합한가 (ADR-0018) | ✅ | 5행이 R-ID/F-ID/Module/Scaffolding/Conventions 모두 커버. P4 plan이 본 표만 읽고 작성됨 |
| Q2. Before/After가 *측면 컬럼 + Before 컬럼 + After 컬럼* 3열 표인가 | ✅ | 13행 모두 3열 충족 |
| Q3. Call Sites가 *위치 + 영향 + 조치* 3열인가 | ✅ | 6행 모두 충족 |
| Q4. Plan 커밋 DAG가 단방향 acyclic인가 | ✅ | C1→C2→C3→C4→C5→C6 + C7 docs 병행. 순환 없음 |
| Q5. 각 커밋 메시지가 ADR-0021 정규식 `^(feat\|fix\|chore\|docs\|test\|refactor)\([a-z][a-z0-9,_-]*\): .+` 충족하는가 | ✅ | feat(backend) / test(backend) / docs(feat) 모두 정합 |
| Q6. 테스트 추가 ≥ 1건인가 (기능 추가 PR 강제 — CLAUDE.md 필수 규칙 #5) | ✅ | 14건 추가 (security 3 + jwt 3 + auth_service 8) |
| Q7. SRS R-ID 매핑이 명확한가 | ✅ | R-F-01 (register) + R-F-02 (authenticate) + R-F-03 (get_current_user) + R-N-03 (bcrypt 마커 검증) + R-N-04 (JWT secret env) — frontmatter + brief + contract 모두 일치 |
| Q8. 코딩 컨벤션 (11 §1·§2·§3) 위반 없는가 | ✅ | 함수 snake_case (hash_password, verify_password, encode_token, decode_token) / 서비스 PascalCase (AuthService) / 예외 PascalCase (DuplicateEmail, InvalidToken) 모두 contract §1·§2 명시 |
| Q9. dev/stg/prod 3 profile 부팅 자산 영향이 있는가 | ✅ N/A | 본 PR 부팅 자산 변경 0 (.env.example/LOCAL.md/uv.lock/alembic 모두 무변경). RFP §NFR-06 단일 환경 운영 N/A. 사유 명시 |
| Q10. Rollback 전략이 alembic downgrade 또는 revert를 명시하는가 | ✅ | §5 1차/2차/hotfix/Trigger 모두 명시. revert PR + cascade (I-04와 묶임) |

**3축 OX 결과**: 10/10 PASS.

## 7. NEEDS-WORK 항목

(없음) — Verdict PASS. P6 진입 허용.
