import os

class Config:
    # Sửa tên biến từ SQLALCHEMY_DATABASE_URI thành DATABASE_URI
    DATABASE_URI = "postgresql+psycopg2://postgres:1234@127.0.0.1:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = "your_secret_key_here"