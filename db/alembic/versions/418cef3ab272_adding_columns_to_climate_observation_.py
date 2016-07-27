"""Adding columns to climate observation table

Revision ID: 418cef3ab272
Revises: 5de546b9328c
Create Date: 2016-07-25 15:07:14.540489

"""

# revision identifiers, used by Alembic.
revision = '418cef3ab272'
down_revision = '5de546b9328c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('climate_raw_table', sa.Column('knbid_', sa.VARCHAR(200)))
    op.add_column('climate_raw_table', sa.Column('metalink_', sa.VARCHAR(200)))
    op.add_column('climate_raw_table', sa.Column('authors_', sa.VARCHAR(200)))
    op.add_column('climate_raw_table', sa.Column('authors_contact_', sa.VARCHAR(200)))

def downgrade():
    pass
