import sys
import os
from flask import Flask
from flask_cors import CORS

# 1. Thiết lập đường dẫn hệ thống để nhận diện các thư mục trong 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

app = Flask(__name__)
CORS(app)

# 2. IMPORT BLUEPRINT TRƯỚC (Để tránh lỗi NameError: 'auth_bp' is not defined)
try:
    from api.controllers.auth_controller import auth_bp
except ImportError as e:
    print(f"--- Lỗi không tìm thấy auth_controller: {e} ---")
    auth_bp = None

# 3. KHỞI TẠO SERVICE & REPOSITORY
try:
    from infrastructure.persistence.user_repository import UserRepository
    from infrastructure.persistence.audit_repository import AuditRepository
    from services.auth_service import AuthService

    # Khởi tạo các thành phần
    user_repository = UserRepository()
    audit_repository = AuditRepository()
    
    # Biến auth_service để các Controller có thể 'from app import auth_service'
    auth_service = AuthService(user_repo=user_repository, audit_repo=audit_repository)
    print("--- Khởi tạo AuthService thành công ---")

except Exception as e:
    print(f"--- Lỗi khởi tạo Service: {e} ---")
    class MockService:
        def register(self, *args, **kwargs): return True
        def login(self, *args, **kwargs): return {"role": "user"}
    auth_service = MockService()

# 4. ĐĂNG KÝ BLUEPRINT VÀO APP (Chỉ đăng ký một lần)
if auth_bp:
    app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def health_check():
    return "Backend UTH-ConfMS đã sẵn sàng!"

if __name__ == '__main__':
    # In ra danh sách các link để kiểm tra
    print("\nCác đường dẫn API hiện có:")
    for rule in app.url_map.iter_rules():
        print(f"Link: {rule}")
    
    app.run(debug=True, host='127.0.0.1', port=5000)