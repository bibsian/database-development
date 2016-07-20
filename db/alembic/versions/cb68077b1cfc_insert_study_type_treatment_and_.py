"""Insert study type, treatment, and experimental maintenance

Revision ID: cb68077b1cfc
Revises: 
Create Date: 2016-07-18 17:10:59.899657

"""

# revision identifiers, used by Alembic.
revision = 'cb68077b1cfc'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.add_column('main_table', sa.Column('study_type', sa.VARCHAR(200)))
	op.add_column('main_table', sa.Column('treatment_type', sa.VARCHAR(200)))
	op.add_column('main_table', sa.Column('num_treatments', sa.VARCHAR(200)))
	op.add_column('main_table', sa.Column('exp_maintainence', sa.VARCHAR(200)))


def downgrade():
    pass
