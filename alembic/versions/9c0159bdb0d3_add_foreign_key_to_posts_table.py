"""add foreign key to posts table

Revision ID: 9c0159bdb0d3
Revises: eeb7fd746065
Create Date: 2022-01-08 20:41:35.957967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c0159bdb0d3'
down_revision = 'eeb7fd746065'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_users_fk", "posts", "users",
                          ["owner_id"], ["id"], ondelete="CASCADE")


def downgrade():
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
