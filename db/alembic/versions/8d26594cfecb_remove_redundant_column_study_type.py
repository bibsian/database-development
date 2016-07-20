"""Remove redundant column 'study_type'

Revision ID: 8d26594cfecb
Revises: fb7bb74fa834
Create Date: 2016-07-18 18:32:48.796024

"""

# revision identifiers, used by Alembic.
revision = '8d26594cfecb'
down_revision = 'fb7bb74fa834'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    pass


def downgrade():
	op.drop_column('main_table', 'study_type')

