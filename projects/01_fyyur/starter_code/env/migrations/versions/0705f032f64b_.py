"""empty message

Revision ID: 0705f032f64b
Revises: fee051190d3c
Create Date: 2020-06-18 13:35:22.730311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0705f032f64b'
down_revision = 'fee051190d3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'deleted')
    # ### end Alembic commands ###