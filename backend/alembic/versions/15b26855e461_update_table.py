"""update table

Revision ID: 15b26855e461
Revises: ede2cc2576ce
Create Date: 2025-07-19 14:14:48.825130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '15b26855e461'
down_revision: Union[str, Sequence[str], None] = 'ede2cc2576ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.drop_column('movies', 'createdAt')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('createdAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('movies', 'created_at')
    # ### end Alembic commands ###
