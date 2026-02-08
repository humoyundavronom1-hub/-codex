from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.auth.security import decode_token
from backend.models.models import Admin

security = HTTPBearer()

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> Admin:
    try:
        payload = decode_token(credentials.credentials)
        admin_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Token yaroqsiz")
    admin = db.get(Admin, admin_id)
    if not admin or not admin.is_active:
        raise HTTPException(status_code=401, detail="Admin topilmadi")
    return admin
