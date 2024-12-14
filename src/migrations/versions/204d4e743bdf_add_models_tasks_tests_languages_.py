"""add models: tasks, tests, languages, categories

Revision ID: 204d4e743bdf
Revises: 1783a106c067
Create Date: 2024-12-14 00:58:41.393621

"""
from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer

from api.problems.models import DIFFICULTLY_CHOICES

# revision identifiers, used by Alembic.
revision: str = '204d4e743bdf'
down_revision: Union[str, None] = '1783a106c067'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('languages',
    sa.Column('name', sa.String(length=28), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tests',
    sa.Column('path', sa.String(length=280), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('difficulty', sqlalchemy_utils.types.choice.ChoiceType(DIFFICULTLY_CHOICES, impl=Integer()), nullable=False),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.Column('tests', sa.Integer(), nullable=False),
    sa.Column('constraints', sa.String(length=100), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['category'], ['categories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tests'], ['tests.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    op.drop_table('tests')
    op.drop_table('languages')
    op.drop_table('categories')
    # ### end Alembic commands ###
