---
doc_type: coding-conventions
version: v0.1 (Draft)
status: Draft
author: woosung.ahn@bespinglobal.com
date: 2026-05-20
gate: C
related:
  R-ID: [R-N-03, R-N-04, R-N-05, R-N-06]
  F-ID: [F-01, F-02, F-03]
  supersedes: null
---

# realworld-py — Coding Conventions

## 변경 이력

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-05-20 | woosung.ahn@bespinglobal.com | 초안 (`/flow-design` Phase 2/4, Python + FastAPI + React/Vite 양 stack 컨벤션) |

## 1. 명명 규칙

| 항목 | 규칙 | 예 |
|---|---|---|
| Python 파일명 | `snake_case.py` | `auth_service.py`, `article_router.py` |
| Python 모듈/패키지 | `snake_case` | `realworld.services.auth` |
| Python 클래스 | `PascalCase` | `AuthService`, `ArticleRepo`, `UserCreateSchema` |
| Python 함수·메서드 | `snake_case` | `register_user()`, `get_by_slug()` |
| Python 상수 | `UPPER_SNAKE_CASE` | `JWT_EXP_SECONDS`, `DEFAULT_LIMIT` |
| Python private | 선행 `_` | `_hash_password()`, `_generate_slug()` |
| Pydantic 스키마 | `<Domain><Action>Schema` 또는 `<Domain>Response` | `UserCreateSchema`, `ArticleResponse` |
| SQLAlchemy 모델 | 단수형 `PascalCase` | `User`, `Article`, `Comment`, `Tag` |
| SQLAlchemy 테이블 | 복수형 `snake_case` | `users`, `articles`, `comments`, `tags` |
| DB 컬럼 | `snake_case` | `password_hash`, `created_at`, `author_id` |
| FastAPI 라우터 | `<domain>_router` | `users_router`, `articles_router` |
| React 컴포넌트 | `PascalCase.tsx` | `ArticleCard.tsx`, `CommentItem.tsx` |
| React 훅 | 선행 `use` + camelCase | `useAuth`, `useArticles` |
| TypeScript 인터페이스/타입 | `PascalCase` | `Article`, `ArticleListResponse` |
| TS 변수·함수 | `camelCase` | `articleList`, `handleSubmit` |
| TS 상수 | `UPPER_SNAKE_CASE` | `API_BASE_URL`, `JWT_STORAGE_KEY` |
| Test 파일 (Python) | `test_<대상>.py` | `test_auth_service.py`, `test_articles_routes.py` |
| Test 함수 (Python) | `test_<scenario>_<expected>()` | `test_register_duplicate_email_returns_422()` |
| 환경 변수 | `UPPER_SNAKE_CASE` | `JWT_SECRET`, `DATABASE_URL` |
| Git 브랜치 | `<mode>/<slug>-issue-<N>` (ADR-0044) | `feat/auth-login-issue-12` |
| Git 커밋 | Conventional (`type(scope): subject`) | `feat(auth): add JWT verification` |

## 2. 에러 코드 PREFIX/SUFFIX

본 시스템은 도메인 에러를 클래스로 표현하고, FastAPI exception handler가 HTTP 응답 + 한글 메시지로 매핑한다. 에러 코드 자체는 *로깅용 식별자*로 사용된다 (응답 body에 노출하지 않음).

| 도메인 | PREFIX | 예 |
|---|---|---|
| Auth (인증/시크릿) | `AUTH_` | `AUTH_DUPLICATE_EMAIL`, `AUTH_INVALID_CREDENTIALS`, `AUTH_TOKEN_EXPIRED`, `AUTH_TOKEN_INVALID` |
| Article (게시글) | `ARTICLE_` | `ARTICLE_NOT_FOUND`, `ARTICLE_FORBIDDEN`, `ARTICLE_SLUG_COLLISION` |
| Comment (댓글) | `COMMENT_` | `COMMENT_NOT_FOUND`, `COMMENT_FORBIDDEN`, `COMMENT_EMPTY_BODY` |
| User (사용자) | `USER_` | `USER_NOT_FOUND`, `USER_DUPLICATE_USERNAME` |
| Validation (입력 검증) | `VALIDATION_` | `VALIDATION_REQUIRED`, `VALIDATION_TOO_SHORT`, `VALIDATION_FORMAT` |
| System (시스템) | `SYSTEM_` | `SYSTEM_DB_ERROR`, `SYSTEM_INTERNAL_ERROR` |

매핑 규칙: `{DOMAIN}_{CATEGORY}_{DETAIL}` (devtoolkit.config.yaml과 정합).

## 3. 언어 관용구

### 3.1 Python

- **타입 힌트 필수** — 모든 함수 시그니처에 인자·반환 타입 명시. `from __future__ import annotations` 사용해 forward reference 단순화.
- **f-string 우선** — `%` 포매팅 / `.format()` 지양.
- **dataclass·Pydantic 우선** — 단순 DTO는 Pydantic BaseModel. 도메인 객체는 SQLAlchemy 모델 또는 `@dataclass`.
- **`pathlib.Path` 사용** — `os.path` 지양.
- **예외는 도메인 클래스로** — `raise InvalidCredentialsError()` 형태. raw `raise Exception()` 금지.
- **async / await** — FastAPI 라우트·서비스는 기본적으로 `async def`. SQLAlchemy는 async session(`AsyncSession`).
- **`with` 블록** — 파일·DB 트랜잭션 등 자원은 컨텍스트 매니저로.
- **`is None` / `is not None`** — None 비교는 `==` 금지.
- **Walrus(`:=`)** — 가독성 해치지 않는 한 허용.
- **import 순서** — stdlib → third-party → local. `ruff` 자동 정렬.

### 3.2 TypeScript / React

- **함수 컴포넌트만** — class 컴포넌트 금지.
- **명시적 props 타입** — `type Props = { ... }`. `any` 금지(`unknown` 사용).
- **훅 우선** — 상태 관리는 `useState` + `zustand` (전역). Redux는 미사용.
- **Strict 모드** — `tsconfig.json: "strict": true`.
- **`const` 우선** — `let`은 명시적 재할당 필요한 경우만.
- **불변성** — state·props 직접 변이 금지. `setState(prev => ...)` 패턴.
- **JSX 키** — 리스트 렌더링 시 `key`는 안정적 ID(article.slug, comment.id) 사용. index 금지.
- **이벤트 핸들러 명명** — `handleSubmit`, `handleClick`. 인라인 화살표는 단순할 때만.
- **fetch 래퍼** — 직접 `fetch` 호출 금지. `M-FE-ApiClient` 경유.

### 3.3 SQL / 마이그레이션

- raw SQL 금지 (R-N-05). SQLAlchemy ORM 또는 Alembic auto-generated migration만 허용.
- 인덱스는 명시적 — 모델에 `Index(...)` 선언.
- FK는 `ondelete="CASCADE"` 명시 (R-F-08 hard delete + 댓글 CASCADE).

## 4. 주석 정책

- **WHY만 적기** — WHAT은 코드가 말함. 코드를 읽으면 "왜 이렇게 했는지"가 안 보일 때만 주석.
- **docstring** — Public 함수·클래스는 1~2줄 docstring. 인자/반환 타입은 타입 힌트로 표현하므로 docstring에 중복 명시 안 함.
- **TODO / FIXME** — `# TODO: <설명>` 또는 `# FIXME(이슈번호): <설명>`. 미해결로 머지 시 GitHub Issue 링크 필수.
- **section 주석 금지** — `# ===== Section ===== ` 류는 IDE 분할로 대체. 단, FastAPI 라우터 그룹 시작 등 *구조적 marker*는 1줄 허용.
- **사용자 입력·보안 관련 주석** — 비밀번호 해시·JWT 등에는 *반드시* 보안 메모 1줄 (예: `# bcrypt rounds=12, R-N-03`).

## 5. Lint·포맷

| 도구 | 룰셋 | 자동 강제 |
|---|---|---|
| `ruff` (Python lint + import 정렬) | `select = ["E", "F", "I", "W", "B", "UP"]` + `line-length=100` | pre-commit + CI |
| `black` (Python format) | line-length=100, target-version=`py311` | pre-commit + CI |
| `mypy` (Python type check) | `strict_optional = True`, `warn_unused_ignores = True` | CI (선택, 시간 부족 시 P1로 후속) |
| `eslint` (TS lint) | `@typescript-eslint/recommended` + `react-hooks/recommended` | pre-commit + CI |
| `prettier` (TS format) | default rules, line-length=100 | pre-commit + CI |
| `tsc --noEmit` (TS type check) | `tsconfig.strict=true` | CI |
| `pre-commit` (훅 러너) | ruff·black·eslint·prettier 통합 | 로컬 커밋 시 자동 |

**자동 강제 흐름**: 로컬 `git commit` → pre-commit 훅이 ruff·black·eslint·prettier 일괄 실행 → 실패 시 커밋 차단. PR → GitHub Actions 워크플로 재실행 → 실패 시 머지 차단(branch protection).

## 6. Import 정책

### 6.1 Python

```python
# 1) stdlib
from __future__ import annotations
import os
from datetime import datetime, timedelta
from typing import Optional

# 2) third-party
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

# 3) local (절대 import. relative `..` 금지)
from realworld.models.user import User
from realworld.schemas.user import UserCreateSchema
from realworld.utils.security import hash_password
```

- ruff `I` 룰이 위 순서 자동 정렬.
- 와일드카드 import (`from x import *`) 금지.
- `relative` import (`from ..models import X`) 지양 — 절대 경로 사용.

### 6.2 TypeScript

```ts
// 1) external (react, react-router-dom, zustand 등)
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

// 2) internal absolute (vite alias `@/`)
import { ArticleCard } from '@/components/ArticleCard';
import { apiClient } from '@/api/client';

// 3) types
import type { Article } from '@/types/article';
```

- `@/` alias는 `vite.config.ts` + `tsconfig.json paths`에 설정.
- 상대 import는 같은 폴더 안에서만 (`./Component`). 두 단계 이상(`../../`) 금지.
- 사용하지 않는 import는 eslint가 자동 제거.
