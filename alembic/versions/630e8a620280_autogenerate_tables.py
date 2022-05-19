"""Autogenerate tables

Revision ID: 630e8a620280
Revises: 
Create Date: 2022-05-18 20:35:26.747254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '630e8a620280'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts')
    op.create_table(
        'users', sa.Column('id', sa.Integer(),
                           nullable=False, primary_key=True)
    )
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  server_default='TRUE', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', 'posts', 'users', [
                          'owner_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_users_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    op.drop_table('posts')
    op.drop_column('users', 'id', ondelete="CASCADE")
    # ### end Alembic commands ###