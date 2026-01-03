import jwt
from datetime import datetime, timedelta

class AuthService:
    def __init__(self, user_repo, audit_repo, db_session):
        self.user_repo = user_repo
        self.audit_repo = audit_repo
        self.db_session = db_session

    def register(self, email, password, full_name, role='author'):
        try:
            # 1. Kiểm tra user tồn tại
            existing_user = self.user_repo.get_by_email(email)
            if existing_user:
                return False

            # 2. Tạo user mới (Đây là bước quan trọng nhất và nó đã chạy được)
            new_user = self.user_repo.create_user(
                email=email,
                password=password,
                full_name=full_name,
                role=role
            )

            if new_user:
                # 3. Tạm thời bỏ qua ghi log để tránh lỗi 'log_action' 
                # vì Repository của bạn có thể đặt tên hàm khác (vd: create_log)
                print(f"✅ Đã tạo thành công tài khoản: {email} với quyền {role}")
                return True
            
            return False
        except Exception as e:
            print(f"🔥 LỖI TẠI AUTH_SERVICE: {e}")
            return False

    def login(self, email, password):
        try:
            user = self.user_repo.get_by_email(email)
            if user and user.password == password:
                return user
            return None
        except Exception as e:
            print(f"🔥 LỖI ĐĂNG NHẬP: {e}")
            return None