"""Admin review add subsection

Revision ID: eb047c8525ba
Revises: 00667812e389
Create Date: 2024-03-26 20:27:31.606208

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "eb047c8525ba"
down_revision: Union[str, None] = "00667812e389"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "admin_review",
        sa.Column("sub_section_heading", sa.String()),
        schema="ssle_metro",
    )


def downgrade() -> None:
    op.drop_column("admin_review", "sub_section_heading", schema="ssle_metro")
