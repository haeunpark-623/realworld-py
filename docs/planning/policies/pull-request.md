# PR 정책 — 양식 · 사용자 책임 · 미체크 강제 · 4 위치 책임 분리

> **위치**: `docs/planning/policies/pull-request.md`
> **상위 결정**: ADR-0046 (PR 정책 정본 신설), ADR-0044 (브랜치 전략 — 머지 전략·branch protection), ADR-0021 (이슈/PR 제목 — Conventional Commits), ADR-0001 (D-06 2단 게이트), ADR-0011·0037·0038 (AI 게이트 6축), ADR-0010 (Schema-level Document Enforcement).
> **관련 정책**: [`branch-strategy.md`](branch-strategy.md), [`sprint-cycle.md`](sprint-cycle.md), [`github-issue.md`](github-issue.md).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v1.1 | 2026-05-19 | yongtae.cho@bespinglobal.com | §4.5 신설 (ADR-0047) — **매 PR GitHub Actions 워크플로 양축 검증**. workflow가 매 PR 자동 트리거되는 구조(`pull_request.opened`/`edited`/`synchronize` 이벤트)에서 *workflow YAML 미변경 PR*에서도 PR body/title이 workflow 검증 룰 미충족 시 status check FAIL → 머지 차단 위험 차단. 로컬(act/manual reproduction/dev fork 실 실행 중 1택) + GitHub Actions runner 후행 실행 양축. 증거 = `### Manual verification` 통합 미체크 1줄 — `- [ ] GitHub Actions 워크플로 로컬 검증 (act 또는 manual): <명령> → <결과/사유>`. ADR-0046 §4 `manual_checkbox_must_be_unchecked` BLOCK에 자연 흡수 (별 schema 신설 없음). N/A 케이스(`.github/workflows/` 부재·PR 트리거 워크플로 0개·외부 의존 장애)는 사유 명시. §7 cross-ref에 ADR-0047 행 추가. |
| v1.0 | 2026-05-19 | yongtae.cho@bespinglobal.com | 초안 — ADR-0046 정합. PR 정책 4곳 분산(`branch-strategy.md` 머지 전략 / `pull_request_template.md` 양식 / `qa-test.md` Test Plan 생성 / `sprint-cycle.md` D-06 게이트) 상태를 정본 1파일로 흡수. 8 절 구조 — §1 양식·§2 머지 전략·§3 사용자 책임 경계·§4 자율실행 시 미체크 강제·§5 4 위치 책임 분리·§6 적용 범위·§7 cross-ref·§8 변경 절차. **§3 사용자 책임 3단** — Manual ✅ / DoD ✅ / Approve+머지. `tested` 라벨 부착 자체가 폐지(라벨 표식 없음)되어 머지 게이트는 §3.2 status check `pr-body-checkboxes`가 자동 발행. **§4 자율실행 미체크 강제** — `manual_checkbox_must_be_unchecked` schema BLOCK + validate-doc.sh §5f 분기. **§5 4 위치 책임 분리** — commit subject / commit body / PR body / PR comment 각각 영속성·작성 책임. agent-toolkit 자체(dogfooding) + newProject install.sh 카피 양쪽 적용. |

---

> **본 정책은 agent-toolkit이 사용자(도입 팀)에게 제공할 PR 운영의 표준 형태**다. 본 프로젝트(agent-toolkit) 자체 개발도 동일 모델을 따른다(dogfooding).
>
> newProject 도입자가 가장 먼저 읽어야 할 자리는 본 정책 + `.github/pull_request_template.md` + `.claude/commands/qa-test.md` 3곳. **본 파일은 *원칙·정본*, 템플릿은 *양식*, qa-test.md는 *집행*이다**.

## 1. PR 양식 (`.github/pull_request_template.md`)

PR 본문은 다음 4블록 + 머지 게이트 안내로 구성된다 ([`.github/pull_request_template.md`](../../../.github/pull_request_template.md) 정본):

```markdown
## Summary
<1~3 bullet — 무엇을 왜 바꿨는지>

Closes #<issue number>

---

## Test Plan (D-06 강제)

### Build
- [ ] <build cmd> (output: ...)              ← 자동 (LLM 채움)

### Automated tests
- [ ] <test cmd> — N passed, 0 failed         ← 자동 (LLM 채움)

### Manual verification
- [ ] {{acceptance Functional 항목}}           ← 사람 (반드시 미체크로 직렬화)
- [ ] {{acceptance UX 항목}}                    ← 사람 (반드시 미체크로 직렬화)
- [ ] {{회귀 시나리오}}                          ← 사람 (반드시 미체크로 직렬화)

### DoD coverage
| Acceptance | PR diff | 검증 |
|---|---|---|
| ... | ... | ... |

---

## Touched Areas (멀티 모듈 — 영역 3개 이상은 강제, ADR-0021 §2.2)

---

## 머지 게이트 안내 (휴먼 게이트, branch protection)
- [ ] PR 제목 Conventional Commits 형식 (issue-pr-title-lint)
- [ ] 자동 CI green
- [ ] Approve 리뷰 ≥ 1
- [ ] `tested` 라벨 부착 (사람이 로컬 빌드 + 재현 후 부착)
```

본 양식은 `.github/pull_request_template.md` 정본 미러. 본 정책 §1과 템플릿이 충돌하면 **템플릿이 정본**(GitHub UI가 직접 카피).

## 2. 머지 전략

[`branch-strategy.md`](branch-strategy.md) §4 정본 인용 — 다음 3옵션:

| 옵션 | 정책 | 사용 시점 |
|---|---|---|
| **Squash and merge** | ✅ **권장 기본** | 모든 일반 PR. 이슈 1개 = main 커밋 1개 1:1 매핑 |
| **Create a merge commit** | ⚠️ 예외 허용 | 다단계 마이그레이션·ADR 분할 발행 등. PR 본문에 보존 사유 명시 |
| **Rebase and merge** | ❌ **금지** | silent rewriting 위험 + ADR-0025 ff-only 정합 위배 |

GitHub repo 설정: Allow squash merging **ON** / Allow merge commits **ON** / Allow rebase merging **OFF** / Default = "Squash and merge". 상세는 branch-strategy.md §4.1·§5(branch protection 9개 규칙).

## 3. 사용자 책임 경계 (3단)

> **사람은 다음 3가지만 한다. 그 외 모든 작업은 LLM 또는 워크플로 책임.**

| # | 동작 | 위치 | 검증 |
|---|---|---|---|
| 1 | 로컬 빌드 + 재현 + **Manual verification** 체크박스 ✅ | PR body §"### Manual verification" | 사람이 직접 체크박스 클릭 |
| 2 | **DoD coverage** 표 검토 → 통과 항목 명시 ✅ | PR body §"### DoD coverage" | 사람이 표 마지막 컬럼 ✅ |
| 3 | **Approve 리뷰 + Squash 머지 클릭** | PR review + merge 버튼 | 사람 |

**LLM 또는 워크플로가 하는 일** (사람이 *하지 않는다*):
- **머지 게이트 검증** → §3.2 GitHub Actions가 status check `pr-body-checkboxes` 자동 발행 (ADR-0046 §2.5)
- PR body 작성·재작성 → LLM
- commit subject·commit body 작성 → LLM
- Build·Automated tests 자동 실행 및 결과 채움 → LLM
- 변경 요청 수신 시 추가 커밋 + push → LLM
- 충돌 해소·테스트 fix → LLM
- 머지 후 cleanup(브랜치 삭제 등) → 자동 또는 LLM

> **사용자가 PR body를 *직접 편집하지 않는다*는 원칙**. 사람이 본문을 손대야 하는 상황은 LLM 산출 자체의 갭 — 발견 시 회귀 시그널이며 별 ADR 격상 후보(open-items.md).

> **`tested` 라벨 자체 부재** — 라벨이라는 중간 표식 없이 *체크박스 상태 자체*가 status check를 통해 머지 게이트로 직결. 라벨 부착·삭제 동작 0건.

### 3.1 사람 머지 절차

1. PR body §"### Manual verification" 항목별 로컬 재현 → 체크박스 ✅ 클릭
2. PR body §"### DoD coverage" 표 검토 → 통과 항목 마지막 컬럼 ✅
3. (자동) §3.2 워크플로가 체크박스 카운트 → status check `pr-body-checkboxes` PASS 발행
4. Approve 리뷰 작성 (변경 요청 없으면)
5. Squash 머지 클릭 (branch protection의 Required status checks 통과 후)

### 3.2 PR body checkbox status check 메커니즘

머지 게이트 검증은 **GitHub Actions가 status check를 직접 발행**. 라벨이라는 중간 표식 없이 *체크박스 상태 자체*가 머지 게이트.

| 항목 | 값 |
|---|---|
| 워크플로 파일 | `.github/workflows/pr-body-checkbox-gate.yml` (ADR-0046 §2.5) |
| 이벤트 | `pull_request.edited` (체크박스 클릭) + `pull_request.opened` + `pull_request.synchronize` |
| 발동 조건 | 매 이벤트마다 — `### Manual verification` + `### DoD coverage` 안 `- [ ]` 갯수 카운트 |
| status check context | `pr-body-checkboxes` |
| PASS 조건 | 미체크 갯수 == 0 |
| FAIL 조건 | 미체크 갯수 > 0 (description에 잔존 갯수 명시) |
| branch protection 등록 | Required status checks 목록에 `pr-body-checkboxes` (ADR-0044 §5.1) |

**자율실행(`/goal`·`/orchestrate`·`/flow-feature` P10) 정합**:
- LLM이 PR open → 모든 체크박스 *미체크* 상태(§4 BLOCK + ADR-0046 §2.3 + schema `manual_checkbox_must_be_unchecked`)
- 워크플로가 `opened` 이벤트 수신 → 미체크 > 0 → status check FAIL
- 사람이 로컬 재현 후 체크박스 클릭 → `edited` 이벤트 → 워크플로 재발동 → 미체크 0 → status check PASS
- branch protection이 status check FAIL 시 머지 차단 → 사람 검증 누락 PR은 머지 불가

> **사람은 status check를 *수동 override하지 않는다*** — admin bypass 또는 status check 강제 PASS 우회 금지. 만약 워크플로 미발동 시(이벤트 누락·파싱 오류) 별 PR로 워크플로 디버깅 — 사람이 *수동 우회로 머지*하지 않음(원칙 유지).

## 4. 자율실행 시 미체크 강제 (Schema BLOCK)

`/goal`·`/orchestrate` 등 LLM 자율 실행 또는 단일 `/qa-test --ai` 모두 동일 적용.

> **PR open 직후 정상 상태 = Manual verification·DoD coverage 모든 체크박스 `- [ ]`**. LLM은 PR body에 *체크박스 자체*는 박지만 ✅ 클릭은 *절대 하지 않는다*. 사람이 로컬 재현 후 직접 클릭하기 전까지 체크박스는 비어 있는 상태 유지 — 이 상태에서는 §3.2 status check가 FAIL을 발행하므로 머지 차단.

**규칙**:
- `## 1. Test Plan 4블록` 안의 `### Manual verification` 체크박스는 **항상 `- [ ]` (미체크)**로 직렬화
- `### DoD coverage` 표 안 체크박스도 동일 규칙(표 안 체크박스 변형 발견 시 BLOCK)
- `### Build` / `### Automated tests`는 자동 결과 — `- [x]` 허용(LLM이 자동 실행 후 결과 채움)

**Schema 강제** ([`feature-ai-qa.schema.yaml`](../../../.claude/schemas/feature-ai-qa.schema.yaml) `manual_checkbox_must_be_unchecked`):

```yaml
manual_checkbox_must_be_unchecked:
  in_section: "## 1. Test Plan 4블록"
  applies_to_subsections:
    - "### Manual verification"
    - "### DoD coverage"
  forbidden_pattern: '^[[:space:]]*-[[:space:]]*\[[xX]\]'
  severity: BLOCK
  description: "ADR-0046 §4 — 사람이 검증할 항목은 항상 미체크(`- [ ]`)로 직렬화. /goal 자율 실행에서도 동일 강제."
```

`validate-doc.sh`가 본 룰을 자동 강제. LLM이 *친절하게* 사전 체크하면 BLOCK → PR 생성 차단.

> **자동 ↔ 사람 책임의 구조적 분리**: Test Plan 4블록은 schema-level로 4 subsection으로 강제 분리(ADR-0011 + 본 정책). 자동 항목(Build·Automated tests)은 LLM이 실행 후 결과 채움, 사람 항목(Manual verification·DoD coverage)은 LLM이 시나리오만 박고 *항상 미체크* — 사람이 로컬 재현 후 직접 체크.

### 4.5 매 PR GitHub Actions workflow 양축 검증 (ADR-0047)

**매 PR**은 **로컬 + GitHub** 양축으로 GitHub Actions 워크플로를 검증한다 — workflow YAML 변경 여부와 무관. workflow가 매 PR마다 자동 트리거되는 구조(`pull_request.opened`/`edited`/`synchronize` 이벤트)이므로 *workflow 미변경 PR*에서도 PR body/title이 workflow 검증 룰 미충족 시 status check FAIL → 머지 차단 시나리오가 발생할 수 있어, PR 작성자가 사전 검증으로 차단한다.

**적용 트리거 — 전 PR**:

- workflow YAML 변경 PR이든 미변경 PR이든 동일 적용
- workflow YAML *변경* PR은 추가로 *workflow 자체의 syntax/논리 검증*까지 포함(증거 1줄 본문에 변경 파일명 명시로 범위 추적)

**N/A 조건 (사유 명시 허용)**:

- repo의 `.github/workflows/` 디렉토리 자체가 없음 (workflow 0개)
- PR 이벤트 트리거 워크플로가 0개 (`push`/`schedule` 전용 워크플로만 있는 repo)
- 외부 의존(docker engine·dev fork 권한) 부재로 사전 실행 불가 시 사용자 *명시적 승인* 후 skip — 자동 skip 금지

**양축 정의**:

| 축 | 시점 | 도구 | 증거 |
|---|---|---|---|
| 로컬 (선행) | `gh pr create` 호출 전 | `act`(nektos/act) 권장 / manual reproduction 허용 / dev fork 실 실행 (act 미지원 기능) | PR body `### Manual verification`에 명령 + 결과 미체크 1줄 (통합 형식) |
| GitHub (후행) | `pull_request.opened`/`synchronize` | GitHub Actions runner | 기존 status check (`pr-body-checkboxes`·`pr-title-lint`·기타) PASS |

**증거 형식 — 통합 1줄 (Manual verification 항목)**:

```markdown
### Manual verification

- [ ] GitHub Actions 워크플로 로컬 검증 (act 또는 manual): `<실행 명령>` → <PASS/FAIL/skip 사유>
- [ ] (기존 휴먼 검증 항목들...)
```

- 매 PR 1줄 (workflow YAML 미변경 PR도 동일)
- workflow YAML *변경* PR은 본문에 변경 파일명 명시 — 예: `로컬 검증 (act, .github/workflows/pr-body-checkbox-gate.yml 수정): act pull_request -W ... → PASS`
- N/A 케이스 사유 명시 — 예: `로컬 검증: N/A (.github/workflows/ 디렉토리 부재)` 또는 `N/A (push 전용 워크플로만 존재)`

본 항목은 §4 `manual_checkbox_must_be_unchecked` BLOCK에 자연 흡수 — LLM은 항상 미체크 직렬화, 사람이 로컬 재현 후 ✅ 클릭. 별 schema 룰 신설 없음.

**도구 선택 (PR 작성자 재량)**:

1. **`act`** — Docker 기반 GitHub Actions 에뮬레이터. 충실한 재현. 예: `act pull_request -W .github/workflows/<file>.{yml,yaml} -s GITHUB_TOKEN="$(gh auth token)"`
2. **manual reproduction** — workflow의 핵심 step을 bash로 직접 실행. 현 toolkit 3 workflow처럼 `gh api`·`gh pr view` 호출이 본체인 경우 더 빠름 — 예: `gh pr view <N> --json body --jq '.body' | awk '...'`로 `pr-body-checkbox-gate.yml` 시뮬레이션
3. **dev fork branch 실 실행** — `act` 미지원 기능 (self-hosted runners·OIDC `id-token: write`·GitHub-hosted secrets·reusable workflow `secrets: inherit` 일부·matrix 동시성) 사용 시. dev fork에 푸시 → Actions 결과 확인 → 본 branch로 cherry-pick

**예외**: act 미지원 기능 사용 workflow는 manual reproduction 또는 dev fork 실 실행으로 대체 허용 — Manual verification 항목 본문에 사유 명시 의무.

## 5. 4 위치 책임 분리 (commit subject · commit body · PR body · PR comment)

같은 PR이라도 정보가 살아 남는 *영속성*과 *발견 가능성*이 위치마다 다르다. 4 위치 각각에 무엇을 담을지 명확히 분리.

### 5.1 위치 정의

| 위치 | 어디 보임 | 영속성 | 담는 내용 |
|---|---|---|---|
| **commit subject** | squash 머지 후 main `git log --oneline` 첫 줄 | **영구 (main log)** | `<type>(<scope>): <summary> (#<N>)` (ADR-0021 §1.5 정규식) |
| **commit body** | squash 머지 후 `git show <commit>` body (squash 화면의 commit extended description) | **영구 (main log)** | `Closes #N` + Acceptance 매핑(R-ID/F-ID) + breaking change 노트 + 부팅 자산 변경 메모 |
| **PR body** | GitHub PR 본문 (lifecycle view) | PR 한정 (머지 시점에 commit body로 일부 흡수) | Test Plan 4블록 + AI 게이트 6축 결과 + 스크린샷 링크 + 부팅 결과 + 발견 사항 |
| **PR comment** | PR comment 영역 (시계열 누적) | PR 한정 | 변경 요청 · 발견 사항 추가 · 머지 사유 (특이사항 있을 때만) |

### 5.2 작성 책임

| 위치 | 작성 | 기준 |
|---|---|---|
| commit subject | LLM | PR 제목 그대로 사용 (squash 기본 동작, ADR-0044 §4.2) |
| commit body | LLM | PR body의 *영구 보존 부분*만 추려서 작성 — `Closes #N` + R-ID/F-ID + breaking 노트 + 부팅 자산 변경 메모 |
| PR body | LLM | `/qa-test --ai` 산출 `<slug>.ai-qa-report.md` 통째로 박음 (qa-test.md 단계 10) |
| PR comment | 사람(변경 요청·머지 사유) + LLM(자동 응답·회귀 결과) | 휴먼 게이트 의사소통. `tested` 라벨 폐지(§3.2)로 라벨 부착 사유 코멘트 없음 |

### 5.3 commit subject + commit body 예시 (영구 main history 기록)

```
feat(auth): JWT 토큰 갱신 엔드포인트 추가 (#42)              ← commit subject

Closes #42                                                    ← commit body
                                                              ← commit body
Acceptance:                                                   ← commit body
- R-AUTH-01 (토큰 갱신 5분 단위)                              ← commit body
- R-AUTH-02 (만료된 refresh token 거부)                       ← commit body
                                                              ← commit body
Breaking: 없음                                                ← commit body
부팅 자산: .env.dev.example +1 (JWT_REFRESH_TTL)              ← commit body
```

**1년 후 `git blame src/auth/refresh.ts` 추적 시** 이 commit으로 점프하면 *왜 바꿨나·어떤 R-ID인가·breaking 여부·env 변경 여부*가 즉시 보인다 — PR로 점프할 필요 없음.

### 5.4 PR body (lifecycle view)

`/qa-test --ai`가 `<slug>.ai-qa-report.md` 산출 후 `gh pr create --body "$(cat ...)"` 호출. PR body는 **머지 가능성 근거** — Test Plan 4블록 + AI 게이트 6축 + 발견 사항.

PR body는 머지 시점에 *일부*가 commit body로 흡수됨(GitHub squash 머지 기본 동작 — PR 본문 → commit body). LLM은 PR body 작성 시 *commit body로 흡수될 부분*을 의식적으로 분리한다(`## 0. Verdict` 직후 `## (commit body 권장 보존 블록)` subsection에 `Closes #N` + Acceptance + Breaking + 부팅 자산 4 항목 박는다 — qa-test.md 단계 10 절차).

### 5.5 PR comment (휴먼 게이트 의사소통)

- **변경 요청** (사람): `gh pr review <N> --request-changes --body "발견 사항: ... (파일:라인 + 재현 절차)"`
- **회귀 결과** (LLM): 변경 요청 수신 후 추가 커밋 push + `gh pr comment <N> --body "<P10-qa-ai 회귀 결과>"`
- **머지 사유** (사람, 특이사항 있을 때만): `gh pr comment <N> --body "외부 의존 stg 컨테이너 장애로 stg profile skip — ADR-0037 §예외 적용"`

> `tested` 라벨 자체 폐지(§3.2)로 라벨 부착 사유 코멘트 항목 없음. 머지 게이트 상태(PASS/FAIL)는 status check `pr-body-checkboxes` 워크플로 로그(`gh run view`)에서 추적 — PR comment 작성 없음.

PR comment는 **휴먼 게이트의 누적 기록**. PR close 후에도 GitHub UI에서 볼 수 있지만 main history에는 안 박힘 — 영구 보존 필요 정보는 commit body로 끌어올린다.

## 6. 적용 범위·예외

### 6.1 적용

- **agent-toolkit 자체**(dogfooding) — 본 정책 즉시 적용
- **newProject 전수** — `scripts/install.sh`가 `docs/planning/policies/branch-strategy.md`를 카피하는 동일 패턴(ADR-0044 v1.1)으로 본 파일도 카피. install.sh는 ADR-0044 v1.1 이후 정책 정본 추가마다 카피 블록 1행 추가 — 또는 `policies/` 폴더 전체 rsync 격상(별 PR/ADR).
- newProject가 임의 수정하지 않는다 — 정책 변경은 agent-toolkit 측 amend 후 install 재실행으로 흘러 들어옴(branch-strategy.md와 동일 정책).

### 6.2 예외

| 예외 | 허용 조건 |
|---|---|
| docs-only PR (정책 문서·README·CHANGELOG 단독) | `chore/<purpose>-<YYYYMMDD>` 브랜치 허용(branch-strategy.md §2.2). Test Plan §### Manual verification은 *N/A 명시* 허용 |
| 부트스트랩 PR (`/flow-bootstrap`) | `chore/planning-bootstrap-<YYYYMMDD>` 자동 분기. Test Plan 4블록 자체 N/A |
| 외부 의존 장애로 부팅 검증 불가 | ADR-0037 §예외 — 사용자 승인 후 명시적 skip + PR comment에 사유 명시 |
| 단일 환경 운영 (stg=prod 공유) | ADR-0037 v1.1 — N/A + 사유 명시 |

## 7. Cross-ref

| 자산 | 본 정책과의 관계 |
|---|---|
| [`.github/pull_request_template.md`](../../../.github/pull_request_template.md) | §1 PR 양식 정본(템플릿) — 본 정책 §1이 인용 |
| [`branch-strategy.md`](branch-strategy.md) §4 머지 전략 + §5 branch protection | §2 머지 전략 정본 — 본 정책이 인용 |
| [`sprint-cycle.md`](sprint-cycle.md) §2 D-06 게이트 | §3 사용자 책임 경계 + §4 미체크 강제의 *상위 결정* (휴먼 게이트 = 사람 책임) |
| [`github-issue.md`](github-issue.md) §1.5 이슈/PR 제목 + §5 파생 이슈 | §5.1 commit subject 형식의 원천 |
| [`.claude/commands/qa-test.md`](../../../.claude/commands/qa-test.md) | Test Plan 4블록 생성 + `gh pr create` 호출 — 본 정책 §1·§4 집행 정본 |
| [`.claude/schemas/feature-ai-qa.schema.yaml`](../../../.claude/schemas/feature-ai-qa.schema.yaml) | §4 미체크 강제 BLOCK 룰 (`manual_checkbox_must_be_unchecked`) 정본 |
| [`adr/0046-pull-request-policy.md`](../adr/0046-pull-request-policy.md) | 본 정책 신설 결정 ADR |
| [`adr/0047-workflow-local-verification.md`](../adr/0047-workflow-local-verification.md) | §4.5 workflow 변경 PR 양축 검증 결정 ADR |
| [`adr/0044-branch-strategy.md`](../adr/0044-branch-strategy.md) | §2 머지 전략의 원천 ADR |
| [`adr/0021-issue-naming-and-origin.md`](../adr/0021-issue-naming-and-origin.md) | §5.1 commit subject 형식의 원천 ADR |
| [`adr/0001-test-gate-ai-and-human.md`](../adr/0001-test-gate-ai-and-human.md) | §3·§4의 D-06 2단 게이트 정의 원천 ADR |
| [`adr/0011-ai-gate-browser-verification.md`](../adr/0011-ai-gate-browser-verification.md) · [`0037-pr-local-runnability.md`](../adr/0037-pr-local-runnability.md) · [`0038-design-system-enforcement.md`](../adr/0038-design-system-enforcement.md) | AI 게이트 6축 (자동) — 본 정책 §3·§4가 *사람 책임* 영역과 책임 분리 |
| [`.github/workflows/pr-body-checkbox-gate.yml`](../../../.github/workflows/pr-body-checkbox-gate.yml) | §3.2 status check 발행 워크플로 — PR body 체크박스 카운트 → `pr-body-checkboxes` PASS/FAIL |
| `CLAUDE.md` §"GitHub 이슈·스프린트 정책" | agent-toolkit 자체용 정본 포인터 |

## 8. 변경 절차

본 정책의 §1~§5 변경은 **ADR 발행 필수**(`docs/planning/adr/NNNN-*.md`). §6 예외 확장·§7 cross-ref 추가·오탈자 수정은 본 파일 변경 이력 표 갱신만으로 처리.

변경 영향 점검 체크리스트:
- [ ] §1 양식 변경 시 — `.github/pull_request_template.md` 동기 + `qa-test.md` Test Plan 4블록 schema 정합 확인
- [ ] §2 머지 전략 변경 시 — branch-strategy.md §4·§5 동시 갱신 필수 (본 정책은 인용만)
- [ ] §3 사용자 책임 경계 변경 시 — sprint-cycle.md §2 D-06 게이트 정의 동기 확인
- [ ] §4 미체크 강제 변경 시 — `feature-ai-qa.schema.yaml` `manual_checkbox_must_be_unchecked` 룰 + `validate-doc.sh` 분기 동기 확인
- [ ] §5 3 레이어 책임 분리 변경 시 — `qa-test.md` 단계 10 (gh pr create 호출) + ADR-0021 §1.5 commit 형식 정합 확인
