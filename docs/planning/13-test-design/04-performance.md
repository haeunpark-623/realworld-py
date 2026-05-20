---
doc_type: test-design
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: [R-N-01, R-N-02, R-N-03, R-N-04, R-N-05]
  F-ID: []
  supersedes: null
---

# 13-test-design / 04-performance — Performance & Security Tests

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, R-N-01·R-N-02 성능 + R-N-03~R-N-05 보안) |

## 1. 성능 테스트

### 1.1 R-N-01 — API p95 < 200ms (게시글 목록 100건 시드)

- **목표**: `GET /api/articles?limit=20` p95 응답시간 < 200ms
- **시점**: PR 단계 통합 테스트로 실행. dev 매 커밋엔 미실행 (시간 가변성)
- **시나리오**:
  1. `tests/integration/test_performance.py::test_articles_list_p95` 진입
  2. 게시글 100건 시드 (factory로 생성)
  3. `httpx.AsyncClient.get('/api/articles?limit=20')` 100회 호출, 각 호출 시간 측정
  4. `statistics.quantiles(times, n=20)[18]` (p95) 계산 → < 200ms 검증
- **fail 시 대응**:
  - SQLAlchemy 쿼리에 `selectinload(Article.author)` 추가 (N+1 회피)
  - `articles.created_at` 인덱스 추가
  - `articles.slug` UNIQUE 인덱스 추가 (이미 모델에 선언)
- **도구**: pytest + httpx + statistics (stdlib)

### 1.2 R-N-02 — FCP < 1.5s (게시글 목록 페이지)

- **목표**: 게시글 목록 페이지(http://localhost:5173) FCP < 1500ms (로컬 dev 서버 기준)
- **시점**: PR 단계 gstack `/qa` Performance 트레이스 1회
- **시나리오**:
  1. `pnpm dev` (프론트엔드 dev 서버 부팅)
  2. `uv run uvicorn ...` (백엔드 부팅)
  3. 백엔드 100건 시드
  4. gstack `/qa`로 http://localhost:5173 진입 + Performance 트레이스 측정
  5. FCP 메트릭 < 1500ms 확인
- **fail 시 대응**:
  - React.lazy로 페이지별 chunk 분리 (S-02·S-03·S-06 등)
  - 게시글 카드 컴포넌트의 첫 paint 최소화
  - 이미지·아이콘 SVG 인라인
- **도구**: gstack `/qa` (Chrome DevTools Performance)

## 2. 보안 테스트

### 2.1 R-N-03 — 비밀번호 bcrypt 저장 검증

- **목표**: 회원가입 후 DB의 `users.password_hash` 컬럼이 `$2b$` 마커로 시작
- **시점**: 단위 + 통합 매 회귀
- **시나리오**:
  - 단위: `hash_password("plain")` 결과가 `$2b$`로 시작 검증
  - 통합: `POST /api/users` 후 `SELECT password_hash FROM users WHERE email=...`로 직접 조회 + 형식 검증
- **fail 시 대응**: passlib `CryptContext(schemes=["bcrypt"])` 설정 점검. 라이브러리 다운그레이드 / 미설치 가능성
- **도구**: pytest (단위·통합)

### 2.2 R-N-04 — 시크릿 환경변수 누락 시 부팅 실패

- **목표**: `JWT_SECRET` 환경 변수 미설정 시 부팅 단계에서 명시적 예외
- **시점**: PR 단계 + `/cso` 보안 점검
- **시나리오**:
  - 단위: `Settings()` 인스턴스 생성 시 환경변수 없으면 `ValidationError`
  - 통합: TestClient 생성 시 환경변수 monkeypatch 제거 → 부팅 실패 확인
  - `/cso` (gstack): git grep으로 `JWT_SECRET=eyJ...` 류 평문 시크릿 패턴 0건 확인
- **fail 시 대응**: pydantic-settings의 `Field(...)` 필수 선언 점검. .env에 placeholder만 commit
- **도구**: pytest + `/cso` (gstack)

### 2.3 R-N-05 — XSS / SQL injection 안전성

- **XSS 목표**: 본문에 `<script>alert(1)</script>` 작성 시 브라우저에서 alert 미발화
- **SQL injection 목표**: 임의 입력에 `'; DROP TABLE articles; --` 패턴 포함 시 DB 무결성 영향 없음
- **시점**: PR 단계 통합 + gstack `/qa` E2E 1회
- **시나리오**:
  - 통합 (XSS): `POST /api/articles` body에 XSS 페이로드 → `GET /api/articles/{slug}` 응답에 페이로드 그대로 (저장은 원본). 응답 자체는 escape 안 함이 RealWorld spec
  - 통합 (SQLi): query parameter나 body에 SQL injection 페이로드 → SQLAlchemy 파라미터 바인딩으로 무력화. 후속 `GET /api/articles` 정상 응답으로 DB 무결성 확인
  - E2E (XSS): gstack `/qa`로 글 작성 → 상세 페이지 진입 → alert 미발화 확인 (React JSX 기본 escape)
- **fail 시 대응**:
  - SQLAlchemy raw SQL 사용 부위 점검 (현 정책 raw SQL 금지, 11-coding-conventions §3.3)
  - 프론트엔드 `dangerouslySetInnerHTML` 사용 부위 0건 확인
- **도구**: pytest (통합) + gstack `/qa` (E2E)

### 2.4 보안 추가 점검 (`/cso` 권고)

본 프로젝트 학습 컨텍스트에서 추가로 `/cso` 보안 점검이 다음 항목을 매 PR마다 확인:

- `.env` 파일 또는 시크릿 패턴(`JWT_SECRET=eyJ...`, `password=...`) 평문 commit 0건
- `passlib` 등 보안 라이브러리 버전이 GitHub Security Advisory에 등재된 취약 버전 아닌지
- `CORS_ORIGINS` 환경변수가 `*` (모든 출처 허용) 아닌지 — 본 프로젝트는 `http://localhost:5173` 만
- JWT secret 길이 ≥ 32자 (HS256 최소)

## 3. 도구·시점

| 종류 | 도구 | 시점 | R-ID |
|---|---|---|---|
| API p95 측정 | pytest + httpx + statistics | PR 단계 통합 | R-N-01 |
| FCP 측정 | gstack `/qa` Performance | PR 단계 E2E 1회 | R-N-02 |
| bcrypt 형식 검증 | pytest 단위·통합 | 매 회귀 | R-N-03 |
| 시크릿 미설정 부팅 실패 | pytest 단위·통합 | 매 회귀 | R-N-04 |
| 시크릿 평문 commit 점검 | `/cso` (gstack) | PR 단계 | R-N-04 |
| XSS 페이로드 안전성 | pytest 통합 + gstack `/qa` | PR 단계 | R-N-05 |
| SQL injection 안전성 | pytest 통합 | 매 회귀 | R-N-05 |
| 보안 라이브러리 취약 버전 점검 | `/cso` | PR 단계 | R-N-04 |
