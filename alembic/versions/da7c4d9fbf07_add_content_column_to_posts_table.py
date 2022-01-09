"""add content column to posts table

Revision ID: da7c4d9fbf07
Revises: 8d88efb4c0e9
Create Date: 2022-01-08 20:19:47.670917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da7c4d9fbf07'
down_revision = '8d88efb4c0e9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade():
    op.drop_column("posts", "content")
