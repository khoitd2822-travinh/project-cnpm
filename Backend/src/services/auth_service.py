
import jwt # Thư viện tạo Token
from datetime import datetime, timedelta

class authservice:
    def __init__(self, user_repo, audit_repo):
        self.user_repo = user_repo
        self.audit_repo = audit_repo

    def login(self, email, password):
        # Bước 4: Gọi Repository lấy User theo email
        user = self.user_repo.get_by_email(email)
        
        # Bước 8: Kiểm tra mật khẩu (password == user.password)
        if user and user.password == password:
            # Bước 9: Tạo Audit Log thành công
            self.audit_repo.create_log(user.user_id, "LOGIN", "Login Success")
            
            # Bước 8: Tạo mã JWT Token chứa Role để điều hướng
            token = self.generate_token(user)
            
            # Bước 14: Trả về Token và Role cho Controller
            return {"token": token, "role": user.role}
        
        # Bước 12: Nếu sai mật khẩu, báo lỗi
        return None

    
    def generate_token(self, user):
        payload = {
            "user_id": user.user_id,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, "SECRET_KEY", algorithm="HS256")
    
    def register(self, email, password, full_name):
        # 1. Kiểm tra xem email đã tồn tại chưa
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            return None # Email đã được dùng

        # 2. Gọi Repository để lưu user mới vào Database
        # Mặc định role là 'user', bạn có thể chỉnh lại
        new_user = self.user_repo.create_user(email, password, full_name, role="user")

        if new_user:
            # 3. Ghi log đăng ký thành công
            self.audit_repo.create_log(new_user.user_id, "REGISTER", "User registered successfully")
            return True
        
        return False