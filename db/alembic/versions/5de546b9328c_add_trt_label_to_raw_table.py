"""add trt_label to raw_table

Revision ID: 5de546b9328c
Revises: 8d26594cfecb
Create Date: 2016-07-19 13:39:46.689318

"""

# revision identifiers, used by Alembic.
revision = '5de546b9328c'
down_revision = '8d26594cfecb'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('raw_table', sa.Column('trt_label', sa.VARCHAR(200)))



def downgrade():
    pass
