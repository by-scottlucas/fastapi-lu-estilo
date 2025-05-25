"""create orders and order_items tables

Revision ID: 4fb1fca5c297
Revises: 9a34460daaf5
Create Date: 2025-05-25 11:38:55.654272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fb1fca5c297'
down_revision: Union[str, None] = '9a34460daaf5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
