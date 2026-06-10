"""add_password_hash_to_users

Revision ID: a9223fb45abf
Revises: 1ee8c9985699
Create Date: 2026-06-10 17:48:12.921463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9223fb45abf'
down_revision: Union[str, None] = '1ee8c9985699'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# bcrypt hash for "UNSET_PASSWORD" — existing rows cannot log in until reset
_PLACEHOLDER_HASH = (
    "$2b$12$FX6JKAR2U8WJLIexdSu66.q0KIpXb1IOa65QgPYh.3x.AGT22L6C."
)


def upgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('password_hash', sa.String(length=255), nullable=True)
        )

    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE users SET password_hash = :hash WHERE password_hash IS NULL"),
        {"hash": _PLACEHOLDER_HASH},
    )

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash', nullable=False)


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password_hash')
