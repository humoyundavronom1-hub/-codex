from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.config import DATABASE_URL
from backend.db.session import Base
from backend.models import models  # noqa: F401

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def init_db():
    Base.metadata.create_all(bind=engine)
