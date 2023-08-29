"""first migration1

Revision ID: 95f48d732c86
Revises: ad6a27b9d264
Create Date: 2023-08-25 12:15:43.435983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95f48d732c86'
down_revision: Union[str, None] = 'ad6a27b9d264'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
