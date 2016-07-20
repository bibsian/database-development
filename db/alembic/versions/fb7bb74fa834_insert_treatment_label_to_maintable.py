"""insert treatment label to maintable

Revision ID: fb7bb74fa834
Revises: cb68077b1cfc
Create Date: 2016-07-18 17:37:12.718542

"""

# revision identifiers, used by Alembic.
revision = 'fb7bb74fa834'
down_revision = 'cb68077b1cfc'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('main_table', sa.Column('trt_label', sa.VARCHAR(200)))


def downgrade():
    pass
