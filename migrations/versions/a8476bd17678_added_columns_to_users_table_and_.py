"""Added columns to users table and rearranged checklists/items

Revision ID: a8476bd17678
Revises: 16cfdf63621e
Create Date: 2020-11-21 22:20:32.504816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8476bd17678'
down_revision = '16cfdf63621e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('users', sa.Column('has_reminders', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('profile_image', sa.String(), nullable=True))
    op.add_column('users', sa.Column('reminder_time', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('timezone', sa.Integer(), nullable=False))
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'username')
    op.drop_column('users', 'timezone')
    op.drop_column('users', 'reminder_time')
    op.drop_column('users', 'profile_image')
    op.drop_column('users', 'name')
    op.drop_column('users', 'has_reminders')
    op.alter_column('items', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###