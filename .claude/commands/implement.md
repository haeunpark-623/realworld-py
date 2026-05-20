---
description: Use this when the user is about to write code, asks to start implementing a task, needs to translate a plan into commits, or is about to begin coding after all design gates have passed.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# /implement

## 목적
`change-contract` + `implementation-planner` + `acceptance-criteria` + `/plan-eng-review` PASS를 모두 충족한 상태에서 **코드를 작성**. 본 단계 이전의 게이트 누락 시 진입 거부.

## 사용 시점
- 모든 게이트 통과 직후
- 단일 이슈 작업 (1~3 working days 범위)

## 진입 전 체크리스트 (모두 ✅ 필요)

### 모드 무관 (전역)
```
[ ] <slug>.contract.md 존재
[ ] <slug>.plan.md 존재
[ ] <slug>.acceptance.md 존재
[ ] <slug>.eng-review.md 가 PASS
[ ] <slug>.risk.md High 리스크 모두 완화
[ ] git branch가 작업 단위로 분기됨
```

### mode=sprint 추가 체크
```
[ ] GitHub Issue가 status:in-progress (본인 assigned)
[ ] Blocked-by 모두 closed
[ ] 브랜치가 작업 단위로 분기됨 (미분기 시 본 Command가 main 최신화 후 base=최신 origin/main에서 자동 분기 — ADR-0025)
[ ] 브랜치명이 <mode>/<slug>-issue-<N> 패턴 (mode 접두: feat / mod / bug / design)
```

### mode=planning
```
* 이슈/라벨 검증 skip
* 브랜치 자유 (또는 main 직접 작업도 허용 — docs-only 변경 시)
```

## 입력
- 위 4종 산출물
- 작업 브랜치

## 산출물
- 코드 변경 (커밋 단위로)
- 단위 테스트 (plan에 매핑된)
- 빌드 통과 증거

## 실행 단계
1. 진입 체크리스트 검증 → 미충족 시 BLOCKED + 회귀할 Phase 안내
1a. **`Blocked-by:` 본문 검사** — [`issue-claim`](../skills/devtoolkit/issue-claim/SKILL.md) Skill 호출. 미해소 시 `status:blocked` 자동 부착 + 진입 거부 (policies/github-issue.md §3 규칙 #1·#2, ADR-0022)
2. plan의 Subtask 순서대로 구현
3. 각 Subtask마다:
   - 코드 작성
   - 단위 테스트 작성·실행
   - 커밋 (커밋 메시지에 이슈 번호 포함)
4. 빌드 명령 실행 — `docs/planning/12-scaffolding/12-scaffolding.md` §5 (SoT) 또는 newProject 루트 `LOCAL.md` §3(유저 facing)이 안내하는 **native script 직호출** (ADR-0041). 예: `pnpm build` · `./gradlew build` · `uv run pytest` 등. multi-module은 빌드 도구 native syntax(`pnpm -r build` · `./gradlew :backend:build` 등) 사용. 12-scaffolding §5 미작성·LOCAL.md §3 stale 시 BLOCKED — 본 단계 진입 전 `/flow-design` Gate C / 매 PR LOCAL.md 동기(ADR-0040) 완료 확인. (이전 ADR-0028 `./devkit` wrapper + ADR-0027 3-fallback lookup은 ADR-0041로 폐기.)
5. 자가 평가 금지 — `/code-review`로 위임

## 완료 조건
- 모든 Subtask 커밋됨
- 단위 테스트 100% 통과
- 빌드 green
- acceptance.md의 Functional 항목 셀프체크 ≥ 모두 ✅
- **UI/FE 변경 Subtask는 dev 서버 + 브라우저로 골든패스 1회 이상 실증 (ADR-0011)** — 스크린샷을 `docs/features/<slug>/screenshots/<screen>.png`에 저장. tsc/vitest/build 통과는 "컴파일 가능" 의미일 뿐 "사용자에게 동작" 의미가 아님.
- (단, 휴먼 재현 테스트는 `/qa-test --human` + 사람의 PR 검증으로 별도 진행)

## Strict Rules (CLAUDE.md 계승)
- **plan에 없는 작업 금지** — 발견 시 plan 회귀
- **테스트 없이 완료 금지** (CLAUDE.md 필수 규칙)
- **UI/FE 변경 시 브라우저 검증 없이 완료 금지** (CLAUDE.md 필수 규칙 9 + ADR-0011) — 빌드 통과는 검증이 아님
- **매 PR GitHub Actions 워크플로 로컬 검증 없이 PR 진입 금지** (CLAUDE.md 필수 규칙 13 + ADR-0047) — workflow가 매 PR 자동 트리거되는 구조라 *workflow YAML 미변경 PR*도 PR body/title 미충족 시 status check FAIL 위험. `/qa-test --ai` 단계 6b가 act/manual reproduction/dev fork 실 실행 결과를 Manual verification에 통합 1줄로 직렬화해야 함. N/A 케이스(workflows/ 디렉토리 부재·PR 트리거 워크플로 0개)는 사유 명시 후 통과. 정본 — [`docs/planning/policies/pull-request.md`](../../docs/planning/policies/pull-request.md) §4.5
- **코딩 컨벤션 위반 금지** (`docs/design/code-conventions.md`)
- **보안 파일 Write/Edit 금지** (settings.json PreToolUse 훅이 차단)
- **자기 평가 금지** (Generator≠Evaluator) — 본 Command가 PASS 판정을 자체 부여 X

## FSM 전이
- **mode=sprint** (ADR-0029 — FSM 전이 자동화, ADR-0048 — P-1 시점 앞당김):
  - **진입 시 (P-1에서 이미 호출됐으면 멱등 skip, ADR-0048)**: `issue-claim` Skill 호출 전 `gh issue view #N --json labels`로 검사 → `status:in-progress` 이미 부착 + assignee 본인이면 **skip**(중복 호출 방지, 멱등). 그 외(P-1 미통과 케이스 = mode=planning에서 사용자가 직접 #N 지정·`/implement` 사용자 직호출 등)는 `issue-claim` 신규 호출: `gh issue edit #N --add-label "status:in-progress" --remove-label "status:todo" --remove-label "status:blocked" --add-assignee @me`
  - 종료 시: PR 생성으로 `status:in-review` 전이 — `.github/workflows/sync-issue-labels.yml`이 PR `opened`/`ready_for_review` 이벤트에서 자동 (PR body `Closes #N` 파싱)
  - 머지 시: `status:*` 일괄 제거 (`tested` 보존) — 동 워크플로 `closed && merged==true` 이벤트에서 자동
- **mode=planning**:
  - 진입 시: `flow-state.current_phase = P8-implement` 만 갱신 (이슈 없음, P-1·issue-claim 모두 N/A)
  - 종료 시: `current_phase = P9-code-review`

## 브랜치 / 커밋 / 푸시 정책 (mode=sprint)

> **정본**: [`docs/planning/policies/branch-strategy.md`](../../docs/planning/policies/branch-strategy.md) (ADR-0044). 본 표는 *집행 절차*. 원칙(단일 trunk + 이슈-1-브랜치-1-PR + rebase 금지 + squash 권장)과 branch protection 9개 규칙은 정본 참조.

| 단계 | 동작 | 주체 / 시점 |
|---|---|---|
| 분기 | `git fetch origin` → `git checkout main` → `git pull --ff-only` → `git checkout -b <mode>/<slug>-issue-<N>` (base=최신 origin/main, ADR-0025) | /implement 진입 시 자동 (미분기일 때만; 이미 분기돼 있으면 skip). `--ff-only` 실패 시 BLOCKED — 로컬 main 오염 가능성, 사용자가 정리 후 재시도 |
| 커밋 | plan Subtask당 1커밋. 메시지 형식: `<type>(<scope>): <summary> (#<N>)` — 이슈 번호 필수 | /implement 작업 중 |
| push | 중간 push 안 함 (자가 push 금지) | /qa-test --ai PASS 직후 1회 일괄 (qa-test.md) |
| PR 생성 | `gh pr create --base main --head <브랜치> --body <PR body — Test Plan 4블록>` + **commit body** (squash 머지 후 main history 영구 기록)에 `Closes #N` + R-ID/F-ID 매핑 + breaking 노트 + 부팅 자산 변경 메모 명시 — ADR-0046 §2.4 / pull-request.md §5 (4 위치 책임 분리) | /qa-test --ai |
| 머지 게이트 (D-06 2단) | status check `pr-body-checkboxes` PASS — `pr-body-checkbox-gate.yml`이 PR body 미체크 갯수 == 0 시 자동 PASS 발행 (ADR-0046 §2.5). **`tested` 라벨 자체 폐지** — 사람은 라벨 클릭 안 함, Manual ✅ + DoD ✅ + Approve + 머지 클릭만 (사용자 책임 3단) | 사람 |
| 머지 후 close | `Closes #N` → 이슈 자동 close + `status:*` 일괄 제거 | `.github/workflows/sync-issue-labels.yml` PR `closed && merged==true` 이벤트 자동 처리 (ADR-0029, `tested` 처리 책임 v1.2로 제거) |

> **파생 이슈 (ADR-0008)도 동일** — 새 이슈는 새 브랜치(`<mode>/<slug>-issue-<N+m>`) + 별도 PR + 자체 머지·close. sub-issue 메커니즘 없음.

## Artifact Binding
- 입력: contract, plan, acceptance, eng-review(PASS), risk
- 출력: → `/code-review`, `/qa-test`
