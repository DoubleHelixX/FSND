"""empty message

Revision ID: c9cc5d444047
Revises: fdd8c4a38afd
Create Date: 2020-06-15 23:22:17.724742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9cc5d444047'
down_revision = 'fdd8c4a38afd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'facebook_link')
    op.drop_column('artist', 'deleted')
    op.drop_column('artist', 'website_link')
    op.drop_column('artist', 'seeking_venue')
    op.drop_column('artist', 'seeking_description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_description', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('website_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('deleted', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
