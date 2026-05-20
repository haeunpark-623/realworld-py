# {{PROJECT_NAME}} — 로컬에서 켜기

> **목적**: 이 저장소를 처음 clone한 사람이 *이 파일 1개*만 따라 하면 dev/stg/prod 3 profile 모두 로컬에서 부팅 가능하도록 한다.
> **정본 위치**: 이 파일은 newProject 루트의 *유저 facing* 정본. 부팅 자산 *정의*의 SoT는 `docs/planning/12-scaffolding/<lang>.md` §7 (평면 명명, `file-numbering.md` §3.2). 다국어 newProject는 lang별 파일 모두가 SoT (예: `typescript.md` + `java.md`). 본 LOCAL.md와 lang별 12-scaffolding은 매 PR에서 동기 갱신된다 (ADR-0037 v1.1 + ADR-0040).
> **진화 규칙**: 부팅 자산(`.env.{dev,stg,prod}.example`·migrations·lockfile·setup scripts·부팅 명령)이 변경되면 본 파일도 같은 PR에서 갱신. AI 게이트 6번째 축이 동기 누락을 BLOCK한다.

---

## 변경 이력

> **첫 채움 시 정책**: install.sh가 본 template를 카피한 직후 도입자(또는 에이전트)는 본 표에서 **v0.1만 남기고 `v0.X-template` 행은 모두 삭제**한다. 메타 이력은 toolkit 측 `docs/install/LOCAL.template.md`의 PR/commit log가 정본이며, newProject LOCAL.md에는 *해당 newProject의* 본문 갱신 이력만 누적한다.

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | {{INIT_DATE}} | {{INIT_AUTHOR}} | 초안 — install.sh가 LOCAL.template.md를 카피해 생성. 첫 채움은 12-scaffolding §7 작성 직후. |
| v0.2-template | 2026-05-16 | yongtae.cho@bespinglobal.com | template 자체 보강 (test-case-3 PR #37·#38 회귀 흡수, ADR-0040 v1.1, **stack-agnostic**): §1.5 *사전* 함정 안내 박스 신설(monorepo+root .env / ORM 최초 migration / SPA 정적 서버 3종), §2 단계 4 push vs migrate init 분기, §3.2·3.3 실제 동작 stg/prod 명령 패턴, §5.3·5.4 cwd 함정 troubleshooting. **언어 일반화** — §1.5.1 해결 패턴 (a)~(d): Java/Spring `spring.profiles.active`·Python `python-dotenv`/Pydantic·Go `godotenv`·Node `dotenv-cli` 4개 동치 + symlink fallback. §1.5.2 ORM에 Prisma·TypeORM·SQLAlchemy·JPA(Hibernate)·Flyway·Liquibase 사례 포함. §3.2·3.3·5.4 예시도 Node와 Java 양 stack 명시. |
| v0.3-template | 2026-05-16 | yongtae.cho@bespinglobal.com | §4 부팅 자산 표 분리 (ADR-0037 v1.2 정합) — "DB migrations" 단일 행 → "스키마 적용 (dev iteration)" + "DB migrations (stg/prod release)" 2행. dev iteration용은 Prisma `db push`·TypeORM `synchronize`·Hibernate `ddl-auto`·SQLAlchemy `create_all`·Alembic `upgrade head` 류, stg/prod release용은 정식 migration 파일 디렉토리(prisma/migrations·flyway·alembic/versions). 두 흐름이 다른 자산임을 LOCAL.template와 scaffolding.schema 양쪽에서 명시. lockfile·설치/seed scripts·부팅 명령 예시도 Python(poetry/uv)·Java(gradle) 사례 추가. |
| v0.4-template | 2026-05-17 | yongtae.cho@bespinglobal.com | **3분류 모델 (ADR-0037 v1.3)** — test-case-4 commit `2cb6fa0` 회귀 흡수. v0.3-template 2분기 모델이 *분리형*만 표현해서 단일 메커니즘 스택(Spring Boot + Flyway integration 등)이 redundant/wrong 명령(`./gradlew flywayMigrate` w/o plugin 등)을 만들어 넣는 함정. §1.5.2 ORM 흐름을 (a) 분리형 · (b) 단일 메커니즘(부팅 통합) · (c) N/A 3분류로 재편. §2 셋업의 단계 4 코멘트에 단일 메커니즘 패턴 명시. §4 자산 표 두 migration 행에 footnote — 단일 메커니즘 채택 시 양쪽 동일 참조 또는 "N/A — §3 부팅이 곧 migrate" 허용. §5.3 troubleshooting을 분류별 분기로 재편. Spring Boot + Flyway integration이 canonical 예. |
| v0.5-template | 2026-05-18 | yongtae.cho@bespinglobal.com | **풀스택 monorepo 케이스 + 평면 명명 SoT 정합 (test-case-5 흡수)** — (1) SoT 인용 경로를 `12-scaffolding/12-scaffolding.md`(존재 불가) → `12-scaffolding/<lang>.md` (평면 명명, `file-numbering.md` §3.2)로 일괄 교정. 다국어 newProject는 lang별 파일 모두를 SoT로 본다. (2) §1.5.1 monorepo 함정에 **(e) 워크스페이스별 .env 완전 분리** 패턴 추가 — FE/BE가 다른 stack인 풀스택 케이스(예: Vite/pnpm FE + Spring Boot/Gradle BE)에서 가장 흔한데 (a)~(d) 어디에도 안 들어가던 5번째 옵션. 채택 시 루트 cwd 함정 자체가 없음. (3) §2 단계 3 cp 블록을 "단일 패키지 vs monorepo 워크스페이스 분리" 2 변형 코멘트로 분기 — 후자는 워크스페이스 수 × 3벌. (4) §3.1~3.3 부팅 명령에 "옵션 A 워크스페이스 직접 실행 / 옵션 B docker-compose 통합" 2 변형 가이드 + 환경 변수 출처에 `{workspace}/.env.{profile}` 표기. (5) §4 자산 표 환경 변수·lockfile·컨테이너 행에 "monorepo 분리 시 행 N개로 확장" footnote. (6) §5.2 troubleshooting의 "3 벌" hardcoded → "단일 3벌 / monorepo 워크스페이스 수 × 3벌"로 분기. (7) 변경 이력 표 헤더 위에 "첫 채움 시 v0.X-template 행 삭제" 정책 1줄 추가. |
| v0.7-template | 2026-05-18 | yongtae.cho@bespinglobal.com | **multi-stack 의존성 설치 + Gradle multi-project syntax 함정 흡수 (ADR-0043, test-case-5 LOCAL.md §2 step 2 사용자 피드백)** — test-case-5의 `./gradlew :backend:dependencies` 가 (a) 루트에 wrapper 없음(backend/gradlew) + (b) `settings.gradle.kts: rootProject.name = "backend"`인 standalone build에 multi-project syntax 잘못 적용으로 `Project 'backend' not found in root project 'backend'.` 에러. LLM이 분포 majority(multi-project root build)를 standalone에 hallucinate한 패턴. (1) §1.5.5 사전 함정 신설 — multi-stack 의존성 설치 원칙(stack별 1줄씩, 자기 wrapper/CLI 위치에서) + Gradle wrapper + settings.gradle 위치 점검 3축(`find . -name gradlew` + `cat settings.gradle* | grep rootProject.name/include`) + multi-project vs standalone 분기 호출 표 + Maven/sbt/Bazel/Cargo 동치 함정 stack-agnostic 표. (2) §5.6 troubleshooting 신설 — `./gradlew: No such file` + `Project 'X' not found in root project 'Y'.` 증상별 진단·해결(§1.5.5 cross-ref). (3) §5.6 placeholder → §5.7 renumber. (4) §2 단계 2 placeholder 확장 — multi-stack 인지 주석 4줄 + Gradle 분기 1줄 추가. WARN-class(ADR-0042 점진성 정합) — schema·validator 미터치. 재발 ≥ 2건 누적 시 scaffolding.schema.yaml §5에 wrapper 위치 검증 must_contain BLOCK 격상. §1.5 박스 5건 도달 — 6번째 추가 시 `docs/install/local-pitfalls.md` 분리 reform 트리거. |
| v0.6-template | 2026-05-18 | yongtae.cho@bespinglobal.com | **컨테이너 베이스 이미지 함정 2종 흡수 (ADR-0042, test-case-5 uncommitted fix)** — (1) §1.5.4 사전 함정 신설 — 베이스 이미지가 사전 점유한 비루트 사용자(예: eclipse-temurin Ubuntu base의 UID 1000 `ubuntu`)와 `useradd --uid 1000` 충돌 + corepack 비인터랙티브 환경 GPG 서명 프롬프트(node:* + `corepack enable` 단독) 2종을 stack-agnostic 원칙으로 박음. eclipse-temurin / node / python / distroless 베이스에 동일 적용. (2) §5.5 troubleshooting 신설 — `useradd: UID ... is not unique` 류 에러 + corepack 단계 hang/timeout 증상별 진단 + 해결(§1.5.4 cross-ref). (3) 기존 §5.5 placeholder를 §5.6으로 renumber. WARN-class — schema·validator 미터치(ADR-0042 §2.2 — stack 다양성·진화 속도 미스매치로 false-positive 위험. 재발 ≥ 2건 누적 시 schema BLOCK 격상 검토). |

---

## 1. 사전 요구사항

> 본 절은 12-scaffolding §1 디렉토리 트리 + §2 패키지 명명 규칙에서 도출.

- **언어/런타임**: {{예: Node.js 20 LTS, Python 3.12, Java 21, ...}}
- **패키지 매니저**: {{예: pnpm 9, uv, gradle wrapper, ...}}
- **컨테이너 (선택)**: {{Docker 24+, docker-compose v2, ...}}
- **DB**: {{PostgreSQL 16, MySQL 8, SQLite, ...}}
- **OS 가정**: {{macOS / Linux / WSL2}}

---

## 1.5 흔한 함정 — *사전* 안내

> 본 절은 사후 troubleshooting(§5)이 아니라 **셋업 *전*에 한 번 읽어 미리 피하는** 함정 모음. test-case-3 PR #37·#38 회귀에서 도출 — 다음 newProject에서 같은 실패를 반복하지 않게 한다.

### 1.5.1 monorepo + root `.env.{profile}` cwd 미스매치

`.env.{dev,stg,prod}`을 project root에 두는 monorepo는 다음 함정에 노출됨:
- 워크스페이스 cwd(예: `backend/` · `services/api/`)에서 실행되는 도구(ORM CLI · 런타임 환경 변수 자동로드 등)는 **root env를 자동으로 로드하지 않는다**
- 결과: `Error: Environment variable not found: DATABASE_URL` 류 에러로 부팅 실패

**해결 패턴** (스택별로 1개 선택 — 본 newProject 채택 방식을 명시):

- (a) **build tool / 런타임의 profile-aware 설정 기능 활용** (스택 native, 가장 권장)
  - Java/Spring: `application-{profile}.yml` + `SPRING_PROFILES_ACTIVE=dev` (env 파일이 아니라 profile yml로 분리하는 게 Spring native 방식, 단일 또는 root 디렉토리 모두 OK)
  - Python(Poetry/uv): `python-dotenv` + 앱 시작 시 `load_dotenv("../.env.dev")` 또는 `pydantic-settings`의 `_env_file=...`
  - Go: `godotenv.Load("../.env.dev")` 명시 호출
  - Node: 아래 (b) 패턴 사용
- (b) **dotenv-cli 래핑** (Node monorepo 한정)
  - 각 워크스페이스 스크립트를 `dotenv -e ../.env.{profile} -- ...`로 감싼다 (`devDependencies: dotenv-cli@^7.x`). 예: `"dev": "dotenv -e ../.env.dev -- tsx watch src/server.ts"`
- (c) **monorepo 도구의 env-pass 옵션** (Node 한정)
  - Turborepo `passThroughEnv` · Nx `env` · pnpm `--filter` + root 셸 export 등
- (d) **워크스페이스별 .env symlink/카피** (스택 무관)
  - 추가 동기 부담은 있지만 도구·언어 비의존
- (e) **워크스페이스별 .env 완전 분리 (root .env 없음)** — 풀스택 monorepo에서 가장 흔함
  - 구조: 루트에 `.env*` 없음. 각 워크스페이스가 자기 `.env.{dev,stg,prod}.example` 보유 (예: `frontend/.env.{p}.example` + `backend/.env.{p}.example` — 워크스페이스 N개면 N × 3 = N\*3벌)
  - 호출: 각 워크스페이스가 stack native 메커니즘으로 *자기 .env* 자동 로드. 예 — Vite는 cwd의 `.env.{mode}` 자동 로드 / Spring Boot는 `SPRING_PROFILES_ACTIVE` + `application-{profile}.yml` / Node는 `dotenv -e .env.{p} -- ...` 등
  - 장점: 루트 cwd 함정 자체가 없음. FE/BE가 다른 stack(예: pnpm + Gradle)일 때 한쪽 도구 강제 불필요
  - 단점: `.example` 파일 수가 N\*3로 늘어남 — §5.2 troubleshooting과 §4 자산 표가 N\*3 분량 lint 필요
  - 적용 예: 본 template 권고 — 풀스택 (FE Vite/Next + BE Spring/Rails/Django) monorepo

본 프로젝트 채택: `{{(a)/(b)/(c)/(d)/(e) 중 1개 또는 N/A — 단일 패키지}}`

### 1.5.2 ORM 최초 migration 부재 (3분류 모델)

스택·프레임워크가 채택한 **호출 메커니즘**에 따라 다음 3분류 중 1개. 분류는 stack이 아닌 *프로젝트 선택*(예: Spring Boot도 Gradle Flyway 플러그인 도입 시 분리형 가능):

- **(a) 분리형** — dev 빠른 동기 명령 ≠ 운영 migrate 명령 (각각 따로 호출)
  - 함정: `prisma migrate deploy` · `flyway migrate` · `alembic upgrade head` 등 운영 migration은 **기존 파일만** 적용. 최초 부팅 시 `migrations/` 비어 있으면 DB 빈 상태로 남음
  - dev 빠른 동기: Prisma `db push --skip-generate` / TypeORM `synchronize=true` / SQLAlchemy `Base.metadata.create_all` — migration 파일 없이 schema → DB
  - 정식 migration의 최초 1회: Prisma `migrate dev --name init` / Flyway `V1__init.sql` + `flyway migrate` CLI / Liquibase `db.changelog-master.xml` + `update`
  - 적용 예: Prisma, TypeORM, SQLAlchemy, Django(`manage.py migrate`), Rails(`db:migrate`), Flyway/Liquibase **standalone CLI 또는 Gradle/Maven 플러그인 사용 시**
- **(b) 단일 메커니즘 (부팅 통합)** — 부팅 명령 자체가 migrate를 수행. dev/stg/prod 모두 동일
  - **별도 migrate 명령 없음** — 앱 시작 시 framework integration이 `migrations/` 디렉토리를 읽어 자동 적용
  - 작성 작업: migration 파일(`db/migration/V*.sql` 등)을 추가만 하면 됨. 적용은 다음 `bootRun`이 자동 수행
  - 적용 예:
    - **Spring Boot + Flyway integration** (canonical) — `spring.flyway.enabled=true`(기본값) + `org.flywaydb:flyway-core` 의존성만으로 `bootRun` 시 `db/migration/V*.sql` 자동 적용. **`flywayMigrate` Gradle 태스크 호출 금지** — 그 태스크는 별도 `org.flywaydb.flyway` 플러그인 도입 시에만 존재하고 Spring Boot 설정과 별 컨피그 필요
    - **Spring Boot + Liquibase integration** — `spring.liquibase.enabled=true` + `spring-boot-starter-jdbc` + Liquibase 의존성
    - **Hibernate `ddl-auto` 단독** (Flyway/Liquibase 없이) — `spring.jpa.hibernate.ddl-auto=update` 또는 `create` (운영 비권장, dev/POC만)
    - **EF Core (.NET)** — 앱 시작 코드에 `Database.Migrate()` 호출
    - **GORM (Go)** — 앱 시작 코드에 `db.AutoMigrate(&Model{})` 호출
- **(c) N/A** — ORM/스키마 자체 없음 (CLI-only, frontend-only, file-system store 등)

본 프로젝트 채택 분류: `{{(a) 분리형 / (b) 단일 메커니즘 / (c) N/A 중 1개}}`
- (a) 채택 시 — dev: `{{명령}}`, stg/prod: `{{명령}}`
- (b) 채택 시 — 부팅 명령 (§3 참조): `{{명령}}`, 자동 migrate 메커니즘: `{{예: spring.flyway.enabled=true / Database.Migrate() on startup}}`
- (c) 채택 시 — 사유: `{{예: CLI-only, no DB}}`

### 1.5.3 stg/prod 부팅용 정적 서버 가정 (SPA frontend 한정)

> 본 함정은 frontend가 SPA(React/Vue/Svelte 등)인 경우에만 해당. **Java/Spring + Thymeleaf · Django + 템플릿 · 단일 backend** 등 SSR/MPA 구조는 N/A.

frontend가 SPA인 경우 stg/prod는 *빌드 산출물* 기반. 다음 두 함정 흔함:
- `serve` · `http-server` 같은 별도 도구는 보통 **미설치** — `npm install -g serve` 강제는 newProject 사용자 부담 + 버전 불일치 위험
- `NODE_ENV=production` 같은 inline 셋팅은 다른 env 변수(API_URL 등)를 누락시킴 — `.env.{stg,prod}`를 명시 로드 권장 (§1.5.1 해결 패턴 적용)

**해결 패턴**: 빌드 도구가 기본 제공하는 preview 모드 사용 — `vite preview --port 4173` · `next start` · `astro preview` 등. backend는 §1.5.1의 채택 패턴으로 `.env.{stg,prod}` 로드 (Node: `dotenv -e .env.prod -- node dist/server.js` / Java: `SPRING_PROFILES_ACTIVE=prod java -jar app.jar` 등).

### 1.5.4 컨테이너 베이스 이미지 함정 2종 (Dockerfile 작성 시)

> 본 함정은 Dockerfile/docker-compose를 사용하는 newProject에 한정. dev 환경 native 부팅(`pnpm dev` · `./gradlew bootRun`)만 사용하고 stg/prod도 host에서 직접 실행하는 구조는 N/A.
> 두 함정 모두 **베이스 이미지 버전 진화 + LLM 학습 분포 격차**가 원인 — 본 절을 *Dockerfile 작성·검토 직전*에 한 번 읽고 미리 피한다. (ADR-0042)

#### (1) 베이스 이미지가 사전 점유한 비루트 사용자와 `useradd` 충돌

**증상**: `docker build` runtime stage의 `RUN useradd --uid 1000 --create-home --shell /bin/bash app` 류 단계에서 다음 에러로 실패.
```
useradd: UID 1000 is not unique
# 또는
useradd: user 'app' already exists
```

**원인**: 최근 베이스 이미지(`eclipse-temurin:21-jre`·`eclipse-temurin:21-jdk` Ubuntu base / Bitnami / Chainguard / node:22-alpine `node` 사용자 등)는 보안 강화 방향으로 **UID 1000 비루트 사용자를 이미 제공**. 가장 흔한 사례:
- `eclipse-temurin:21-*` (Ubuntu 22.04 base) — `ubuntu` 사용자 (UID 1000, since 2024)
- `node:*-alpine` · `node:*` — `node` 사용자 (UID 1000)
- `nginx:*-alpine` — `nginx` 사용자 (UID 101, sub-1000)

LLM 학습 분포의 다수가 *이전*(Debian/Alpine base 시점 UID 1000 비어 있던 시기)에 작성된 Dockerfile이라 `useradd --uid 1000 ... app`을 무조건 추가하는 경향.

**해결 원칙 (stack-agnostic)**: **베이스 이미지가 이미 비루트 사용자를 제공하면 그걸 그대로 `USER <name>` 사용**. 새로 만드는 건 베이스가 root-only(예: `alpine` 단독·`debian:slim` 단독·`scratch`)일 때만.

| 베이스 이미지 | 채택 비루트 사용자 | Dockerfile 예 |
|---|---|---|
| `eclipse-temurin:21-jre` (Ubuntu base) | `ubuntu` (UID 1000) | `USER ubuntu` |
| `node:22-alpine` · `node:22` | `node` (UID 1000) | `USER node` |
| `python:3.12-slim` | 없음 (root only) | `RUN useradd --create-home app && USER app` (UID 자동 할당, `--uid 1000` 명시 금지) |
| `golang:1.23-alpine` | 없음 (root only) | 위와 동일 패턴 |
| `gcr.io/distroless/*:nonroot` | `nonroot` (UID 65532) | `USER nonroot` |
| `nginx:1.27-alpine` (frontend 정적 호스팅) | `nginx` (sub-1000) | 보통 권한 그대로 사용 — 강제 비루트 시 `USER nginx` |

**검증 절차**: Dockerfile 작성 직후 다음 1회 실행으로 점검:
```bash
docker run --rm --entrypoint sh <base-image> -c 'cat /etc/passwd | tail -5'
# UID 1000(또는 비루트) 사용자가 이미 있으면 그 이름을 USER로 채택
```

#### (2) corepack 비인터랙티브 환경에서 GPG 서명 확인 프롬프트

**증상**: `docker build` 가 corepack 단계 직후 `pnpm install` 첫 호출에서 hang 또는 timeout. CI 로그에는 다음 류가 보일 수 있음:
```
! Corepack is about to download https://registry.npmjs.org/pnpm/-/pnpm-X.Y.Z.tgz
? Do you want to continue? [Y/n]
# (TTY 없어 stdin 닫혀 무한 대기)
```

**원인**: Node ≥ 16.13의 corepack이 pnpm/yarn 다운로드 시 GPG 서명 확인 도입. node:22-alpine 등 최신 베이스에서 기본 활성. `RUN corepack enable`만으로는 *실행 시점*(다음 `pnpm install`)에 프롬프트를 띄움 — Docker build는 TTY가 없어 hang.

**해결 원칙 (stack-agnostic)**: **corepack 사용 시 빌드 단계에서 `corepack prepare <pm>@<version> --activate`로 버전 핀 + pre-fetch 강제**. `--activate` 가 서명 확인까지 빌드 단계에 끌어와 install 호출 시점엔 캐시 hit.

```Dockerfile
# 권장 패턴 (Node monorepo 한정)
FROM node:22-alpine AS build
WORKDIR /workspace
RUN corepack enable && corepack prepare pnpm@9.15.4 --activate
# ↑ pnpm 버전은 packageManager 필드 또는 pnpm-lock.yaml과 정합 (보통 root package.json packageManager: "pnpm@9.15.4")
COPY pnpm-lock.yaml package.json ./
RUN pnpm install --frozen-lockfile
```

**버전 핀 출처**: 다음 셋 중 어느 쪽도 OK:
- (a) `package.json` `packageManager` 필드 (예: `"packageManager": "pnpm@9.15.4"`) — Node 공식 권장
- (b) `pnpm-lock.yaml` 첫 줄 `lockfileVersion` + lockfile 생성 시 pnpm 버전 (lockfile 헤더 comment)
- (c) `.nvmrc` / `package.json` `engines.pnpm` 등 명시 필드

세 곳 중 *한 곳*과 Dockerfile `corepack prepare`의 버전이 정합해야 한다. 불일치 시 lockfile 호환 깨짐.

**Yarn / npm 동치 패턴**: corepack은 pnpm뿐 아니라 yarn에도 동일 영향. `corepack prepare yarn@4.5.0 --activate` 또는 `corepack prepare npm@10.x --activate` 패턴 동일 적용. npm은 Node 베이스에 이미 동봉이라 corepack 우회 가능.

### 1.5.5 multi-stack 의존성 설치 + Gradle/Maven multi-project syntax 함정

> 본 함정은 FE + BE처럼 stack이 다른 multi-stack monorepo, 특히 **Gradle/Maven/sbt/Bazel/Cargo 같은 *parent-aware* 빌드 도구**를 사용할 때 발생. 단일 stack은 N/A.
> 원인: LLM 학습 분포의 다수가 *multi-project root build*(루트에 wrapper + parent settings/pom이 module을 `include`)라서, *standalone module build*(wrapper가 module 안 + parent 설정 없음) 구조에서도 multi-project syntax(`:module:task` · `-pl module` 등)를 자동 적용. 결정적 fail. (ADR-0043)

#### (1) 멀티 stack은 stack별로 1줄씩, 각 wrapper/CLI는 자기 위치에서

원칙: **각 stack의 wrapper/CLI는 *자기 디렉토리*에서 실행되는 게 기본**. 셸 자동 cwd 이동(`cd module && ...`) 또는 빌드 도구의 cwd 명시 플래그(`-p` · `-pl` 등) 사용.

```bash
# 권장 — multi-stack monorepo의 의존성 설치 (각 stack별로 1줄)
pnpm install --frozen-lockfile                              # FE (pnpm-workspace.yaml이 루트면 루트에서 OK)
(cd backend && ./gradlew dependencies)                      # BE — module cwd에서 직호출 (subshell로 cwd 격리)
# 또는: ./backend/gradlew -p backend dependencies            # BE — -p 플래그로 명시 (cwd 이동 없이)
```

**금지 패턴 (standalone module에서 깨짐)**:
```bash
./gradlew :backend:dependencies   # ❌ 루트에 ./gradlew 없으면 "No such file or directory"
                                  # ❌ standalone(rootProject.name="backend") 구조면 ":backend"가 자기 자신을 가리켜 Gradle 에러
                                  #    "Project 'backend' not found in root project 'backend'."
```

#### (2) Gradle wrapper + settings.gradle 위치 점검 3축

Dockerfile/LOCAL.md 작성 *전*에 1회 실행해 구조를 명확히 한 뒤 호출 패턴 결정:

```bash
# 축 1 — wrapper 위치 확인
find . -name "gradlew" -not -path "*/node_modules/*" -not -path "*/build/*" 2>/dev/null
# 결과 해석:
#   ./gradlew              → 루트 build (multi-project일 가능성)
#   ./backend/gradlew      → backend 안 (standalone 또는 backend 자체가 부분 root)

# 축 2 — rootProject.name 확인
cat <gradlew 위치>/settings.gradle* 2>/dev/null | grep -E 'rootProject.name|^include'
# 결과 해석:
#   rootProject.name = "<repo-name>" + include 'backend' → multi-project root build
#   rootProject.name = "backend" + include 없음            → standalone module build (backend가 자기 자신의 root)

# 축 3 — 호출 패턴 결정
```

| 구조 | 판정 근거 | 의존성 설치 호출 | 부팅 호출 예 |
|---|---|---|---|
| **multi-project root build** | 루트에 `gradlew` + `settings.gradle`이 `include 'backend'` 포함 | `./gradlew :backend:dependencies` (루트에서) | `./gradlew :backend:bootRun` |
| **standalone module build** | wrapper가 `backend/` 안 + `backend/settings.gradle*`의 `rootProject.name = "backend"` (include 없음) | `(cd backend && ./gradlew dependencies)` 또는 `./backend/gradlew -p backend dependencies` | `(cd backend && ./gradlew bootRun)` 또는 `./backend/gradlew -p backend bootRun` |

#### (3) Maven / sbt / Bazel / Cargo 동치 함정 (stack-agnostic)

| 빌드 도구 | multi-project syntax (작동 조건) | standalone에서 깨지는 패턴 |
|---|---|---|
| Gradle | `./gradlew :backend:bootRun` (parent `settings.gradle`이 `include 'backend'`) | `Project ':backend' not found in root project '...'` |
| Maven | `mvn -pl backend install` (parent `pom.xml`의 `<modules>`에 `<module>backend</module>`) | `[ERROR] Could not find specified profile (-pl)` 또는 reactor 미인식 |
| sbt | `sbt "project backend" run` (root `build.sbt`에 `lazy val backend = project.in(file("backend"))`) | `Not a valid project ID: backend` |
| Bazel | `bazel build //backend:lib` (`WORKSPACE`가 루트, `backend/BUILD` 존재) | `no such package 'backend'` |
| Cargo (Rust) | `cargo build -p backend` (root `Cargo.toml`의 `[workspace] members = ["backend"]`) | `package(s) 'backend' not found in workspace` |

원칙: **wrapper/CLI가 module 안에 있고 parent 설정이 module을 포함하지 않으면, module 자체가 root이고 multi-project syntax는 미존재 경로**.

본 프로젝트 채택: `{{multi-project root build / standalone module build / 단일 stack(N/A) 중 1개}}`
- 채택 호출 패턴: `{{예: ./gradlew :backend:dependencies (multi-project) / (cd backend && ./gradlew dependencies) (standalone) / N/A}}`

---

## 2. 처음 한 번 셋업 (Initial Setup)

```bash
# 1) clone
git clone <repo-url>
cd <repo-name>

# 2) 의존성 설치
#    멀티 stack인 경우 각 stack의 wrapper/CLI를 *그 위치*에서 호출 (§1.5.5).
#    Gradle/Maven 채택 시 wrapper 위치 + settings.gradle (또는 pom.xml `<modules>`) 검사 후 결정:
#      - multi-project root build (parent가 module을 include): `./gradlew :module:task`
#      - standalone module build (wrapper가 module 안 + parent 설정 없음): `(cd module && ./gradlew task)` 또는 `./module/gradlew -p module task`
{{설치 명령 — 단일 stack 예: `pnpm install --frozen-lockfile`. 멀티 stack 예: 각 stack별로 1줄씩 — `pnpm install --frozen-lockfile` + `(cd backend && ./gradlew dependencies)` 또는 `./backend/gradlew -p backend dependencies`}}

# 3) 환경 변수 파일 준비 — profile별로 1벌씩
#
#    §1.5.1 채택 패턴에 따라 분기:
#
#    (단일 패키지 / (a)~(d) 채택 — 루트 .env 사용):
cp .env.dev.example  .env.dev
cp .env.stg.example  .env.stg
cp .env.prod.example .env.prod
#
#    (e) 채택 시 — 워크스페이스별 .env 완전 분리 (워크스페이스 N개면 N*3벌):
# cp frontend/.env.dev.example  frontend/.env.dev
# cp frontend/.env.stg.example  frontend/.env.stg
# cp frontend/.env.prod.example frontend/.env.prod
# cp backend/.env.dev.example   backend/.env.dev
# cp backend/.env.stg.example   backend/.env.stg
# cp backend/.env.prod.example  backend/.env.prod
#
# 각 .env.{dev,stg,prod} 안의 시크릿(JWT_SECRET·DB_PASSWORD 등)을 실제 값으로 채움
# 각 profile별로 다른 값 사용 권장. JWT_SECRET은 알고리즘이 요구하는 최소 길이 준수 (HS256 = 32자)

# 4) DB 스키마 적용 (dev profile, 최초 1회) — §1.5.2 분류에 따라 분기
# (a) 분리형 채택 시 — dev 빠른 동기 + 정식 migration 분리 호출:
{{최초 dev 셋업 명령 — 예: pnpm prisma:push:dev    # = prisma db push --skip-generate}}
# 정식 migration 흐름 시작 (최초 1회만, 이후엔 stg/prod에서 migrate 사용):
#   {{예: pnpm migrate:init    # = prisma migrate dev --name init}}
# ⚠️ 함정: 'migrate deploy'·'flyway migrate' CLI 류는 *기존 migration 파일만* 적용.
#    migrations/ 비어 있으면 DB 빈 상태로 남음.
#
# (b) 단일 메커니즘(부팅 통합) 채택 시 — 별도 명령 없음. §3 dev 부팅이 곧 migrate:
#   예) Spring Boot + Flyway integration: `./gradlew bootRun --args='--spring.profiles.active=dev'`
#       부팅 로그에서 `Flyway Community Edition ... by Redgate` + `Migrating schema "public" to version "X"` 확인
#   ⚠️ 함정: `./gradlew flywayMigrate` 같은 Gradle 태스크 호출 금지 — 그 태스크는 별도 `org.flywaydb.flyway`
#           플러그인 도입 시에만 존재하고 Spring Boot의 `spring.flyway.*` 설정과 별 컨피그 필요.
#           Spring Boot가 부팅 시 자동 적용하므로 redundant.
#
# (c) N/A 채택 시 — 이 단계 자체 skip

# 5) seed 데이터 (dev profile)
{{seed 명령 — 예: pnpm seed:dev    # monorepo는 dotenv -e ../.env.dev -- 래핑됨, §1.5.1}}
```

---

## 3. Profile별 부팅 명령

> **profile 3분기 강제 (ADR-0037 v1.1)** — 매 PR에서 3 profile 모두 부팅 검증된다. 본 절의 명령이 그대로 AI 게이트 6번째 축에서 실행된다.

### 3.1 dev profile (로컬 개발)

```bash
# 단일 패키지 / (a)~(d) 채택 — 단일 명령
{{dev 부팅 명령 — 예: pnpm dev:local / SPRING_PROFILES_ACTIVE=dev ./gradlew bootRun}}

# (e) 채택 — 워크스페이스 분리 시 2 변형 권고
# 옵션 A: 워크스페이스 직접 실행 (각 워크스페이스 1터미널씩 — hot reload O)
#   {{예: SPRING_PROFILES_ACTIVE=dev ./gradlew :backend:bootRun        # 8080}}
#   {{예: pnpm --filter @app/frontend dev                                # 5173}}
# 옵션 B: docker-compose (DB 포함 통합 기동 — N개 워크스페이스를 1명령으로)
#   {{예: docker compose -f docker-compose.dev.yml --env-file backend/.env.dev up}}
```

- 기대 출력: `{{ready 신호 — 예: :3000 listening / Started ConduitApplication ... profile [dev]}}`
- 환경 변수 출처: `.env.dev` *(또는 (e) 채택 시: `{{workspace}}/.env.dev` 워크스페이스 수만큼)*
- DB: `{{dev DB 위치 — 예: localhost:5432/myapp_dev}}`
- Hot reload: {{O / X}}

### 3.2 stg profile (스테이징 — 로컬에서 stg 환경 흉내)

```bash
# 빌드 → 실행 (stg는 빌드 산출물 기반, watch 모드 없음)
{{빌드 명령 — 예: pnpm build / ./gradlew build / poetry build}}

# 단일 패키지 / (a)~(d) 채택 — 단일 실행
{{stg 실행 명령 — 예: pnpm start:stg / SPRING_PROFILES_ACTIVE=stg java -jar build/libs/app.jar}}

# (e) 채택 — 워크스페이스 분리 시 2 변형:
# 옵션 A: 로컬 실행 (각 워크스페이스 1터미널)
#   {{backend — 예: SPRING_PROFILES_ACTIVE=stg java -jar backend/build/libs/app.jar    # 8080}}
#                  또는 Node: dotenv -e backend/.env.stg -- node backend/dist/server.js
#   {{frontend 정적 (SPA만) — 예: pnpm --filter @app/frontend exec vite preview --port 4173}}
# 옵션 B: docker-compose (canonical — workspace별 .env.stg를 compose env_file로 주입)
#   {{예: docker compose -f docker-compose.stg.yml --env-file backend/.env.stg up}}
```

- 기대 출력: `{{ready 신호 — 예: :3000 listening / Started ... profile [stg] / Accepting connections at http://localhost:4173}}`
- 환경 변수 출처: `.env.stg` *(또는 (e) 채택 시: `backend/.env.stg` + `frontend/.env.stg` 등 워크스페이스 수만큼)*
- DB: `{{stg DB 위치 — 또는 'dev DB 공유' 명시}}`
- Hot reload: 보통 X (빌드 산출물 기반)
- ⚠️ 흔한 함정 (§1.5.3 참조): `serve` 같은 별 정적 서버 미설치 / `NODE_ENV=staging`만 inline 셋팅 시 다른 env 누락 → 빌드 도구 기본 preview + `dotenv -e .env.stg` 권장. JWT_SECRET 등 시크릿 평문 금지 — env injection
- **단일 환경 운영 시**: 본 절을 "N/A — stg=prod 공유 운영"으로 표기

### 3.3 prod profile (로컬에서 prod 환경 흉내)

```bash
{{빌드 명령 — 예: pnpm build / ./gradlew build}}

# 단일 패키지 / (a)~(d) 채택 — 단일 실행
{{prod 실행 명령 — 예: pnpm start:prod / SPRING_PROFILES_ACTIVE=prod java -jar build/libs/app.jar}}

# (e) 채택 — 워크스페이스 분리 시 2 변형:
# 옵션 A: 로컬 실행
#   {{backend — 예: SPRING_PROFILES_ACTIVE=prod java -jar backend/build/libs/app.jar
#               또는 Node: dotenv -e backend/.env.prod -- node backend/dist/server.js}}
#   {{frontend 정적 (SPA만) — 예: pnpm --filter @app/frontend exec vite preview --port 4173}}
# 옵션 B: docker-compose (canonical)
#   {{예: docker compose -f docker-compose.prod.yml --env-file backend/.env.prod up}}
```

- 기대 출력: `{{ready 신호}}`
- 환경 변수 출처: `.env.prod` *(또는 (e) 채택 시: 워크스페이스별 `.env.prod`)*
- DB: `{{prod DB 위치 — 보통 별 인스턴스 권장. secret manager(Vault·Doppler·AWS Secrets Manager) 권장, .env.prod는 placeholder만 commit}}`
- Hot reload: X (빌드 산출물)
- **단일 환경 운영 시**: N/A 표기

---

## 4. 부팅 자산 (Runnability Assets)

> 본 표는 `docs/planning/12-scaffolding/<lang>.md` §7과 동기 (다국어 시 lang별 파일 모두). 자산이 변경되면 양쪽 모두 갱신.

| 자산 | 경로 | 변경 trigger | 갱신 책임 |
|---|---|---|---|
| 환경 변수 템플릿 | `.env.{dev,stg,prod}.example` *(또는 (e) 채택 시 워크스페이스별 — 예: `frontend/.env.{p}.example` + `backend/.env.{p}.example` 등 N\*3종, footnote ★1)* | 새 환경 변수 추가 | 변수를 도입한 이슈 |
| 스키마 적용 (dev iteration) | `{{(a) 분리형: 예 backend/package.json scripts.prisma:push:dev / SQLAlchemy create_all / Alembic upgrade head — 또는 (b) 단일 메커니즘: 'bootRun (spring.flyway.enabled=true 자동 적용)' / 'Database.Migrate() on startup' — 또는 (c) N/A}}` | dev 환경 schema 변경 | 모델 변경 이슈 |
| DB migrations (stg/prod release) | `{{(a) 분리형: 예 backend/prisma/migrations/ + migrate deploy / flyway CLI migrate / alembic upgrade head — 또는 (b) 단일 메커니즘: 예 backend/src/main/resources/db/migration/V*.sql (적용은 stg/prod bootRun이 자동) — 또는 (c) N/A}}` | 운영 release용 migration 작성·적용 | 운영 release 이슈 |
| lockfile | `{{pnpm-lock.yaml · poetry.lock · go.sum · gradle.lockfile 등}}` *(풀스택 monorepo는 여러 lockfile 공존 — 워크스페이스별로 1행씩 추가 권장. 예: `frontend/pnpm-lock.yaml` + `backend/gradle.lockfile`, footnote ★2)* | 의존성 추가/변경 | 의존성 도입 이슈 |
| 설치/seed scripts | `{{예: package.json scripts.{setup,migrate,seed:dev,seed:stg,seed:prod} / build.gradle tasks.seed* / pyproject scripts.*}}` | seed 데이터 변경 | seed 변경 이슈 |
| 부팅 명령 | 본 LOCAL.md §3 + `{{빌드 도구 manifest의 dev/start scripts}}` | 명령 변경 | 명령 변경 이슈 |
| 컨테이너 정의 (선택) | `Dockerfile`·`docker-compose.{dev,stg,prod}.yml` *(multi-image 시 `Dockerfile.<svc>` 분리 — 예: `Dockerfile.api` + `Dockerfile.web`)* | infra 변경 | infra 이슈 |

> **★1 monorepo 분리 footnote**: §1.5.1 (e) 워크스페이스별 .env 완전 분리 채택 시, "환경 변수 템플릿" 행을 워크스페이스 수만큼 분리해서 1행씩 추가한다 (예: FE 행 + BE 행). 단일 패키지 또는 (a)~(d) 채택은 단일 행 유지. AI 게이트 6번째 축이 *모든* `.env.{p}.example` 파일과 LOCAL.md 본문의 정합을 lint한다.
> **★2 lockfile footnote**: 워크스페이스별로 stack이 다르면 lockfile도 분리(예: pnpm + Gradle + uv 혼합 시 3개). 모두 commit + AI 게이트가 누락된 lockfile 갱신을 BLOCK한다.
> **단일 메커니즘(b) 채택 시 footnote**: "스키마 적용" + "DB migrations" 두 행에 별 명령을 넣지 않음. 양쪽 모두 §3 부팅 명령 참조 + migration 파일 디렉토리 명시. 예: 본 LOCAL.md §3 `./gradlew bootRun --args='--spring.profiles.active=*'` + `src/main/resources/db/migration/V*.sql`. **Spring Boot 프로젝트에서 `./gradlew flywayMigrate` 같은 별 Gradle 태스크 작성 금지** — 그 태스크는 별도 `org.flywaydb.flyway` 플러그인 도입 시에만 존재하고, integration은 부팅 자체가 migrate를 수행 (ADR-0037 §2.7).

---

## 5. 자주 발생하는 문제 (Troubleshooting)

> newProject 도입 후 부팅 시 발견되는 문제를 *이슈 단위*로 본 절에 누적. AI 게이트 6번째 축이 부팅 실패를 BLOCK하지만, *해결 방법*은 본 절이 정본.

### 5.1 포트 충돌 (`EADDRINUSE`)

```bash
{{포트 사용 중 프로세스 확인 명령 — 예: lsof -i :3000}}
```

### 5.2 환경 변수 누락 (`X is required`)

해당 변수가 `.env.{dev,stg,prod}.example` **모든 .example 파일**에 정의됐는지 확인. profile 동기 누락이 가장 흔한 패턴.
- 단일 패키지 / (a)~(d) 채택: 3벌 (`.env.{dev,stg,prod}.example`)
- (e) 채택 — 워크스페이스 분리: **워크스페이스 수 × 3벌** (예: FE+BE 2개 워크스페이스면 6벌, FE+BE+worker 3개면 9벌)
- 짧은 시크릿 함정: `JWT_SECRET` 등은 알고리즘 최소 길이(HS256 = 32자) 미만 시 `WeakKeyException` 류 에러

### 5.3 DB 연결 실패

- DB 컨테이너 실행 여부: `docker compose ps`
- profile별 DB URL 일치 여부: `.env.{dev,stg,prod}` 안의 `DATABASE_URL`
- 스키마 미적용 (§1.5.2 채택 분류에 따라 진단):
  - (a) 분리형 채택 시 — dev: `{{예: pnpm prisma:push:dev}}` (또는 최초 1회 정식 흐름 `{{예: pnpm migrate:init}}`). stg/prod: `{{예: pnpm migrate}}` (기존 파일만 적용)
  - (b) 단일 메커니즘 채택 시 — 부팅 로그에서 자동 적용 확인. 예: Spring Boot + Flyway integration이면 `Flyway Community Edition X.Y.Z by Redgate` + `Migrating schema "public" to version "X"`. 둘 다 없으면 `spring.flyway.enabled` + `spring.jpa.hibernate.ddl-auto` 설정 점검. **`./gradlew flywayMigrate` 같은 별 호출 시도 금지** — 그 태스크는 별 plugin이 필요하고 redundant
  - (c) N/A — DB 자체가 없는 구조

### 5.4 monorepo cwd에서 `DATABASE_URL not found` (또는 다른 env 누락)

> §1.5.1 함정의 사후 발현 — 한 번 막혔다면 본 절로 빠르게 진단.

증상 (스택별 사례):
```
# Node + Prisma
$ cd backend && npx prisma migrate deploy
Error: Environment variable not found: DATABASE_URL.

# Java + Spring (유사 패턴)
$ cd backend && ./gradlew bootRun
... Could not resolve placeholder 'database.url' ...

# Python + SQLAlchemy
$ cd backend && python -m alembic upgrade head
... KeyError: 'DATABASE_URL' ...
```

원인: backend cwd에서 도구를 직접 호출하면 root `.env.{profile}`이 자동 로드되지 않음. backend 자체 env 설정이 없으니 변수 누락.

해결: **워크스페이스 cwd에서 빌드 도구·ORM CLI를 직접 호출하지 말 것**. 항상 root에서 §1.5.1 채택 패턴으로 호출 — 스크립트/run 명령이 root env를 명시 로드함.
- 채택 패턴 확인: `{{본 newProject 채택 패턴 (a)/(b)/(c)/(d)와 적용 위치를 명시}}`
  - 예 (Node + dotenv-cli): `backend/package.json scripts.prisma:*` 가 `dotenv -e ../.env.{profile} --` 로 래핑됐는지
  - 예 (Java + Spring): `SPRING_PROFILES_ACTIVE` env 또는 `--spring.profiles.active=` 플래그가 설정됐는지
  - 예 (Python + Pydantic settings): `Settings(_env_file="../.env.dev")` 등으로 root env 경로 명시했는지

### 5.5 컨테이너 베이스 이미지 함정 (Dockerfile 작성 시 — ADR-0042)

> §1.5.4 사전 안내의 사후 발현. 본 절은 *처음 docker build를 깨뜨린 시점*에 빠르게 진단·해결하는 용도.

#### (a) `useradd: UID 1000 is not unique` / `user '...' already exists`

증상:
```
$ docker build -f Dockerfile.api .
...
=> ERROR [runtime 3/4] RUN useradd --uid 1000 --create-home --shell /bin/bash app
useradd: UID 1000 is not unique
```

진단:
```bash
# 해당 베이스 이미지가 사전 점유한 사용자 확인
docker run --rm --entrypoint sh <base-image> -c 'cat /etc/passwd | tail -5'
# UID 1000(또는 비루트) 사용자가 보이면 §1.5.4 표 참조
```

해결: `RUN useradd ...` 라인 제거 + `USER <existing-user>` 직접 사용. eclipse-temurin Ubuntu base는 `USER ubuntu` / node base는 `USER node` / distroless `:nonroot`는 `USER nonroot`.

#### (b) corepack 단계 hang / `Do you want to continue? [Y/n]` 무한 대기

증상:
```
$ docker build -f Dockerfile.web .
...
=> [build 3/8] RUN corepack enable
=> [build 4/8] RUN pnpm install --frozen-lockfile
# (이 단계에서 timeout 또는 무한 hang — 종종 ~10분 대기 후 fail)
```

진단: 베이스가 `node:*` + corepack을 enable만 하고 *버전 핀 없이* 다음 단계에서 pnpm/yarn 호출하는 패턴인지 Dockerfile 점검.

해결: `RUN corepack enable` → `RUN corepack enable && corepack prepare pnpm@X.Y.Z --activate`. 버전은 `package.json` `packageManager` 필드 또는 lockfile 헤더 comment와 정합 (§1.5.4 (2) 표).

### 5.6 multi-stack 의존성 설치 / Gradle multi-project syntax 함정 (ADR-0043)

> §1.5.5 사전 안내의 사후 발현. `LOCAL.md §2 단계 2 의존성 설치`를 그대로 카피했는데 깨지는 경우.

#### (a) `bash: ./gradlew: No such file or directory`

증상: 프로젝트 루트에서 `./gradlew :backend:dependencies` 실행 시 즉시 fail.

진단:
```bash
find . -name "gradlew" -not -path "*/node_modules/*" 2>/dev/null
# 결과가 ./backend/gradlew 뿐이면 wrapper가 module 안에 있음 → standalone build 가능성 높음
```

해결: §1.5.5 (2) 표 참조. `(cd backend && ./gradlew dependencies)` 또는 `./backend/gradlew -p backend dependencies`로 전환. 루트의 `LOCAL.md §2` 본문도 동시 갱신.

#### (b) `Project 'X' not found in root project 'Y'.` (Gradle)

증상:
```
$ cd backend && ./gradlew :backend:dependencies
FAILURE: Build failed with an exception.
* What went wrong:
Project 'backend' not found in root project 'backend'.
```

진단: `:backend:dependencies` 의 `:backend`는 *서브프로젝트 경로*인데, `settings.gradle*` 의 `rootProject.name = "backend"` + `include` 없음 → standalone build. `:backend`는 루트 자기 자신을 가리키므로 *서브프로젝트로* 존재하지 않음.

```bash
cat backend/settings.gradle* | grep -E 'rootProject.name|^include'
# rootProject.name = "backend"  + include 라인 없음 → standalone module
```

해결: `:backend:` 접두사 제거 → `./gradlew dependencies` (bare task name). 루트 LOCAL.md §2·§3 본문에서 `:backend:` 접두사를 일괄 제거 (단, parent build 도입할 계획이면 그쪽으로 갈 수도 있음 — 큰 변경이므로 별 이슈).

#### (c) Maven `[ERROR] Could not find specified profile (-pl)` / sbt `Not a valid project ID` / Cargo `package(s) not found in workspace`

증상: 빌드 도구별 동치 함정. §1.5.5 (3) stack-agnostic 표 참조.

해결: parent 설정 파일(pom.xml `<modules>` / build.sbt `lazy val ... = project.in(...)` / Cargo.toml `[workspace] members`)에 해당 module이 포함됐는지 점검. 없으면 multi-project syntax 폐기 + module cwd 직호출로 전환.

### 5.7 (newProject별 추가 — 발견 시점에 본 절에 누적)

---

## 6. 외부 의존 (선택)

> 외부 서비스(Auth0·Stripe·S3 등) 또는 컨테이너 의존이 있으면 본 절에 셋업 절차 명시.

- {{서비스명}}: {{셋업 절차 또는 mock 사용 방법}}

---

## 7. 본 문서 갱신 책임 (메타)

- **누가**: 부팅 자산을 변경하는 이슈의 PR 작성자(에이전트 또는 사람)
- **언제**: 같은 PR 안에서 갱신. 별 hotfix PR로 미루지 않음 (ADR-0037 §2.3)
- **검증**: AI 게이트 6번째 축이 (a) 부팅 자산 diff 여부, (b) 본 LOCAL.md 갱신 여부를 동시 확인. 한쪽만 변경 시 BLOCK
- **상위 SoT 동기**: 본 절차가 12-scaffolding §7과 다르면 `/docs-update`가 정합 검수에서 WARN. 양쪽 동기가 우선
