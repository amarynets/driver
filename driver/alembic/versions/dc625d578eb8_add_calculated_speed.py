"""Add calculated speed

Revision ID: dc625d578eb8
Revises: a3effb6c4b1c
Create Date: 2021-08-19 01:52:20.406251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc625d578eb8'
down_revision = 'a3effb6c4b1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('positions', sa.Column('calculated_speed', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('positions', 'calculated_speed')
    # ### end Alembic commands ###