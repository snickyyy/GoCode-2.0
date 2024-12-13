"""add solutions table

Revision ID: 0104047a1406
Revises: 204d4e743bdf
Create Date: 2024-12-14 01:22:37.038223

"""

from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer

from api.problems.models import TASK_STATUS_CHOICES

# revision identifiers, used by Alembic.
revision: str = "0104047a1406"
down_revision: Union[str, None] = "204d4e743bdf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "solutions",
        sa.Column("user", sa.Integer(), nullable=False),
        sa.Column("solution", sa.String(length=1445), nullable=False),
        sa.Column("task", sa.Integer(), nullable=False),
        sa.Column("language", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sqlalchemy_utils.types.choice.ChoiceType(
                TASK_STATUS_CHOICES, impl=Integer()
            ),
            nullable=False,
        ),
        sa.Column("time", sa.Integer(), nullable=False),
        sa.Column("memory", sa.Integer(), nullable=False),
        sa.Column("test_passed", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["language"], ["languages.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["task"], ["tasks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("solutions")
    # ### end Alembic commands ###
