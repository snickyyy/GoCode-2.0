"""add model users

Revision ID: 1783a106c067
Revises: 
Create Date: 2024-12-13 20:33:55.902136

"""

from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer

from api.users.models import ROLES

# revision identifiers, used by Alembic.
revision: str = "1783a106c067"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=25), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("email", sa.String(length=180), nullable=False),
        sa.Column("description", sa.String(length=120), nullable=True),
        sa.Column(
            "role",
            sqlalchemy_utils.types.choice.ChoiceType(ROLES, impl=Integer()),
            nullable=False,
        ),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
