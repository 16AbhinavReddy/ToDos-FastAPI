"""empty message

Revision ID: d9bca284f23d
Revises: b1f240cfcdca
Create Date: 2023-05-08 15:31:26.005919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9bca284f23d'
down_revision = 'b1f240cfcdca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column("phone_no", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_no')
