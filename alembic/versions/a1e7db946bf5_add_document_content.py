"""add document content

Revision ID: a1e7db946bf5
Revises: 550517e71a2e
Create Date: 2026-08-12 23:50:55.296621
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "a1e7db946bf5"
down_revision: Union[str, Sequence[str], None] = "550517e71a2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "documents",
        sa.Column(
            "content",
            sa.Text(),
            nullable=True,
        ),
    )

    op.execute(
        sa.text(
            "UPDATE documents "
            "SET content = '' "
            "WHERE content IS NULL"
        )
    )

    op.alter_column(
        "documents",
        "content",
        existing_type=sa.Text(),
        nullable=False,
    )

    op.alter_column(
        "documents",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "documents",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )

    op.drop_column(
        "documents",
        "content",
    )
