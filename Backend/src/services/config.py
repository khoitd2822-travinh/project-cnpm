import os

class Config:
    """Base configuration."""
    # Khóa bí mật để mã hóa Token
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uth_conf_ms_secret_key_2026'
    
    # Cấu hình Database - HÃY KIỂM TRA MẬT KHẨU TẠI ĐÂY
    # Cấu trúc: postgresql+psycopg2://user:password@host:port/dbname
    # Tôi đổi localhost thành 127.0.0.1 để tránh lỗi IPv6 (::1) mà bạn gặp trong log
    DB_USER = os.environ.get('DB_USER') or 'postgres'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or '1234'  # <--- THAY MẬT KHẨU THẬT Ở ĐÂY
    DB_HOST = os.environ.get('DB_HOST') or '127.0.0.1'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_NAME = os.environ.get('DB_NAME') or 'postgres' # Đảm bảo tên DB này tồn tại trong pgAdmin

    DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    DEBUG = False
    TESTING = False
    CORS_HEADERS = 'Content-Type'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Cấu hình Swagger cho tài liệu API
class SwaggerConfig:
    """Swagger configuration."""
    template = {
        "swagger": "2.0",
        "info": {
            "title": "UTH-ConfMS API",
            "description": "API hệ thống quản lý hội nghị UTH",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"]
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }