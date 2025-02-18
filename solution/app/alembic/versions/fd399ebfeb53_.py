"""empty message

Revision ID: fd399ebfeb53
Revises: cd3bbd014380
Create Date: 2025-02-18 16:37:14.485409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fd399ebfeb53'
down_revision: Union[str, None] = 'cd3bbd014380'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('campaigns', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('campaigns', 'image_url')
    # ### end Alembic commands ###
