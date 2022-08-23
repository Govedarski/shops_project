"""Alter field in ShopModel

Revision ID: 6fd2edd0b97e
Revises: 326753047981
Create Date: 2022-08-22 20:47:07.618831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fd2edd0b97e'
down_revision = '326753047981'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('shop', 'bulstat',
               existing_type=sa.VARCHAR(length=9),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('shop', 'bulstat',
               existing_type=sa.VARCHAR(length=9),
               nullable=True)
    # ### end Alembic commands ###
