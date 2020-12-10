"""added a column for salt

Revision ID: 221284726ee4
Revises: 386f4f666051
Create Date: 2020-12-10 23:42:24.519294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '221284726ee4'
down_revision = '386f4f666051'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('link', sa.Column('link_salt', sa.String(length=8), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('link', 'link_salt')
    # ### end Alembic commands ###
