"""create posts table

Revision ID: 8d88efb4c0e9
Revises: 
Create Date: 2022-01-08 19:58:54.098040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d88efb4c0e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("title", sa.String, nullable=False))


def downgrade():
    op.drop_table("posts")
