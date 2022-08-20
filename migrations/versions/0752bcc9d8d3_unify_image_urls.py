"""Unify image_urls

Revision ID: 0752bcc9d8d3
Revises: 88093a8f3714
Create Date: 2022-08-19 13:47:32.308995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0752bcc9d8d3'
down_revision = '88093a8f3714'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shop_owner', sa.Column('confirmed', sa.Boolean(), nullable=False))
    op.drop_column('shop_owner', 'confirm')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shop_owner', sa.Column('confirm', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('shop_owner', 'confirmed')
    # ### end Alembic commands ###
