"""add reviews table

Revision ID: 6a820a636ddb
Revises: 12bb7e97faf9
Create Date: 2026-01-31 14:23:35.409466
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6a820a636ddb"
down_revision: Union[str, Sequence[str], None] = "12bb7e97faf9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),

        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),

        sa.CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="review_rating_check",
        ),
        sa.UniqueConstraint(
            "user_id",
            "product_id",
            name="uq_user_product_review",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("reviews")
