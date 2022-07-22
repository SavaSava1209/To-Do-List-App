"""empty message

Revision ID: fad77ea47c49
Revises: 
Create Date: 2022-07-20 13:57:08.972357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fad77ea47c49'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('todos', sa.Column('list_id', sa.Integer(), nullable=False))
    op.alter_column('todos', 'completed',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.create_foreign_key(None, 'todos', 'todolists', ['list_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.alter_column('todos', 'completed',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.drop_column('todos', 'list_id')
    op.drop_table('todolists')
    # ### end Alembic commands ###