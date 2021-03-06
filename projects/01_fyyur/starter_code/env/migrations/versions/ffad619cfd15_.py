"""empty message

Revision ID: ffad619cfd15
Revises: c9cc5d444047
Create Date: 2020-06-15 23:22:38.063607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffad619cfd15'
down_revision = 'c9cc5d444047'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('artist', sa.Column('facebook_link', sa.String(length=120), nullable=True))
    op.add_column('artist', sa.Column('seeking_description', sa.String(length=250), nullable=True))
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'website_link')
    op.drop_column('artist', 'seeking_venue')
    op.drop_column('artist', 'seeking_description')
    op.drop_column('artist', 'facebook_link')
    op.drop_column('artist', 'deleted')
    # ### end Alembic commands ###
