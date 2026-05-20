"""initial

Revision ID: 0001
Revises:
Create Date: 2026-05-20

본 revision은 Issue #1 부팅 골격용 빈 init.
실 스키마(User/Article/Comment/Tag)는 후속 이슈(#2 User, #6 Comment 등)에서
down_revision="0001"로 연결한다.
"""

from collections.abc import Sequence

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
