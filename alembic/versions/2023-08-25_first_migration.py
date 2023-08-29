"""first migration

Revision ID: ad6a27b9d264
Revises: fa80d5bcb204
Create Date: 2023-08-25 12:09:38.530719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad6a27b9d264'
down_revision: Union[str, None] = 'fa80d5bcb204'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
