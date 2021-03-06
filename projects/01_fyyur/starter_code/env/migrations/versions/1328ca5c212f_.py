"""empty message

Revision ID: 1328ca5c212f
Revises: e290c62d17c5
Create Date: 2020-06-15 21:42:09.478491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1328ca5c212f'
down_revision = 'e290c62d17c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_description', sa.String(length=250), nullable=True))
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'seeking_venue')
    op.drop_column('artist', 'seeking_description')
    # ### end Alembic commands ###
