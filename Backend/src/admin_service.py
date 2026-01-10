
# admin_service.py
from datetime import datetime

class AdminService:
    def __init__(self, db):
        # db là kết nối tới Postgres của bạn
        self.db = db 

    # 1. Chức năng Quản lý User (Khớp với cụm Manage User trong sơ đồ)
    def get_all_users(self):
        # Lấy danh sách để hiện lên bảng Dashboard
        return self.db.execute("SELECT id, fullname, email, role FROM users").fetchall()

    def update_user_role(self, user_id, new_role):
        # Nâng cấp hoặc hạ bậc thành viên
        self.db.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
        self.log_event(f"Admin updated User {user_id} to role {new_role}")

    # 2. Chức năng Thiết lập Hội nghị (Khớp với Setup Conference / Manage Timeline)
    def setup_conference(self, name, location, deadline):
        query = "INSERT INTO conference (name, location, submission_deadline) VALUES (%s, %s, %s)"
        self.db.execute(query, (name, location, deadline))
        self.log_event(f"Admin setup new conference: {name}")

    # 3. Chức năng Ghi nhật ký (Khớp với View Active Log)
    def log_event(self, action):
        # Lưu vào bảng AuditLogs trong Postgres
        query = "INSERT INTO AuditLogs (action, timestamp) VALUES (%s, %s)"
        self.db.execute(query, (action, datetime.now()))