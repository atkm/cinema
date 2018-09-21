"""empty message

Revision ID: 9f5184eb7e18
Revises: 1162f603e5c8
Create Date: 2018-09-20 19:12:54.394892

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9f5184eb7e18'
down_revision = '1162f603e5c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('showtime', sa.Column('showdate', sa.Date(), nullable=True))
    op.drop_column('showtime', 'showtime')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('showtime', sa.Column('showtime', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_column('showtime', 'showdate')
    # ### end Alembic commands ###
