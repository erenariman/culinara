"""remove_shopping_and_organization_tables

Revision ID: 69fbe612723d
Revises: 239addcfca86
Create Date: 2026-04-02 16:22:12.056119

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69fbe612723d'
down_revision: Union[str, Sequence[str], None] = '239addcfca86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop in reverse dependency order with if_exists=True
    op.execute("DROP TABLE IF EXISTS shopping_list_items CASCADE")
    op.execute("DROP TABLE IF EXISTS shopping_lists CASCADE")
    op.execute("DROP TABLE IF EXISTS organizations CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    # Organization (Simplistic)
    op.create_table('organizations',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False)
    )
    # Shopping List
    op.create_table('shopping_lists',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True)
    )
    # Shopping Item
    op.create_table('shopping_list_items',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('shopping_list_id', sa.String(), sa.ForeignKey('shopping_lists.id'), nullable=False),
        sa.Column('ingredient_id', sa.String(), sa.ForeignKey('ingredients.id'), nullable=True),
        sa.Column('custom_text', sa.String(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(), nullable=True),
        sa.Column('is_checked', sa.Boolean(), server_default='false')
    )
