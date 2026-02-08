from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.models.models import Group, UserProgress, InviteLog, MessagesLog, User, UserDailyStats

def dashboard_kpi(db: Session):
    total_groups = db.query(func.count(Group.id)).scalar() or 0
    restricted_users = db.query(func.count(UserProgress.id)).filter(UserProgress.unlocked == False).scalar() or 0
    unlocked_total = db.query(func.count(UserProgress.id)).filter(UserProgress.unlocked == True).scalar() or 0
    all_progress = db.query(func.count(UserProgress.id)).scalar() or 1
    unlock_rate = round((unlocked_total / all_progress) * 100, 2)
    invites_today = db.query(func.count(InviteLog.id)).filter(func.date(InviteLog.created_at) == func.date('now')).scalar() or 0
    spam_alerts = db.query(func.count(User.id)).filter(User.is_bot == True).scalar() or 0
    return {
        "total_groups": total_groups,
        "restricted_users": restricted_users,
        "unlock_rate": unlock_rate,
        "invites_today": invites_today,
        "spam_alerts": spam_alerts,
    }

def leaderboards(db: Session):
    top_inviters = db.query(User.full_name, func.count(InviteLog.id).label("count")).join(InviteLog, InviteLog.inviter_user_id == User.id).group_by(User.id).order_by(func.count(InviteLog.id).desc()).limit(10).all()
    top_talkers = db.query(User.full_name, func.count(MessagesLog.id).label("count")).join(MessagesLog, MessagesLog.user_id == User.id).group_by(User.id).order_by(func.count(MessagesLog.id).desc()).limit(10).all()
    most_active = db.query(User.full_name, func.sum(UserDailyStats.messages + UserDailyStats.invites).label("score")).join(UserDailyStats, UserDailyStats.user_id == User.id).group_by(User.id).order_by(func.sum(UserDailyStats.messages + UserDailyStats.invites).desc()).limit(10).all()
    return {
        "top_inviters": [{"name": r[0], "count": int(r[1] or 0)} for r in top_inviters],
        "top_talkers": [{"name": r[0], "count": int(r[1] or 0)} for r in top_talkers],
        "most_active": [{"name": r[0], "score": int(r[1] or 0)} for r in most_active],
    }
