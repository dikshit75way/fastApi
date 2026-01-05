"""add status on purchase and create review table

Revision ID: 9aeec0bc79b6
Revises: a79a6a4fcf70
Create Date: 2026-01-05 18:15:12.465653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9aeec0bc79b6'
down_revision: Union[str, Sequence[str], None] = 'a79a6a4fcf70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add column as nullable initially
    op.add_column('purchases', sa.Column('status', sa.String(length=255), nullable=True))
    
    # 2. Update existing rows to "pending" or "purchased"
    op.execute("UPDATE purchases SET status = 'purchased'")
    
    # 3. Set NOT NULL constraint
    op.alter_column('purchases', 'status', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('purchases', 'status')
