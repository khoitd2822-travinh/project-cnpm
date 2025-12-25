# Import entity User mà bạn đã tạo ở folder domain
from src.domain.user import User

class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_by_email(self, email):
        # Đây là bước 5: SELECT * FROM users WHERE email = ...
        # Giả sử dùng SQLAlchemy (đề bài yêu cầu Postgres)
        user_data = self.db_session.execute(
            "SELECT user_id, username, password, role FROM users WHERE username = :email",
            {"email": email}
        ).fetchone()

        if user_data:
            # Đây là bước 7: Trả về User Entity cho Service
            return User(
                user_id=user_data['user_id'],
                username=user_data['username'],
                password=user_data['password'], # password đã hash trong DB
                role=user_data['role']
            )
        return None