"""create task assignments table

Revision ID: 1ee8c9985699
Revises: c4e8f1a92b3d
Create Date: 2026-06-10 14:10:23.600002

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1ee8c9985699"
down_revision: Union[str, None] = "c4e8f1a92b3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "task_assignments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_eligible", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "task_id",
            "user_id",
            name="uq_task_assignments_task_id_user_id",
        ),
    )

    with op.batch_alter_table("task_assignments", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_task_assignments_is_eligible"),
            ["is_eligible"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_task_assignments_task_id"),
            ["task_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_task_assignments_user_id"),
            ["user_id"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("task_assignments", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_task_assignments_user_id"))
        batch_op.drop_index(batch_op.f("ix_task_assignments_task_id"))
        batch_op.drop_index(batch_op.f("ix_task_assignments_is_eligible"))

    op.drop_table("task_assignments")