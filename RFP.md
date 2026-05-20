# RFP — RealWorld 기반 게시판 (Python)

> 작성일: 2026-05-20
> 작성자: 박하은 (woosung.ahn@bespinglobal.com)
> 목적: 웹 개발 뉴비 과제 — RealWorld spec을 베이스로 한 게시판(Article + Comment + Auth)을 Python으로 구현
> 마감: 2026-05-22 (2일)
> 학습 목표: AI 활용 웹 개발 사이클 1회 완주 (요구사항 → 분석 → 설계 → 계획 → 구현 → 테스트 → 검증 → 피드백)

---

## 1. 프로젝트 개요

### 1.1 배경
- 사내 "웹 개발 뉴비 과제" — RealWorld 레퍼런스 앱(Conduit) spec을 활용하여 게시판을 만든다.
- AI 도구(Claude Code + agent-toolkit)를 활용한 풀 사이클 개발 1회 완주가 핵심 학습 목표.
- 결과물은 사용성·퀄리티·퍼포먼스 3축 모두에서 "최적의 방법"으로 구현되어야 함.

### 1.2 참고 자료
- RealWorld 문서: https://realworld-docs.netlify.app/introduction/
- RealWorld GitHub: https://github.com/realworld-apps/realworld
- API 스펙: https://realworld-docs.netlify.app/specifications/backend/endpoints/

### 1.3 산출물
1. 동작하는 게시판 웹 애플리케이션 (로컬 부팅 가능)
2. agent-toolkit 사이클로 생성된 설계 문서 일체 (01~15 + ADR)
3. README / LOCAL.md — 부팅·사용 가이드
4. 단위 테스트 + AI 게이트 통과 증거

---

## 2. 사용자 / 페르소나

| 페르소나 | 역할 | 주요 행동 |
|---|---|---|
| 비회원 방문자 | 게시글 열람만 가능 | 게시글 목록·상세 보기, 댓글 읽기 |
| 가입 사용자 | 글쓴이 / 댓글 작성자 | 회원가입, 로그인, 게시글 CRUD, 댓글 CRUD |

> 1차 학습 과제 범위에서는 관리자 페르소나는 제외 (Out of Scope).

---

## 3. 핵심 기능 (MVP)

> RealWorld spec 중 **게시판 핵심 기능만** 추리고, "팔로우·즐겨찾기·태그 피드"는 시간 여유 시 확장.

### F-01. 사용자 인증 (Auth)
- F-01a. 회원가입 (email + username + password)
- F-01b. 로그인 (email + password) → JWT 발급
- F-01c. 현재 사용자 조회 (`GET /api/user`)
- F-01d. 로그아웃 (클라이언트 측 토큰 폐기로 충분)

### F-02. 게시글 (Article)
- F-02a. 게시글 목록 조회 (페이징 — 기본 20개, `?limit=&offset=`)
- F-02b. 게시글 상세 조회 (slug 기반)
- F-02c. 게시글 작성 (제목, 설명, 본문, 태그 배열) — 로그인 필요
- F-02d. 게시글 수정 — 작성자만
- F-02e. 게시글 삭제 — 작성자만

### F-03. 댓글 (Comment)
- F-03a. 댓글 작성 (게시글 1개에 N개) — 로그인 필요
- F-03b. 댓글 목록 조회 (게시글별)
- F-03c. 댓글 삭제 — 작성자만

### F-04. UI / 화면
- F-04a. 홈 — 게시글 목록
- F-04b. 게시글 상세 페이지 (본문 + 댓글 영역)
- F-04c. 글쓰기 / 수정 폼
- F-04d. 로그인 / 회원가입 폼
- F-04e. 내 프로필 (내가 쓴 글 목록 정도면 충분)

### Out of Scope (1차 제외, 시간 남으면 확장)
- 사용자 팔로우 / 팔로잉 피드
- 게시글 즐겨찾기(favorite) / 좋아요 수
- 태그별 피드 / 인기 태그 사이드바
- 프로필 이미지 업로드
- 비밀번호 찾기 / 이메일 검증
- 다국어 / 다크모드

---

## 4. 비기능 요구사항

### NFR-01. 언어 / 스택 (강제 제약)
- **백엔드 언어: Python 필수** (학습 목표상 변경 불가)
- 프레임워크 선택은 `/flow-design` Phase에서 결정 — 후보: FastAPI / Django / Flask
- 데이터베이스: 게이트 C에서 결정 — 후보: SQLite (개발 편의), PostgreSQL (운영 정합)
- 프론트엔드: 게이트 C에서 결정 — 후보 1) 서버 렌더링(Jinja2 + HTMX), 후보 2) SPA(React/Vue + REST API)
  - 뉴비 학습 + 2일 마감 고려 시 서버 렌더링이 유리하나, 설계 단계에서 트레이드오프 평가 후 확정

### NFR-02. 퍼포먼스
- 게시글 목록 페이지 First Contentful Paint < 1.5초 (로컬 기준)
- API p95 응답 시간 < 200ms (게시글 100건 기준)
- N+1 쿼리 금지 — ORM 사용 시 eager loading 또는 select_related 적용

### NFR-03. 사용성
- 모든 폼 유효성 검증 — 에러 메시지 한글
- 모바일 브라우저 최소 호환 (반응형까지는 강제 아님)
- 페이지 이동 시 깜빡임·로딩 표시 명확

### NFR-04. 보안
- 비밀번호는 bcrypt 등 단방향 해시로 저장 (평문 금지)
- JWT secret은 환경변수로만 — 코드/저장소 커밋 금지 (CLAUDE.md 보안 절대 규칙)
- SQL injection · XSS 방어 (ORM + 템플릿 escape 기본값 신뢰)
- CSRF — 서버 렌더링 채택 시 CSRF 토큰 적용

### NFR-05. 품질
- 단위 테스트 — 핵심 비즈니스 로직(인증·권한·CRUD) 커버리지 ≥ 60%
- 린터 + 포매터 적용 (ruff / black 등 게이트 C에서 결정)
- agent-toolkit AI 게이트 6축 통과

### NFR-06. 운영
- 단일 환경 운영 허용 (dev 1 profile만) — 2일 마감 제약상 dev/stg/prod 3 profile은 N/A로 명시
- 로컬 부팅 가이드(LOCAL.md) 필수 — fresh checkout 후 ≤ 5분 부팅
- GitHub Actions workflow 1개 — pytest 실행 정도면 충분

---

## 5. 제약 / 가정

| 항목 | 값 / 설명 |
|---|---|
| 마감 | 2026-05-22 (2일, 약 16 작업시간) |
| 개발 인력 | 1명 (뉴비) + AI 페어 |
| 언어 | Python (필수) |
| 배포 | 로컬 부팅만 필수, 클라우드 배포는 Out of Scope |
| 외부 의존 | DB 1종 (SQLite/Postgres 중 1), 그 외 외부 API 없음 |
| 라이선스 | RealWorld spec 학습 목적 사용 (코드는 본인 작성) |

---

## 6. 성공 기준 (Definition of Done)

1. `LOCAL.md` §3 부팅 명령으로 fresh checkout → 5분 안에 로컬 서버 부팅
2. 비회원이 게시글 목록·상세를 볼 수 있다
3. 회원가입 → 로그인 → 게시글 작성 → 댓글 작성 → 게시글 수정 → 삭제 시나리오가 브라우저에서 끝까지 동작 (gstack `/qa` 골든패스 통과)
4. 단위 테스트 PASS (커버리지 ≥ 60%, 핵심 로직)
5. agent-toolkit AI 게이트 6축 통과
6. PR 1개 이상이 main에 squash merge 되어 GitHub 히스토리 남음
7. ADR 최소 2건 — (1) 백엔드 프레임워크 선택, (2) 프론트엔드 렌더링 방식 선택

---

## 7. 리스크 / 오픈 이슈

| ID | 리스크 | 영향 | 완화책 |
|---|---|---|---|
| R-01 | 뉴비 + 2일 일정 → 일부 기능 미완성 가능 | Mid | MVP 범위를 작게 잘랐고(Out of Scope 명시), `/flow-wbs`에서 시간 박스 추가 분해 |
| R-02 | 프레임워크 결정 지연 | High | 게이트 C에서 트레이드오프 표 작성 후 사용자 1회 승인으로 확정 |
| R-03 | 인증·권한 로직 보안 결함 | High | bcrypt + JWT + `/cso` 보안 점검 통과 강제 |
| R-04 | 퍼포먼스 NFR-02 미달 | Low | 게시글 100건 시드 + 인덱스 + 페이징 강제 |

---

## 8. 다음 단계

1. (사용자) 본 RFP 검토 / 수정 요청
2. `bash agent-toolkit/scripts/install.sh c:\Users\박하은HaeunPark\realworld-py` — 툴킷 도입
3. `cd c:\Users\박하은HaeunPark\realworld-py && /flow-init` — Phase 1 (의도·요구) 진입
4. 이후 `/flow-design` → `/flow-wbs` → `/flow-bootstrap` 순으로 NEW_PROJECT 4 Phase 진행
