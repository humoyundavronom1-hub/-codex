import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.db.session import Base, engine, SessionLocal
from backend.models import models  # noqa: F401
from backend.api.routes import router
from backend.services.bootstrap import seed_admin

load_dotenv()
logging.basicConfig(level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper(), logging.INFO))
logger = logging.getLogger('backend')

app = FastAPI(title='Telegram Moderation API', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_admin(db)
    db.close()
    logger.info('Backend ishga tushdi')

app.include_router(router, prefix='/api')

@app.get('/health')
def health():
    return {'status': 'ok'}
