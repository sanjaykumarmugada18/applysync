"""Gmail connection and session-bound OAuth state; no existing row updates."""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("gmail_connections",
        sa.Column("owner_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("google_subject", sa.String(255)), sa.Column("email", sa.String(254)),
        sa.Column("encrypted_refresh_token", sa.Text()), sa.Column("granted_scopes", sa.Text()),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("revocation_warning", sa.Boolean(), nullable=False),
        sa.Column("connected_at", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("status IN ('connected','disconnected','reauthorization_needed')", name="ck_gmail_status"))
    op.create_table("gmail_oauth_states",
        sa.Column("state_hash", sa.String(64), primary_key=True),
        sa.Column("owner_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("session_id", sa.Uuid(), sa.ForeignKey("auth_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("encrypted_flow", sa.Text()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True)))


def downgrade():
    raise RuntimeError("Gmail downgrade requires an explicit authorization-data preservation plan.")
