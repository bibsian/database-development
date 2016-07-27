"""Change primary key name for climate observation table and add a metarecordid column.

Revision ID: 2dd7086110f9
Revises: 418cef3ab272
Create Date: 2016-07-25 15:22:27.069169

"""

# revision identifiers, used by Alembic.
revision = '2dd7086110f9'
down_revision = '418cef3ab272'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE climate_raw_table RENAME metarecordid to climate_pk')
    op.add_column('climate_raw_table', sa.Column('metarecordid_', sa.VARCHAR(200)))



def downgrade():
    pass
