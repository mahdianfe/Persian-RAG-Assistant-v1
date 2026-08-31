"""add chunk embeddings

Revision ID: 7556ccacc40f
Revises: 193d8fa39665
Create Date: 2026-08-14 17:52:59.143134

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector


revision: str = "7556ccacc40f"
down_revision: Union[str, Sequence[str], None] = "193d8fa39665"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "document_chunks",
        sa.Column(
            "embedding",
            Vector(1024),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "document_chunks",
        "embedding",
    )
