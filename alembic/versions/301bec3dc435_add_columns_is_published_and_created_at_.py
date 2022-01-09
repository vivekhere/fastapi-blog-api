"""add columns is_published and created_at to posts table

Revision ID: 301bec3dc435
Revises: 9c0159bdb0d3
Create Date: 2022-01-08 21:04:47.638415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '301bec3dc435'
down_revision = '9c0159bdb0d3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column(
        "is_published", sa.Boolean, nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text("NOW()")))


def downgrade():
    op.drop_column("posts", "is_published")
    op.drop_column("posts", "created_at")
