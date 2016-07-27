"""drop metareacodid_

Revision ID: c7387e552098
Revises: 2dd7086110f9
Create Date: 2016-07-25 17:11:44.868027

"""

# revision identifiers, used by Alembic.
revision = 'c7387e552098'
down_revision = '2dd7086110f9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    pass


def downgrade():
	op.execute('ALTER TABLE climate_raw_table DROP COLUMN metarecordid_')
