"""add Bai5

Revision ID: f6e645971014
Revises: af6d4bec815a
Create Date: 2024-11-06 16:18:12.903023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6e645971014'
down_revision: Union[str, None] = 'af6d4bec815a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bai5',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ws', sa.Integer(), nullable=False),
    sa.Column('tim', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bai5')
    # ### end Alembic commands ###
