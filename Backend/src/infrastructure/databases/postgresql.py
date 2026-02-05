import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from infrastructure.databases.base import Base

# Load .env from Backend folder (parent of src)
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Use DATABASE_URL from .env, fallback to Config, then fallback to default
DATABASE_URI = os.getenv('DATABASE_URL') or Config.DATABASE_URI or "postgresql+psycopg2://postgres:1234@127.0.0.1:5432/postgres"

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