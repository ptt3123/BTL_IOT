"""add ws1

Revision ID: 46d2c5b58bf1
Revises: 88ef41719674
Create Date: 2024-11-06 17:51:32.702057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '46d2c5b58bf1'
down_revision: Union[str, None] = '88ef41719674'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bai5')
    op.add_column('data', sa.Column('ws', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('data', 'ws')
    op.create_table('bai5',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('ws', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('tim', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
