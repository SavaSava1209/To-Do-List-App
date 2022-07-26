"""empty message

Revision ID: 50954173f2f5
Revises: fad77ea47c49
Create Date: 2022-07-20 14:27:46.483255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50954173f2f5'
down_revision = 'fad77ea47c49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todolists', sa.Column('name', sa.String(), nullable=False))
    op.alter_column('todos', 'completed',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'completed',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_column('todolists', 'name')
    # ### end Alembic commands ###
