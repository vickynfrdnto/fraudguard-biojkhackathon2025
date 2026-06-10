"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-10
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(255), nullable=False), sa.Column("full_name", sa.String(255), nullable=False), sa.Column("hashed_password", sa.String(255), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("is_verified", sa.Boolean(), nullable=False), sa.Column("verification_token", sa.String(255)), sa.Column("reset_token", sa.String(255)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("system_settings", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("key", sa.String(120), nullable=False), sa.Column("value", sa.Text(), nullable=False), sa.Column("description", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_system_settings_key", "system_settings", ["key"], unique=True)
    op.create_table("transactions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL")), sa.Column("reference", sa.String(80), nullable=False), sa.Column("amount", sa.Numeric(14, 2), nullable=False), sa.Column("sender_account", sa.String(80)), sa.Column("recipient_account", sa.String(80)), sa.Column("branch", sa.String(80)), sa.Column("country", sa.String(80)), sa.Column("ip_address", sa.String(64)), sa.Column("channel", sa.String(40)), sa.Column("status", sa.String(20), nullable=False), sa.Column("transaction_time", sa.DateTime(timezone=True), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_transactions_reference", "transactions", ["reference"], unique=True)
    op.create_index("ix_transactions_status", "transactions", ["status"])
    op.create_index("ix_transactions_branch", "transactions", ["branch"])
    op.create_index("ix_transactions_user_created", "transactions", ["user_id", "created_at"])
    op.create_table("risk_scores", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("transaction_id", sa.Integer(), sa.ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False), sa.Column("score", sa.Integer(), nullable=False), sa.Column("level", sa.String(20), nullable=False), sa.Column("classification", sa.String(20), nullable=False), sa.Column("reasons", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.CheckConstraint("score >= 0 AND score <= 100", name="ck_risk_score_range"))
    op.create_index("ix_risk_scores_transaction_id", "risk_scores", ["transaction_id"], unique=True)
    op.create_table("fraud_reports", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("transaction_id", sa.Integer(), sa.ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False), sa.Column("status", sa.String(30), nullable=False), sa.Column("summary", sa.Text(), nullable=False), sa.Column("assigned_to", sa.String(255)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("audit_logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL")), sa.Column("action", sa.String(80), nullable=False), sa.Column("entity", sa.String(80), nullable=False), sa.Column("entity_id", sa.String(80)), sa.Column("ip_address", sa.String(64)), sa.Column("metadata_json", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("notifications", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")), sa.Column("title", sa.String(255), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("severity", sa.String(20), nullable=False), sa.Column("is_read", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))


def downgrade():
    op.drop_table("notifications")
    op.drop_table("audit_logs")
    op.drop_table("fraud_reports")
    op.drop_table("risk_scores")
    op.drop_table("transactions")
    op.drop_table("system_settings")
    op.drop_table("users")
