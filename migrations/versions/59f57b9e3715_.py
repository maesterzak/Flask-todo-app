"""empty message

Revision ID: 59f57b9e3715
Revises: 
Create Date: 2023-12-22 06:59:12.043330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59f57b9e3715'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category'], ['Category.id'], ),
    sa.ForeignKeyConstraint(['category'], ['Category.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Todo')
    op.drop_table('Category')
    # ### end Alembic commands ###
