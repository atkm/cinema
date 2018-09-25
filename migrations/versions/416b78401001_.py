"""empty message

Revision ID: 416b78401001
Revises: 
Create Date: 2018-09-24 20:58:51.804985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '416b78401001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Commands copied and pasted from the former head (4b0680ad571a)
    op.create_table('film',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.PrimaryKeyConstraint('id')
            )
    op.create_table('theater',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=False),
            sa.PrimaryKeyConstraint('id')
            )
    op.create_table('showtime',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('showdate', sa.Date(), nullable=True),
            sa.Column('theater_id', sa.Integer(), nullable=True),
            sa.Column('film_id', sa.Integer(), nullable=True),
            sa.Column('count', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['film_id'], ['film.id'], ),
            sa.ForeignKeyConstraint(['theater_id'], ['theater.id'], ),
            sa.PrimaryKeyConstraint('id')
            )

def downgrade():
    pass
