"""Initial migration

Revision ID: 3bf919352dd6
Revises: 418ad9717056
Create Date: 2024-05-20 18:12:32.897781

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3bf919352dd6"
down_revision: Union[str, None] = "418ad9717056"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("telegram_user_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(
        op.f("ix_users_telegram_user_id"),
        "users",
        ["telegram_user_id"],
        unique=True,
    )
    op.create_table(
        "videos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("views", sa.Integer(), nullable=False),
        sa.Column("video_url", sa.String(), nullable=False),
        sa.Column("channel_name", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_videos_id"), "videos", ["id"], unique=False)
    op.create_index(op.f("ix_videos_title"), "videos", ["title"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_videos_title"), table_name="videos")
    op.drop_index(op.f("ix_videos_id"), table_name="videos")
    op.drop_table("videos")
    op.drop_index(op.f("ix_users_telegram_user_id"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
