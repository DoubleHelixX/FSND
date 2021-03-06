"""empty message

Revision ID: d8b5b8ebb810
Revises: 0705f032f64b
Create Date: 2020-06-18 16:25:50.627459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8b5b8ebb810'
down_revision = '0705f032f64b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'website_link')
    # ### end Alembic commands ###
