"""initial

Revision ID: 0001_initial
Revises:
Create Date: 2026-02-08
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('admins', sa.Column('id', sa.Integer, primary_key=True), sa.Column('email', sa.String(255), nullable=False, unique=True), sa.Column('password_hash', sa.String(255), nullable=False), sa.Column('full_name', sa.String(255), nullable=False), sa.Column('is_active', sa.Boolean, default=True), sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')))
    op.create_table('groups', sa.Column('id', sa.Integer, primary_key=True), sa.Column('telegram_group_id', sa.String(64), nullable=False, unique=True), sa.Column('title', sa.String(255), nullable=False), sa.Column('is_enabled', sa.Boolean, default=True), sa.Column('invite_required', sa.Integer, default=3), sa.Column('reset_on_leave', sa.Boolean, default=False), sa.Column('ignore_bots', sa.Boolean, default=True), sa.Column('admins_bypass', sa.Boolean, default=True), sa.Column('auto_kick_timeout', sa.Integer, default=3600), sa.Column('risk_threshold', sa.Float, default=0.65), sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')))
    op.create_table('users', sa.Column('id', sa.Integer, primary_key=True), sa.Column('telegram_user_id', sa.String(64), nullable=False, unique=True), sa.Column('username', sa.String(255)), sa.Column('full_name', sa.String(255), nullable=False), sa.Column('is_bot', sa.Boolean, default=False), sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')))
    op.create_table('user_progress', sa.Column('id', sa.Integer, primary_key=True), sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id')), sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')), sa.Column('invites_count', sa.Integer, default=0), sa.Column('required_invites', sa.Integer, default=3), sa.Column('unlocked', sa.Boolean, default=False), sa.Column('muted', sa.Boolean, default=True), sa.UniqueConstraint('group_id','user_id', name='uq_group_user_progress'))
    op.create_table('invite_logs', sa.Column('id', sa.Integer, primary_key=True), sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id')), sa.Column('inviter_user_id', sa.Integer, sa.ForeignKey('users.id')), sa.Column('invited_user_id', sa.Integer, sa.ForeignKey('users.id')), sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')))
    op.create_table('messages_log', sa.Column('id', sa.Integer, primary_key=True), sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id')), sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')), sa.Column('message_type', sa.String(50), default='text'), sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')))
    op.create_table('user_daily_stats', sa.Column('id', sa.Integer, primary_key=True), sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')), sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id')), sa.Column('day', sa.String(10), nullable=False), sa.Column('invites', sa.Integer, default=0), sa.Column('messages', sa.Integer, default=0), sa.UniqueConstraint('user_id','group_id','day', name='uq_user_group_day'))
    op.create_table('group_daily_stats', sa.Column('id', sa.Integer, primary_key=True), sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id')), sa.Column('day', sa.String(10), nullable=False), sa.Column('joins', sa.Integer, default=0), sa.Column('leaves', sa.Integer, default=0), sa.Column('unlocks', sa.Integer, default=0), sa.Column('messages', sa.Integer, default=0), sa.UniqueConstraint('group_id','day', name='uq_group_day'))
    op.create_table('risk_scores', sa.Column('id', sa.Integer, primary_key=True), sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')), sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id')), sa.Column('score', sa.Float, default=0), sa.Column('reasons', sa.Text, default=''), sa.UniqueConstraint('user_id','group_id', name='uq_risk_user_group'))
    op.create_table('audit_logs', sa.Column('id', sa.Integer, primary_key=True), sa.Column('actor_admin_id', sa.Integer, sa.ForeignKey('admins.id'), nullable=True), sa.Column('action', sa.String(255), nullable=False), sa.Column('details', sa.Text, default=''), sa.Column('severity', sa.String(20), default='info'), sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')))

def downgrade():
    for t in ['audit_logs','risk_scores','group_daily_stats','user_daily_stats','messages_log','invite_logs','user_progress','users','groups','admins']:
        op.drop_table(t)
