"""add sender_id to rules

Revision ID: 1d5bf493d2c7
Revises: 
Create Date: 2025-09-12 17:52:49.842988
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1d5bf493d2c7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     """Upgrade schema."""
#     # Add new column as nullable first (SQLite-safe)
#     op.add_column('rules', sa.Column('sender_id', sa.Integer(), nullable=True))
#
#     # Drop old index on `sender`
#     op.drop_index(op.f('ix_rules_sender'), table_name='rules')
#
#     # Add foreign key constraint
#     op.create_foreign_key(
#         constraint_name="fk_rules_sender_id",
#         source_table="rules",
#         referent_table="senders",
#         local_cols=["sender_id"],
#         remote_cols=["id"],
#     )
#
#     # Drop old `sender` column
#     op.drop_column('rules', 'sender')
def upgrade() -> None:
    # Do NOT add column again
    # op.add_column('rules', sa.Column('sender_id', sa.Integer(), nullable=True))

    op.drop_index(op.f('ix_rules_sender'), table_name='rules')

    op.create_foreign_key(
        "fk_rules_sender_id", "rules", "senders",
        ["sender_id"], ["id"]
    )

    op.drop_column('rules', 'sender')


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate old `sender` column
    op.add_column('rules', sa.Column('sender', sa.VARCHAR(), nullable=True))

    # Drop the FK constraint
    op.drop_constraint("fk_rules_sender_id", "rules", type_="foreignkey")

    # Recreate old index
    op.create_index(op.f('ix_rules_sender'), 'rules', ['sender'], unique=False)

    # Drop new column
    op.drop_column('rules', 'sender_id')
