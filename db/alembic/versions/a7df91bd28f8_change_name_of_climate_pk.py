"""Change name of climate_pk

Revision ID: a7df91bd28f8
Revises: c7387e552098
Create Date: 2016-07-25 17:31:17.461034

"""

# revision identifiers, used by Alembic.
revision = 'a7df91bd28f8'
down_revision = 'c7387e552098'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE climate_raw_table RENAME climate_pk to metarecordid_')

def downgrade():
    pass
