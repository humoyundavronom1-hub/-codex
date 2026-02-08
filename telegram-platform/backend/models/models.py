from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, UniqueConstraint, Index
from sqlalchemy.sql import func
from backend.db.session import Base

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    telegram_group_id = Column(String(64), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    is_enabled = Column(Boolean, default=True)
    invite_required = Column(Integer, default=3)
    reset_on_leave = Column(Boolean, default=False)
    ignore_bots = Column(Boolean, default=True)
    admins_bypass = Column(Boolean, default=True)
    auto_kick_timeout = Column(Integer, default=3600)
    risk_threshold = Column(Float, default=0.65)
    created_at = Column(DateTime, server_default=func.now())

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(String(64), unique=True, nullable=False)
    username = Column(String(255))
    full_name = Column(String(255), nullable=False)
    is_bot = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class UserProgress(Base):
    __tablename__ = "user_progress"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invites_count = Column(Integer, default=0)
    required_invites = Column(Integer, default=3)
    unlocked = Column(Boolean, default=False)
    muted = Column(Boolean, default=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    __table_args__ = (UniqueConstraint("group_id", "user_id", name="uq_group_user_progress"),)

class InviteLog(Base):
    __tablename__ = "invite_logs"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    inviter_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invited_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class MessagesLog(Base):
    __tablename__ = "messages_log"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_type = Column(String(50), default="text")
    created_at = Column(DateTime, server_default=func.now())

class UserDailyStats(Base):
    __tablename__ = "user_daily_stats"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    day = Column(String(10), nullable=False)
    invites = Column(Integer, default=0)
    messages = Column(Integer, default=0)
    __table_args__ = (UniqueConstraint("user_id", "group_id", "day", name="uq_user_group_day"),)

class GroupDailyStats(Base):
    __tablename__ = "group_daily_stats"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    day = Column(String(10), nullable=False)
    joins = Column(Integer, default=0)
    leaves = Column(Integer, default=0)
    unlocks = Column(Integer, default=0)
    messages = Column(Integer, default=0)
    __table_args__ = (UniqueConstraint("group_id", "day", name="uq_group_day"),)

class RiskScore(Base):
    __tablename__ = "risk_scores"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    score = Column(Float, default=0.0)
    reasons = Column(Text, default="")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    __table_args__ = (UniqueConstraint("user_id", "group_id", name="uq_risk_user_group"),)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    actor_admin_id = Column(Integer, ForeignKey("admins.id"), nullable=True)
    action = Column(String(255), nullable=False)
    details = Column(Text, default="")
    severity = Column(String(20), default="info")
    created_at = Column(DateTime, server_default=func.now())

Index("idx_invite_logs_group_inviter", InviteLog.group_id, InviteLog.inviter_user_id)
Index("idx_messages_log_group_user", MessagesLog.group_id, MessagesLog.user_id)
Index("idx_user_progress_group_unlocked", UserProgress.group_id, UserProgress.unlocked)
Index("idx_audit_logs_created", AuditLog.created_at)
