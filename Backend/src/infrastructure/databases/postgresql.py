from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from infrastructure.databases.base import Base

DATABASE_URI = Config.DATABASE_URI

engine = create_engine(
    DATABASE_URI,
    pool_pre_ping=True,   
    echo=False            
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_postgresql(app=None):
    Base.metadata.create_all(bind=engine)
