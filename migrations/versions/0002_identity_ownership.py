"""Revocable identities and quarantined legacy ownership.

No legacy records are changed or assigned. NULL owners are inaccessible via API.
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("password_hash", sa.String(512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.CheckConstraint("email = lower(email)", name="ck_users_email_lower"))
    op.create_table("auth_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_auth_sessions"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_auth_sessions_user"))
    op.create_index("ix_auth_sessions_user_id", "auth_sessions", ["user_id"])
    op.add_column("job_applications", sa.Column("owner_id", sa.Uuid(), nullable=True))
    op.create_foreign_key("fk_job_applications_owner", "job_applications", "users", ["owner_id"], ["id"])
    op.create_index("ix_job_applications_owner_order", "job_applications", ["owner_id", "created_at", "id"])


def downgrade():
    # Downgrading would remove identity/ownership. Require an explicit manual plan.
    raise RuntimeError("Identity downgrade is intentionally disabled; preserve user data.")
