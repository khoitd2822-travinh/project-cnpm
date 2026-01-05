import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "th_conf_ms_secret_key_2026"

    DB_USER = os.environ.get("DB_USER") or "postgres"
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or "1234"  # ← mật khẩu PostgreSQL 15
    DB_HOST = os.environ.get("DB_HOST") or "127.0.0.1"
    DB_PORT = os.environ.get("DB_PORT") or "5432"
    DB_NAME = os.environ.get("DB_NAME") or "project_cnpm"

    DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
