"""add content column to posts table

Revision ID: 397a44a7fe54
Revises: b8d8a9eaba83
Create Date: 2023-05-14 21:44:39.407995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '397a44a7fe54'
down_revision = 'b8d8a9eaba83'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
