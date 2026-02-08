from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.db.session import get_db
from backend.models.models import Admin, Group, User, UserProgress, RiskScore, AuditLog
from backend.api.schemas import LoginRequest, GroupRuleUpdate, ManualUnlockRequest, ResetProgressRequest
from backend.auth.security import verify_password, create_access_token
from backend.auth.deps import get_current_admin
from backend.analytics.engine import dashboard_kpi, leaderboards

router = APIRouter()

@router.post('/auth/login')
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == payload.email).first()
    if not admin or not verify_password(payload.password, admin.password_hash):
        raise HTTPException(status_code=401, detail='Login xato')
    token = create_access_token(str(admin.id))
    return {'access_token': token, 'token_type': 'bearer'}

@router.get('/dashboard/kpi')
def get_kpi(_: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return dashboard_kpi(db)

@router.get('/groups')
def list_groups(_: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    rows = db.query(Group).all()
    return [r.__dict__ | {"_sa_instance_state": None} for r in rows]

@router.put('/groups/{group_id}/rules')
def update_group_rules(group_id: int, payload: GroupRuleUpdate, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    group = db.get(Group, group_id)
    if not group:
        raise HTTPException(status_code=404, detail='Guruh topilmadi')
    for key, value in payload.model_dump().items():
        setattr(group, key, value)
    db.add(AuditLog(actor_admin_id=admin.id, action='group_rules_update', details=f'group_id={group_id}', severity='info'))
    db.commit()
    return {'status': 'ok'}

@router.get('/users')
def list_users(_: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    out = []
    for u in users:
        risk = db.query(RiskScore).filter(RiskScore.user_id == u.id).order_by(RiskScore.updated_at.desc()).first()
        progress = db.query(func.sum(UserProgress.invites_count), func.max(UserProgress.unlocked)).filter(UserProgress.user_id == u.id).first()
        out.append({
            'id': u.id,
            'telegram_user_id': u.telegram_user_id,
            'full_name': u.full_name,
            'username': u.username,
            'risk_score': float(risk.score) if risk else 0,
            'invites': int(progress[0] or 0),
            'unlocked_any': bool(progress[1]) if progress else False
        })
    return out

@router.post('/users/manual-unlock')
def manual_unlock(payload: ManualUnlockRequest, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    progress = db.query(UserProgress).filter(UserProgress.group_id == payload.group_id, UserProgress.user_id == payload.user_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail='Progress topilmadi')
    progress.unlocked = True
    progress.muted = False
    db.add(AuditLog(actor_admin_id=admin.id, action='manual_unlock', details=f'user={payload.user_id},group={payload.group_id}', severity='warning'))
    db.commit()
    return {'status': 'ok'}

@router.post('/users/reset')
def reset_user(payload: ResetProgressRequest, admin: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    progress = db.query(UserProgress).filter(UserProgress.group_id == payload.group_id, UserProgress.user_id == payload.user_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail='Progress topilmadi')
    progress.invites_count = 0
    progress.unlocked = False
    progress.muted = True
    db.add(AuditLog(actor_admin_id=admin.id, action='reset_progress', details=f'user={payload.user_id},group={payload.group_id}', severity='warning'))
    db.commit()
    return {'status': 'ok'}

@router.get('/leaderboards')
def get_leaderboards(_: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return leaderboards(db)

@router.get('/analytics/unlock-funnel')
def unlock_funnel(_: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    total = db.query(func.count(UserProgress.id)).scalar() or 0
    unlocked = db.query(func.count(UserProgress.id)).filter(UserProgress.unlocked == True).scalar() or 0
    return {'joined': total, 'unlocked': unlocked, 'locked': max(total - unlocked, 0)}

@router.get('/logs')
def get_logs(_: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(200).all()
    return [{'id': l.id, 'action': l.action, 'details': l.details, 'severity': l.severity, 'created_at': str(l.created_at)} for l in logs]

@router.get('/settings')
def settings(_: Admin = Depends(get_current_admin)):
    return {
        'admin_management': True,
        'password_change': True,
        'api_keys': True,
        'audit_log_retention_days': 180,
        'branding': 'logo_upload_enabled'
    }
