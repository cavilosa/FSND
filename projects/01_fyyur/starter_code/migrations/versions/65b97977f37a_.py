"""empty message

Revision ID: 65b97977f37a
Revises: c011a46d2cb3
Create Date: 2021-04-06 14:32:37.246578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65b97977f37a'
down_revision = 'c011a46d2cb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('address', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'address')
    # ### end Alembic commands ###
