"""Create the initial manual application table.

Explicitly authored migration: inspect before applying; no autogenerate database
connection or metadata.create_all is required to produce this revision.
"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "job_applications",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("company", sa.String(200), nullable=False),
        sa.Column("role", sa.String(200), nullable=False),
        sa.Column("applied_on", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("company ~ '[^[:space:]]'", name="ck_job_applications_company_nonblank"),
        sa.CheckConstraint("role ~ '[^[:space:]]'", name="ck_job_applications_role_nonblank"),
        sa.PrimaryKeyConstraint("id", name="pk_job_applications"),
    )


def downgrade():
    op.drop_table("job_applications")
