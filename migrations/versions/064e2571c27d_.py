"""empty message

Revision ID: 064e2571c27d
Revises: 
Create Date: 2021-12-22 09:50:33.950536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '064e2571c27d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('content')
    # ### end Alembic commands ###