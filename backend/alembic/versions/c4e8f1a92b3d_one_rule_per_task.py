"""enforce one eligibility rule per task

Revision ID: c4e8f1a92b3d
Revises: a51ac3589f9a
Create Date: 2026-06-01 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c4e8f1a92b3d"
down_revision: Union[str, None] = "a51ac3589f9a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Keep the latest rule per task before enforcing uniqueness.
    op.execute(
        """
        DELETE FROM task_rules
        WHERE id NOT IN (
            SELECT MAX(id) FROM task_rules GROUP BY task_id
        )
        """
    )

    with op.batch_alter_table("task_rules", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("uq_task_rules_task_id"),
            ["task_id"],
            unique=True,
        )


def downgrade() -> None:
    with op.batch_alter_table("task_rules", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("uq_task_rules_task_id"))
