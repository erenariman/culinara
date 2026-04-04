"""add_deleted_at_to_ingredients

Revision ID: c4e287bb6d03
Revises: 239addcfca86
Create Date: 2026-04-02 18:56:57.705766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4e287bb6d03'
down_revision: Union[str, Sequence[str], None] = '69fbe612723d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('ingredients', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ingredients', 'deleted_at')
