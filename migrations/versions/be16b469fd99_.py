"""empty message

<<<<<<<< HEAD:migrations/versions/39f8ac4a3608_.py
Revision ID: 39f8ac4a3608
Revises: 
Create Date: 2024-05-30 22:51:21.510517
========
Revision ID: be16b469fd99
Revises: 
Create Date: 2024-05-31 05:07:46.384842
>>>>>>>> b0c3c33f3e903c81d92f04d964316925b6684a29:migrations/versions/be16b469fd99_.py

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
<<<<<<<< HEAD:migrations/versions/39f8ac4a3608_.py
revision = '39f8ac4a3608'
========
revision = 'be16b469fd99'
>>>>>>>> b0c3c33f3e903c81d92f04d964316925b6684a29:migrations/versions/be16b469fd99_.py
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=1024), nullable=False),
    sa.Column('is_user', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('last_name', sa.String(length=250), nullable=False),
    sa.Column('username', sa.String(length=250), nullable=False),
    sa.Column('number_document', sa.String(length=250), nullable=False),
    sa.Column('phone', sa.String(length=250), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('number_document'),
    sa.UniqueConstraint('username')
    )
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=1024), nullable=False),
    sa.Column('is_teacher', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('last_name', sa.String(length=250), nullable=False),
    sa.Column('username', sa.String(length=250), nullable=False),
    sa.Column('number_document', sa.String(length=250), nullable=False),
    sa.Column('phone', sa.String(length=250), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=250), nullable=False),
    sa.Column('certificate_teacher', sa.String(length=250), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('number_document'),
    sa.UniqueConstraint('username')
    )
    op.create_table('manager',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=1024), nullable=False),
    sa.Column('is_manager', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('last_name', sa.String(length=250), nullable=False),
    sa.Column('phone', sa.String(length=250), nullable=False),
    sa.Column('number_document', sa.String(length=250), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('number_document')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title_category', sa.String(length=250), nullable=False),
    sa.Column('sub_category', sa.String(length=250), nullable=False),
    sa.Column('category_length', sa.String(length=300), nullable=False),
    sa.Column('create_date', sa.String(length=300), nullable=True),
    sa.Column('course_more_current', sa.String(length=250), nullable=False),
    sa.Column('course_more_sold', sa.String(length=250), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manager_id'], ['manager.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('category_title', sa.String(length=250), nullable=False),
    sa.Column('modules_length', sa.Integer(), nullable=False),
    sa.Column('title_certificate_to_get', sa.String(length=250), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('assessment', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.String(length=300), nullable=True),
    sa.Column('title_Teacher', sa.String(length=250), nullable=False),
    sa.Column('date_expiration', sa.String(length=300), nullable=True),
    sa.Column('title_url_media', sa.String(length=1024), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manager_id'], ['manager.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('modules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description_content', sa.String(length=500), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('url_video', sa.String(length=1024), nullable=False),
    sa.Column('video_id', sa.String(length=250), nullable=True),
    sa.Column('image_id', sa.String(length=250), nullable=True),
    sa.Column('total_video', sa.String(length=250), nullable=True),
    sa.Column('date_create', sa.String(length=250), nullable=False),
    sa.Column('token_module', sa.String(length=1024), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
<<<<<<<< HEAD:migrations/versions/39f8ac4a3608_.py
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=250), nullable=False),
    sa.Column('title_course', sa.String(length=250), nullable=False),
    sa.Column('pad_amount', sa.String(length=250), nullable=False),
    sa.Column('type_payment', sa.String(length=250), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('manager_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['manager_id'], ['manager.id'], ),
========
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title_order', sa.String(length=250), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=250), nullable=False),
    sa.Column('total', sa.String(length=250), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('course_name', sa.String(length=300), nullable=True),
    sa.Column('teacher_name', sa.String(length=300), nullable=True),
    sa.Column('teacher_last_name', sa.String(length=300), nullable=True),
    sa.Column('user_name', sa.String(length=300), nullable=True),
    sa.Column('user_last_name', sa.String(length=300), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
>>>>>>>> b0c3c33f3e903c81d92f04d964316925b6684a29:migrations/versions/be16b469fd99_.py
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trolley',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title_course', sa.String(length=250), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=250), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quizzes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_title', sa.String(length=250), nullable=False),
    sa.Column('answer_teacher', sa.String(length=800), nullable=False),
    sa.Column('answer_user', sa.Boolean(), nullable=False),
    sa.Column('approved', sa.Boolean(), nullable=False),
    sa.Column('approval_percentage_user', sa.String(length=800), nullable=False),
    sa.Column('approval_percentage_number', sa.String(length=800), nullable=False),
    sa.Column('approval_percentage', sa.Boolean(), nullable=False),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quizzes')
    op.drop_table('trolley')
<<<<<<<< HEAD:migrations/versions/39f8ac4a3608_.py
========
    op.drop_table('orders')
    op.drop_table('modules')
>>>>>>>> b0c3c33f3e903c81d92f04d964316925b6684a29:migrations/versions/be16b469fd99_.py
    op.drop_table('payment')
    op.drop_table('modules')
    op.drop_table('course')
    op.drop_table('category')
    op.drop_table('manager')
    op.drop_table('teacher')
    op.drop_table('user')
    # ### end Alembic commands ###
