"""initial schema

Revision ID: 0001
Revises:
"""
import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("video_path", sa.String(500), nullable=False),
        sa.Column("duration", sa.Float, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "segments",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("idx", sa.Integer, nullable=False),
        sa.Column("start", sa.Float, nullable=False),
        sa.Column("end", sa.Float, nullable=False),
        sa.Column("text", sa.Text, nullable=False),
        sa.Column("deleted", sa.Boolean, nullable=False, server_default=sa.false()),
    )
    op.create_index("ix_segments_project_id", "segments", ["project_id"])
    op.create_table(
        "exports",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="none"),
        sa.Column("output_path", sa.String(500)),
        sa.Column("duration", sa.Float),
        sa.Column("error", sa.String(500)),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_exports_project_id", "exports", ["project_id"])


def downgrade() -> None:
    op.drop_table("exports")
    op.drop_table("segments")
    op.drop_table("projects")
