from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.models import Group, User, UserProgress, InviteLog, MessagesLog, UserDailyStats, GroupDailyStats, RiskScore

def get_or_create_group(db: Session, chat_id: str, title: str) -> Group:
    g = db.query(Group).filter(Group.telegram_group_id == str(chat_id)).first()
    if not g:
        g = Group(telegram_group_id=str(chat_id), title=title)
        db.add(g); db.commit(); db.refresh(g)
    return g

def get_or_create_user(db: Session, tg_user) -> User:
    u = db.query(User).filter(User.telegram_user_id == str(tg_user.id)).first()
    if not u:
        name = (tg_user.first_name or '') + (' ' + tg_user.last_name if tg_user.last_name else '')
        u = User(telegram_user_id=str(tg_user.id), username=tg_user.username, full_name=name.strip() or str(tg_user.id), is_bot=tg_user.is_bot)
        db.add(u); db.commit(); db.refresh(u)
    return u

def ensure_progress(db: Session, group: Group, user: User):
    p = db.query(UserProgress).filter(UserProgress.group_id == group.id, UserProgress.user_id == user.id).first()
    if not p:
        p = UserProgress(group_id=group.id, user_id=user.id, required_invites=group.invite_required, invites_count=0, muted=True, unlocked=False)
        db.add(p); db.commit(); db.refresh(p)
    return p

def increment_invite(db: Session, group: Group, inviter: User, invited: User):
    if invited.is_bot and group.ignore_bots:
        return None
    db.add(InviteLog(group_id=group.id, inviter_user_id=inviter.id, invited_user_id=invited.id))
    p = ensure_progress(db, group, inviter)
    p.invites_count += 1
    if p.invites_count >= p.required_invites:
        p.unlocked = True
        p.muted = False
    _upsert_daily(db, inviter.id, group.id, invites=1)
    _group_daily(db, group.id, joins=1)
    _risk_recalc(db, inviter.id, group.id)
    db.commit()
    db.refresh(p)
    return p

def log_message(db: Session, group: Group, user: User):
    db.add(MessagesLog(group_id=group.id, user_id=user.id, message_type='text'))
    _upsert_daily(db, user.id, group.id, messages=1)
    _group_daily(db, group.id, messages=1)
    _risk_recalc(db, user.id, group.id)
    db.commit()

def _upsert_daily(db: Session, user_id: int, group_id: int, invites=0, messages=0):
    d = date.today().isoformat()
    row = db.query(UserDailyStats).filter(UserDailyStats.user_id==user_id, UserDailyStats.group_id==group_id, UserDailyStats.day==d).first()
    if not row:
        row = UserDailyStats(user_id=user_id, group_id=group_id, day=d, invites=0, messages=0)
        db.add(row)
    row.invites += invites
    row.messages += messages

def _group_daily(db: Session, group_id: int, joins=0, leaves=0, unlocks=0, messages=0):
    d = date.today().isoformat()
    row = db.query(GroupDailyStats).filter(GroupDailyStats.group_id==group_id, GroupDailyStats.day==d).first()
    if not row:
        row = GroupDailyStats(group_id=group_id, day=d, joins=0, leaves=0, unlocks=0, messages=0)
        db.add(row)
    row.joins += joins
    row.leaves += leaves
    row.unlocks += unlocks
    row.messages += messages

def _risk_recalc(db: Session, user_id: int, group_id: int):
    invites = db.query(func.count(InviteLog.id)).filter(InviteLog.group_id==group_id, InviteLog.inviter_user_id==user_id).scalar() or 0
    msgs = db.query(func.count(MessagesLog.id)).filter(MessagesLog.group_id==group_id, MessagesLog.user_id==user_id).scalar() or 0
    score = max(0.0, min(1.0, 1.0 - ((invites * 0.15) + (msgs * 0.01))))
    reasons = 'low activity' if score > 0.7 else 'normal'
    row = db.query(RiskScore).filter(RiskScore.user_id==user_id, RiskScore.group_id==group_id).first()
    if not row:
        row = RiskScore(user_id=user_id, group_id=group_id)
        db.add(row)
    row.score = score
    row.reasons = reasons
