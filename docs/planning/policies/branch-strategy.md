# 브랜치 전략 정책 — Trunk-based · 이슈-1-브랜치-1-PR · rebase 금지

> **위치**: `docs/planning/policies/branch-strategy.md`
> **상위 결정**: ADR-0044 (브랜치 전략 정본 신설), ADR-0025 (/implement 분기 시 main 최신화 — fetch + ff-only pull), ADR-0021 (이슈/PR 제목 명명 + 멀티 모듈 + Origin 약한 추적), ADR-0008 (파생 이슈 컨벤션), ADR-0001 (D-06 2단 게이트 — branch protection 강제).
> **관련 정책**: [`policies/sprint-cycle.md`](sprint-cycle.md) (D-06 게이트), [`policies/github-issue.md`](github-issue.md) (라벨·FSM·파생 이슈).

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v1.2 | 2026-05-19 | yongtae.cho@bespinglobal.com | **§5.1 Required status checks 행 갱신 + `tested` 라벨 트리거 폐기 박스 신설** (ADR-0046 정합). 사람 검증 표식이 `tested` 라벨에서 `pr-body-checkboxes` status check로 이전. (1) §5.1 Required status checks 행에 `pr-body-checkboxes` 추가 (AI 게이트 + unit/integration + 본 status check). (2) §5.1 직후 박스 — "tested 라벨 강제" 패턴 폐기 + `.github/workflows/pr-body-checkbox-gate.yml` 정본 명시 + ADR-0029 책임 범위 축소(PR↔Issue 라벨 동기화만, `tested` 제외). 본 정책 §1~§4 변경 없음. |
| v1.1 | 2026-05-18 | yongtae.cho@bespinglobal.com | **§6.1 적용 범위 갱신 + 정본 자산 카피 추가** — ADR-0044 v1.1 정합. v1.0 직후 발견 경로 확인 중 노출된 갭(`.claude/commands/*.md`의 정본 포인터가 newProject에서 404) 해소. `scripts/install.sh`가 본 파일을 newProject의 동일 경로(`docs/planning/policies/branch-strategy.md`)로 *항상 덮어쓰기* 카피 — 명령 파일 상대 경로 포인터 양쪽 모두 유효. LOCAL.md는 매 PR 진화 자산이라 기존 보존, 본 파일은 toolkit 진화 SoT이라 덮어쓰기. §6.1 적용 표 3축화(.claude/commands/ + CLAUDE.md/template + 본 파일 직접 카피). 다른 policies 3건은 본 amend 범위 외(별 PR/ADR로 분리). |
| v1.0 | 2026-05-18 | yongtae.cho@bespinglobal.com | 초안 — 사용자 피드백 "이 프로젝트로 다른 프로젝트 진행할 때, 브랜치 전략이 별도로 있어? 없다면 정책을 만들어야 할 거 같은데" 해소. 기존에 명령 파일(`implement.md`·`flow-bootstrap.md`·`flow-feature.md`) + ADR-0025 + sprint-cycle.md 5곳에 *암묵적으로* 흩어져 있던 브랜치 정책을 정본 1파일로 흡수. 사용자 결정: **머지 전략에서 rebase 제외**(squash 권장 + merge-commit 허용 + rebase 금지). 누락 갭(머지 전략·비-이슈 브랜치 명명·branch protection 상세·stale 정리·hotfix) 일괄 정의. agent-toolkit 자체(dogfooding)·newProject 양쪽에 동일 적용. |

---

> **본 절은 agent-toolkit이 사용자(도입 팀)에게 제공할 브랜치 운영의 표준 형태**다. 본 프로젝트(agent-toolkit) 자체 개발도 동일 모델을 따른다(dogfooding).
>
> newProject 도입자가 가장 먼저 읽어야 할 자리는 본 정책 + `.claude/commands/implement.md` §"브랜치 / 커밋 / 푸시 정책" 표 2곳. 명령 파일은 *집행*이고, 본 파일은 *원칙*이다.

## 1. 핵심 원칙

1. **단일 trunk = `main`** — release/staging/develop 등 *환경 분기 브랜치 도입 금지*. 환경 분리는 `.env.{dev,stg,prod}` + DB·외부 의존(ADR-0037 v1.1) *환경 변수 차원*에서 처리한다. git 브랜치 차원에서는 main 1개만 정본.
2. **이슈-1-브랜치-1-PR** — 작업은 GitHub Issue 단위로만 분기한다. 부모-자식 sub-branch·long-lived feature 브랜치 금지. 파생 이슈도 별도 이슈 → 별도 브랜치 → 별도 PR(ADR-0008).
3. **base = 항상 `main`** — PR 베이스 브랜치는 예외 없이 `main`. 파생 이슈도 부모 브랜치에 끼워넣지 않고 main에서 다시 분기.
4. **로컬 `main`은 항상 `origin/main`과 동일** — 로컬 `main`에 직접 커밋하지 않는다. 모든 변경은 작업 브랜치 → PR → squash 머지 경로로만.
5. **rebase 금지** — `git rebase`·`git pull --rebase`·GitHub "Rebase and merge" 모두 금지(ADR-0044 §2.3). 머지 history rewriting은 silent 손실을 유발할 위험이 있어 채택하지 않는다.
6. **이슈 없는 작업 금지** — 모든 작업 브랜치는 해당 GitHub Issue를 가진다. 예외는 §3.2 부트스트랩·docs-only 메타 작업 한정.

## 2. 브랜치 명명 컨벤션

### 2.1 작업 브랜치 (이슈 단위)

```
<mode>/<slug>-issue-<N>
```

- `<mode>`: `feat` / `mod` / `bug` / `design` 중 1개. `/flow-feature`의 mode 자동 결정과 1:1 매핑(ADR-0032).
  - `feat`: 신규 기능 추가
  - `mod`: 기존 기능 변경 / 비기능 개선
  - `bug`: 버그 수정 (hotfix 포함 — §3.3 참조)
  - `design`: 디자인 변경 / UI 정합 (스타일·레이아웃·토큰)
- `<slug>`: 이슈 제목에서 추출한 kebab-case 약식(영문 소문자·숫자·`-` 만). 길이 ≤ 40자 권장.
- `<N>`: GitHub Issue 번호. 필수.

예시:
- `feat/user-auth-issue-42`
- `bug/login-redirect-issue-58`
- `design/dashboard-tokens-issue-71`
- `mod/api-pagination-issue-103`

자동 생성: `/implement` 진입 시 미분기 상태이면 본 패턴으로 자동 분기(ADR-0025 4단계 절차).

### 2.2 부트스트랩·메타 브랜치 (이슈 없음, 예외)

```
chore/<purpose>-<YYYYMMDD>
```

- 용도: NEW_PROJECT 산출 일괄 등록(`/flow-bootstrap`), 정책 문서 신설/대규모 cross-ref 정리 등 *이슈 단위로 쪼개기 어려운 도구 작업*.
- 예시:
  - `chore/planning-bootstrap-20260518` (`/flow-bootstrap` 자동 분기)
  - `chore/branch-strategy-policy-20260518` (본 정책 신설 PR)
- 본 패턴은 *예외* 트랙이며, 일반 feature 작업에 남용하지 않는다. 의심되면 GitHub Issue를 먼저 생성하고 §2.1로 회귀.

### 2.3 사용 금지 패턴

| 패턴 | 사유 |
|---|---|
| `release/*`·`develop`·`stg`·`prod` | §1.1 — 환경은 `.env.{dev,stg,prod}` 차원, git 브랜치 차원 아님 |
| `hotfix/*` | §3.3 — `bug/<slug>-issue-<N>`로 흡수. 우선순위는 `priority:high` 라벨 + 신속 머지로 표현 |
| `feature/<long-lived>` (이슈 없음) | §1.2 — 모든 작업은 이슈 단위. 큰 작업은 WBS로 쪼개 여러 이슈로 분해 |
| 한글·공백·대문자·특수문자 포함 | shell escape + URL safety + tooling 호환성 |
| `<mode>` 접두 누락 | `/flow-feature` 모드 자동 결정·gate-precondition hook이 prefix를 파싱 |

## 3. 분기·커밋·푸시 정책

### 3.1 분기 절차 (mode=sprint, `/implement` 자동 진입 시)

ADR-0025 4단계 절차를 그대로 따른다:

```bash
git fetch origin
git checkout main
git pull --ff-only            # diverge 시 BLOCKED — 사용자가 로컬 main 정리 후 재시도
git checkout -b <mode>/<slug>-issue-<N>
```

- `--ff-only` 실패 시: 로컬 `main`이 `origin/main`과 diverge한 상태(§1.4 위배). 자동 복구 안 함, 사용자 명시 개입 필요.
- 이미 작업 브랜치에 있으면 skip(분기 동작만 skip, 커밋·push는 진행).
- mode=planning은 본 절 적용 외(브랜치 자유, main 직접 커밋 허용 — docs-only 변경 시).

### 3.2 커밋 메시지 컨벤션 (Conventional Commits)

ADR-0021 §1.5의 이슈/PR 제목 명명 규칙과 **동일 형식**을 커밋 메시지에도 적용:

```
<type>(<scope>): <summary> (#<N>)
```

- `<type>`: `feat` / `fix` / `mod` / `docs` / `chore` / `refactor` / `test` / `perf` / `style` 중 1개
- `<scope>`: 영향 모듈/영역 (kebab-case). 멀티 모듈 시 `multi` 또는 가장 큰 영역 1개(ADR-0021 §1.6 정합)
- `<summary>`: 한국어·영문 자유. 명령형 어휘. 마침표 없음.
- `(#<N>)`: GitHub Issue 번호. 필수. 부트스트랩·메타 브랜치(§2.2)는 생략 허용.

예시:
- `feat(auth): JWT 토큰 갱신 엔드포인트 추가 (#42)`
- `fix(login): 토큰 만료 시 redirect 누락 (#58)`
- `docs(plan): ADR-0044 브랜치 전략 정본 신설`

`Co-Authored-By` 트레일러 등 추가 메타데이터는 자유.

> **참고**: GitHub PR 본문에는 `Closes #<N>` 키워드를 1회 포함(자동 close + `status:*` 정리, ADR-0029).

### 3.3 hotfix 정책

긴급 prod 패치도 별도 브랜치 prefix를 두지 않는다. 처리 절차:

1. GitHub Issue 등록 — `priority:high` + `type:bug` 라벨
2. 작업 브랜치 `bug/<slug>-issue-<N>` 분기 (일반 bug와 동일)
3. AI 게이트 6축 + 휴먼 게이트는 *최소한 단축 적용* — `tested` 라벨 부착 + Approve ≥ 1 (D-06 2단 유지)
4. squash 머지 → 이슈 close → 정상 배포 파이프라인

배포 우선순위·SLA는 라벨 + 이슈 본문으로 표현하고, git 브랜치 구조는 일반 작업과 동일하게 유지한다. branch protection 우회·`--no-verify` 사용 금지.

### 3.4 push 시점

- 중간 push 금지(자가 push 금지) — 부분 작업물 노출 차단
- `/qa-test --ai` PASS 직후 1회 일괄 push (`qa-test.md` 절차)
- push 직후 `gh pr create --base main --head <브랜치>` PR 생성

### 3.5 작업 도중 main 최신화 (정합)

작업 브랜치 작업 중 `main`이 진전된 경우 머지 충돌이 예상되면:

```bash
git fetch origin
git merge origin/main              # ✅ 머지 커밋 허용
# 또는
git merge --no-ff origin/main      # ✅ 명시 머지 커밋
```

- `git rebase origin/main` ❌ 금지(§1.5)
- `git pull --rebase` ❌ 금지(§1.5)

머지 커밋은 squash 머지 시점에 단일 커밋으로 평탄화되므로 main history에는 노출되지 않는다.

## 4. PR 머지 전략

### 4.1 머지 옵션별 정책

GitHub repository "Pull Requests" 설정에서 3개 옵션 중 다음으로 구성:

| 옵션 | 허용 여부 | 사용 시점 |
|---|---|---|
| **Squash and merge** | ✅ **권장 기본** | 모든 일반 PR. 이슈 1개 = main 커밋 1개 1:1 매핑 |
| **Create a merge commit** | ⚠️ 예외 허용 | 의도적으로 다중 커밋 history를 보존해야 할 때(예: 다단계 마이그레이션, ADR 분할 발행). PR 본문에 보존 사유 명시 |
| **Rebase and merge** | ❌ **금지** | §1.5 — silent rewriting 위험 + ADR-0025 ff-only 정합 위배 |

권장 GitHub repo 설정:
- Allow squash merging: **ON**
- Allow merge commits: **ON** (예외용)
- Allow rebase merging: **OFF**
- Default to "Squash and merge"
- "Automatically delete head branches": **ON** (§5.2 정합)

### 4.2 머지 커밋 메시지 (squash 시)

PR 제목을 그대로 사용(이미 Conventional Commits 형식 — ADR-0021). GitHub squash 머지 기본 동작과 정합.

```
feat(auth): JWT 토큰 갱신 엔드포인트 추가 (#42)
```

`Closes #42`는 PR 본문에 두고 커밋 메시지에서는 생략 가능(GitHub 자동 close는 PR 본문 기준).

## 5. Branch Protection (D-06 휴먼 게이트 강제)

### 5.1 main 브랜치 보호 규칙

GitHub Settings → Branches → Branch protection rule for `main` 에서 다음을 강제:

| 규칙 | 설정 | 사유 |
|---|---|---|
| **Require a pull request before merging** | ✅ | §1.4 — main 직접 커밋 차단 |
| **Required approvals** | ≥ 1 | D-06 휴먼 게이트 (sprint-cycle.md §2) |
| **Dismiss stale pull request approvals when new commits are pushed** | ✅ | 변경 후 재승인 강제 |
| **Require status checks to pass before merging** | ✅ | CI green 필수 |
| **Required status checks** | `ai-gate` 또는 동치(`/qa-test --ai` 결과) + 기존 unit/integration CI + **`pr-body-checkboxes`** (ADR-0046 §2.5) | AI 게이트 6축(ADR-0011·0037·0038) + LOCAL.md 동기(ADR-0040) + 사람 검증 체크박스 ✅ (ADR-0046 §2.5 — PR body 미체크 시 status FAIL) |
| **Require branches to be up to date before merging** | ✅ | ADR-0025 ff-only 정합 |
| **Require conversation resolution before merging** | ✅ | 휴먼 리뷰 코멘트 미해결 차단 |
| **Require linear history** | ❌ | §4.1 merge-commit 예외 허용을 위해 끔. 기본 동작은 squash이므로 실질 linear |
| **Do not allow force pushes** | ✅ | main history 안전 |
| **Restrict who can push to matching branches** | (선택) | 보안 강화 — 머지 권한자 제한 |
| **Allow specified actors to bypass required pull requests** | ❌ | admin bypass 금지 (`--no-verify` 우회 차단과 정합) |

**v1.2 변경 (ADR-0046 정합)** — 사람 검증 표식이 `tested` *라벨*에서 `pr-body-checkboxes` *status check*로 이전. 라벨 기반 머지 게이트 워크플로 패턴 폐기. `.github/workflows/pr-body-checkbox-gate.yml`이 `### Manual verification` + `### DoD coverage` subsection의 미체크 갯수 == 0일 때만 status check PASS를 발행. 라벨 표식 자체 없음 — 체크박스 상태가 머지 게이트로 직결. ADR-0029 `sync-issue-labels.yml`은 PR ↔ Issue 라벨 동기화 책임만 유지(`tested` 처리 책임 제거).

### 5.2 머지 후 브랜치 정리

- **자동 삭제**: GitHub repo 설정 "Automatically delete head branches" ON으로 PR 머지 직후 원격 브랜치 자동 삭제.
- **로컬 정리**: 사용자 책임 — `git fetch --prune` + `git branch -d <merged>`. 미머지 브랜치에 대한 강제 삭제는 사용자 명시 승인 후에만(`-D` 사용 시).

### 5.3 stale 브랜치 청소

- **개념**: 머지 안 된 채로 마지막 커밋 후 ≥ 30일 경과한 원격 브랜치.
- **검출**: `git for-each-ref --sort=-committerdate refs/remotes/origin/ --format='%(committerdate:short) %(refname:short)'` 또는 GitHub UI "Branches" 탭.
- **처리**: 해당 이슈가 `status:blocked`/`status:in-progress` 정당 사유로 살아 있는지 검토. 정당 사유 없으면 사용자가 명시 승인 후 삭제(이슈도 동시에 close 또는 sprint rollover — sprint-cycle.md §3.4).
- **자동화 보류**: 본 정책은 *수동 정리* 원칙. 자동 청소 워크플로는 `open-items.md` 후속 항목.

## 6. 적용 범위·예외

### 6.1 적용 (v1.1 갱신)

- agent-toolkit 자체(dogfooding) — 본 정책 즉시 적용
- newProject 전수 — `install.sh`가 3축으로 본 정책을 흡수:
  - `.claude/commands/`(implement·flow-feature·flow-bootstrap 등) — 집행 절차 + 정본 포인터 (rsync 카피)
  - `docs/install/CLAUDE.template.md` → newProject의 `CLAUDE.md` §"필수 규칙 12" — 원칙 인라인 흡수
  - **`docs/planning/policies/branch-strategy.md`** — 본 정본 파일 자체를 newProject의 동일 경로에 *항상 덮어쓰기* 카피(ADR-0044 v1.1). 명령 파일 상대 경로 `../../docs/planning/policies/branch-strategy.md`가 newProject에서도 유효.
- LOCAL.md(ADR-0040)와의 카피 정책 차이: LOCAL.md는 *매 PR 진화 자산*이라 기존 파일 발견 시 보존, 본 파일은 *toolkit 진화 SoT*이라 항상 덮어쓰기. newProject가 임의 수정하지 않는다 — 정책 변경은 agent-toolkit 측 amend 후 install 재실행으로 흘러 들어옴.

### 6.2 예외

| 예외 | 허용 조건 |
|---|---|
| docs-only PR (정책 문서·README·CHANGELOG 단독) | `chore/<purpose>-<YYYYMMDD>` 브랜치 허용. AI 게이트 6축 중 코드 관련 축은 N/A 명시 |
| 부트스트랩 PR (`/flow-bootstrap`) | `chore/planning-bootstrap-<YYYYMMDD>` 자동 분기. Test Plan N/A |
| 외부 의존 장애로 부팅 검증 불가 | ADR-0037 v1.1 — 사용자 승인 후 명시적 skip |
| 단일 환경 운영 (stg=prod 공유) | ADR-0037 v1.1 — N/A + 사유 명시 |

## 7. 영향 받는 자산 (Cross-ref)

| 자산 | 본 정책과의 관계 |
|---|---|
| [`.claude/commands/implement.md`](../../../.claude/commands/implement.md) §"브랜치 / 커밋 / 푸시 정책" | 분기 절차(§3.1)·커밋 메시지(§3.2)·push 시점(§3.4) 집행 정본 |
| [`.claude/commands/flow-bootstrap.md`](../../../.claude/commands/flow-bootstrap.md) §"산출" + §"Phase Sequence" 1~5 | 부트스트랩 브랜치(§2.2) 집행 정본 |
| [`.claude/commands/flow-feature.md`](../../../.claude/commands/flow-feature.md) §"파생 이슈" | 파생 이슈도 main에서 분기(§1.3) 집행 정본 |
| [`policies/sprint-cycle.md`](sprint-cycle.md) §2 D-06 게이트 + 휴먼 게이트 | branch protection 강제(§5) 정합 |
| [`policies/github-issue.md`](github-issue.md) §1.5 이슈/PR 제목 + §5 파생 이슈 Origin | 커밋 메시지 컨벤션(§3.2)·파생 이슈 별 브랜치(§1.2) 정합 |
| [`adr/0025-implement-branch-main-sync.md`](../adr/0025-implement-branch-main-sync.md) | §3.1 4단계 절차의 원천 ADR |
| [`adr/0021-issue-naming-and-origin.md`](../adr/0021-issue-naming-and-origin.md) | §3.2 커밋 메시지 컨벤션의 원천 ADR |
| [`adr/0008-derived-issue-convention.md`](../adr/0008-derived-issue-convention.md) | §1.2 파생 이슈 별 브랜치의 원천 ADR |
| [`adr/0044-branch-strategy.md`](../adr/0044-branch-strategy.md) | 본 정책 신설 결정 ADR |
| [`policies/pull-request.md`](pull-request.md) §2 | 머지 전략을 본 정책 §4에서 인용. PR body·사용자 책임·미체크 강제·3 레이어 책임 분리는 본 정책 범위 외 — pull-request.md가 정본 (ADR-0046) |
| [`docs/install/CLAUDE.template.md`](../../install/CLAUDE.template.md) | newProject용 정본 포인터(§"필수 규칙") |
| `CLAUDE.md` §"GitHub 이슈·스프린트 정책" | agent-toolkit 자체용 정본 포인터 |

## 8. 변경 절차

본 정책의 §1~§5 변경은 ADR 발행 필수(`docs/planning/adr/NNNN-*.md`). §6 예외 확장·§7 cross-ref 추가·오탈자 수정은 본 파일 변경 이력 표 갱신만으로 처리한다.

변경 영향 점검 체크리스트:
- [ ] §1 핵심 원칙 변경 시 — `implement.md`·`flow-bootstrap.md`·`flow-feature.md` 3건 동기 확인
- [ ] §2 명명 컨벤션 변경 시 — `/implement` 자동 분기 절차 + gate-precondition hook + ADR-0032 mode 자동 결정 정합 확인
- [ ] §4 머지 전략 변경 시 — repo settings (`gh api repos/:owner/:repo --jq '.allow_squash_merge,.allow_merge_commit,.allow_rebase_merge'`) + branch protection 동기 확인
- [ ] §5 protection 변경 시 — `tested` 라벨 워크플로(ADR-0029) + AI 게이트 status check 매핑 확인
