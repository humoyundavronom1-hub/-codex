import os
from sqlalchemy.orm import Session
from backend.models.models import Admin
from backend.auth.security import hash_password

def seed_admin(db: Session):
    email = os.getenv("ADMIN_EMAIL", "admin@gov.local")
    password = os.getenv("ADMIN_PASSWORD", "ChangeMe123!")
    exists = db.query(Admin).filter(Admin.email == email).first()
    if not exists:
        db.add(Admin(email=email, password_hash=hash_password(password), full_name="System Admin"))
        db.commit()
