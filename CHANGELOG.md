# Changelog

본 프로젝트는 [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/) 형식을 따른다. 버전은 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)을 따른다.

## [0.1.0] - 2026-05-21

**First release** — AI 페어 개발 학습 과제(2026-05-20~2026-05-21, 2일 ~16h) 사이클 완주. Sprint 1·2 × 10 이슈 모두 머지.

### Added — Backend (FastAPI + Python 3.11)

- 워크스페이스 스캐폴딩 + uv + Alembic + pytest 인프라 (#11, I-01)
- User 모델 + UserRepo + Alembic 0002 add_users (#12, I-02)
- AuthService(register/authenticate/get_current_user) + bcrypt + JWT(HS256) + require_auth middleware (#13, I-03)
- Article + Tag M2M 모델 + Alembic 0003 + ArticleRepo selectinload N+1 회피 + ArticleService 5 메서드 + slug util + 8 라우트(users 3 + articles 5) + RealWorldError handler (#14, I-04)
- 멱등 seed scripts(User 10 + Article 100 + Tag 5) + R-N-01 p95 측정 통합 테스트 — **p50=3.28ms p95=4.24ms (threshold 200ms, 마진 ~47배)** (#15, I-05)
- Comment 모델(article_id FK CASCADE + author lazy=joined) + Alembic 0004 + CommentRepo + CommentService + 4 라우트(R-F-13 PUT 비표준 포함) + CASCADE 검증 통합 테스트 (#16, I-06)

### Added — Frontend (React + Vite + TypeScript + Tailwind)

- 워크스페이스 스캐폴딩 + Vite 5.4 + React 18.3 + TS 5.6 strict + Tailwind 3.4 + react-router-dom 6.28 + zustand 4.5 + npm 11 채택 + 6 라우트 placeholder + Header + api/client + auth store + Vite proxy `/api → :8000` (#17, I-07)
- LoginPage·RegisterPage 실 폼(controlled inputs + 422 한글 에러 인라인) + Header 로그인 상태 분기 + App mount loadFromStorage + ErrorBody·extractErrorMessage 헬퍼 (#18, I-08)
- HomePage(목록+페이지네이션+4 상태) + ArticlePage(본문+댓글 UI+작성자 액션+삭제 모달) + EditorPage(새 글+수정 분기) + ProfilePage(author 필터) + ArticleCard·CommentItem(인라인 편집)·Modal 3 컴포넌트 + 골든패스 7단계 E2E + R-N-02 FCP + R-N-05 XSS 시도 (#19, I-09)

### Added — Infra & Docs

- agent-toolkit + 14 planning artifacts (Gate A/B/C + WBS) + 4 ADR — initial import (#11에 포함)
- LOCAL.md v0.3 (5분 부팅 가이드 + 함정 안내 + Troubleshooting) — Issue #7에서 npm 채택 반영
- README.md + CHANGELOG.md v0.1.0 + retro `2026-05-21-cycle.md` — 본 PR I-10 사이클 종료

### Testing

- backend pytest **77 passed** (3 health + 42 unit + 32 integration)
- frontend `npm run build` 60 modules in ~1.5s + CSS 10.91KB gzip 2.70KB
- R-N-06 커버리지 ≥80% (`--cov-fail-under=80` 정착, I-04)

### Security

- `.env` 파일 git 미포함 (workspace-별 `.env.example`만 commit)
- JWT 평문 · JWT_SECRET 평문 git 0건
- CORS_ORIGINS=`http://localhost:5173` (wildcard `*` 미사용)
- bcrypt password hashing + Pydantic input validation + SQLAlchemy ORM (SQLi 차단) + React JSX escape (XSS 차단)

### Out of Scope (next cycle 후보)

- 팔로우 · 즐겨찾기 · 태그 피드 (RFP §5)
- 마크다운 렌더링 · 이미지 업로드 · 검색
- 다국어 i18n · 다크모드
- 컨테이너(Docker) · 클라우드 배포
- 단위 테스트 frontend (Vitest)

[0.1.0]: https://github.com/haeunpark-623/realworld-py/releases/tag/v0.1.0