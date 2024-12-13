"""add tables: posts, comments and sessions

Revision ID: 00be102190a8
Revises: 0104047a1406
Create Date: 2024-12-14 02:20:27.072194

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "00be102190a8"
down_revision: Union[str, None] = "0104047a1406"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("data", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "posts",
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("user", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(length=600), nullable=False),
        sa.Column("image", sa.String(length=250), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "comments",
        sa.Column("user", sa.Integer(), nullable=False),
        sa.Column("post", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(length=440), nullable=False),
        sa.Column("image", sa.String(length=250), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["post"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("comments")
    op.drop_table("posts")
    op.drop_table("sessions")
    # ### end Alembic commands ###
