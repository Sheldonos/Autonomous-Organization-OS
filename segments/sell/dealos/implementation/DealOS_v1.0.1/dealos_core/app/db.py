from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

kwargs={}
if settings.database_url.startswith('sqlite'):
    kwargs['connect_args']={'check_same_thread':False}
engine=create_engine(settings.database_url, pool_pre_ping=True, **kwargs)
SessionLocal=sessionmaker(bind=engine, autocommit=False, autoflush=False)
class Base(DeclarativeBase): pass

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
