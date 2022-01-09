"""add users table

Revision ID: eeb7fd746065
Revises: da7c4d9fbf07
Create Date: 2022-01-08 20:30:28.941865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeb7fd746065'
down_revision = 'da7c4d9fbf07'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer, nullable=False),
                    sa.Column("email", sa.String, nullable=False),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"))


def downgrade():
    op.drop_table("users")
