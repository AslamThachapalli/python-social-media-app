"""add remaining columns to posts table

Revision ID: 9b6537d3e20c
Revises: 2d48e753b1a8
Create Date: 2023-05-14 22:32:35.063673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b6537d3e20c'
down_revision = '2d48e753b1a8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='True',
                                     nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                  server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
