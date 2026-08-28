"""initial schema: users, wallets, transactions, ussd_sessions

Revision ID: 507ba55bd730
Revises: 
Create Date: 2026-08-27 14:38:52.440581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '507ba55bd730'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Transaction Types ────────────────────────────────────────────
    transaction_type = sa.Enum(
        'fund', 'send', 'receive', 'spend', 'swap',
        name='transactiontype',
    )
    transaction_type.create(op.get_bind(), checkfirst=True)

    transaction_status = sa.Enum(
        'initiated', 'pending', 'processing', 'settled', 'failed', 'reversed',
        name='transactionstatus',
    )
    transaction_status.create(op.get_bind(), checkfirst=True)

    # ── Users ────────────────────────────────────────────────────────
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('phone_number', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(100), nullable=False, server_default='User'),
        sa.Column('email', sa.String(255), unique=True, nullable=True),
        sa.Column('pin_hash', sa.String(128), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('is_verified', sa.Boolean(), server_default='false'),
        sa.Column('kyc_level', sa.String(20), server_default='none'),
        sa.Column('kyc_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('preferred_currency', sa.String(3), server_default='UGX'),
        sa.Column('preferred_language', sa.String(5), server_default='en'),
        sa.Column('daily_limit_usd', sa.Float(), server_default='500'),
        sa.Column('monthly_limit_usd', sa.Float(), server_default='5000'),
        sa.Column('country', sa.String(3), server_default='UG'),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_ussd_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Wallets ──────────────────────────────────────────────────────
    op.create_table(
        'wallets',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), unique=True, nullable=False),
        sa.Column('balance_sats', sa.BigInteger(), server_default='0'),
        sa.Column('reserved_sats', sa.BigInteger(), server_default='0'),
        sa.Column('lnd_pubkey', sa.String(66), nullable=True),
        sa.Column('lnd_address', sa.String(255), nullable=True),
        sa.Column('card_number', sa.String(19), nullable=True),
        sa.Column('card_last4', sa.String(4), nullable=True),
        sa.Column('card_expiry', sa.String(5), nullable=True),
        sa.Column('card_status', sa.String(20), server_default='inactive'),
        sa.Column('daily_spent_sats', sa.BigInteger(), server_default='0'),
        sa.Column('daily_spent_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('monthly_spent_sats', sa.BigInteger(), server_default='0'),
        sa.Column('monthly_spent_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint('balance_sats >= 0', name='positive_balance'),
        sa.CheckConstraint('reserved_sats >= 0', name='positive_reserved'),
    )

    # ── Transactions ─────────────────────────────────────────────────
    op.create_table(
        'transactions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('type', transaction_type, nullable=False),
        sa.Column('status', transaction_status, server_default='initiated'),
        sa.Column('reference', sa.String(50), unique=True, nullable=False),
        sa.Column('amount_fiat', sa.Float(), nullable=False),
        sa.Column('currency_fiat', sa.String(3), nullable=False),
        sa.Column('amount_sats', sa.BigInteger(), nullable=False),
        sa.Column('fee_sats', sa.BigInteger(), server_default='0'),
        sa.Column('rate_used', sa.Float(), nullable=False),
        sa.Column('rate_source', sa.String(20), server_default='coingecko'),
        sa.Column('provider', sa.String(30), nullable=False),
        sa.Column('provider_txn_id', sa.String(100), nullable=True),
        sa.Column('provider_status', sa.String(30), nullable=True),
        sa.Column('payment_hash', sa.String(64), nullable=True),
        sa.Column('payment_request', sa.Text(), nullable=True),
        sa.Column('destination_pubkey', sa.String(66), nullable=True),
        sa.Column('phone_number', sa.String(20), nullable=True),
        sa.Column('merchant_name', sa.String(100), nullable=True),
        sa.Column('description', sa.Text(), server_default=''),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column('initiated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('pending_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('processing_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('settled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('failed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_tx_user_created', 'transactions', ['user_id', 'created_at'])
    op.create_index('idx_tx_status', 'transactions', ['status'])
    op.create_index('idx_tx_provider_txn', 'transactions', ['provider_txn_id'])

    # ── USSD Sessions ────────────────────────────────────────────────
    op.create_table(
        'ussd_sessions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('session_id', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('phone_number', sa.String(20), nullable=False, index=True),
        sa.Column('current_screen', sa.String(50), server_default='main_menu'),
        sa.Column('accumulated_input', sa.Text(), nullable=True),
        sa.Column('menu_depth', sa.Integer(), server_default='0'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('last_request_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('ussd_sessions')
    op.drop_index('idx_tx_provider_txn', table_name='transactions')
    op.drop_index('idx_tx_status', table_name='transactions')
    op.drop_index('idx_tx_user_created', table_name='transactions')
    op.drop_table('transactions')
    op.drop_table('wallets')
    op.drop_table('users')

    sa.Enum(name='transactionstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='transactiontype').drop(op.get_bind(), checkfirst=True)
