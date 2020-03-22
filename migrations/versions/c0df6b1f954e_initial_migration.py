"""Initial migration

Revision ID: c0df6b1f954e
Revises: 
Create Date: 2020-03-22 11:37:56.602652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0df6b1f954e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('short_url',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('long_url', sa.String(), nullable=False),
    sa.Column('short_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('short_url')
    # ### end Alembic commands ###