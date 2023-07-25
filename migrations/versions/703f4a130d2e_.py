"""empty message

Revision ID: 703f4a130d2e
Revises: 
Create Date: 2023-07-25 00:53:27.001314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '703f4a130d2e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('business_name', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('nif', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=150), nullable=False),
    sa.Column('payment_method', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_name'),
    sa.UniqueConstraint('email')
    )
    op.create_table('trip',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country', sa.String(length=40), nullable=False),
    sa.Column('city', sa.String(length=40), nullable=False),
    sa.Column('activities', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('firstname', sa.String(length=100), nullable=False),
    sa.Column('lastname', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=200), nullable=False),
    sa.Column('dni', sa.Integer(), nullable=False),
    sa.Column('payment_method', sa.String(length=100), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('offers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('business_id', sa.Integer(), nullable=False),
    sa.Column('normal_user_price', sa.Integer(), nullable=False),
    sa.Column('medium_user_price', sa.Integer(), nullable=False),
    sa.Column('high_user_price', sa.Integer(), nullable=False),
    sa.Column('premium_user_price', sa.Integer(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['business_id'], ['business_user.id'], ),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('offers')
    op.drop_table('user')
    op.drop_table('trip')
    op.drop_table('business_user')
    # ### end Alembic commands ###
