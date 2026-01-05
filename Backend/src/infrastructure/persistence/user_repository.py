from sqlalchemy import text
from src.domain.user import User

class UserRepository:
    def __init__(self, db_session):
        # UserRepository chỉ cần db_session để làm việc với Database
        self.db_session = db_session

    def get_by_email(self, email):
        # Sử dụng dấu sao hoặc chỉ định rõ để tránh nhầm vị trí cột
        query = text("""
            SELECT user_id, username, password, role 
            FROM users 
            WHERE email = :email
        """)
        result = self.db_session.execute(query, {"email": email.lower().strip()})
        row = result.fetchone()

        if row:
            # row[0]=user_id, row[1]=username, row[2]=password, row[3]=role
            return User(
                user_id=row[0],
                username=row[1],
                password=row[2], 
                role=row[3]
            )
        return None

    def create_user(self, email, password, full_name, role):
        username = email.lower().split("@")[0]

        query = text("""
            INSERT INTO users (username, email, password, full_name, role)
            VALUES (:username, :email, :password, :full_name, :role)
            RETURNING user_id
        """)

        values = {
            "username": username,
            "email": email.lower().strip(),
            "password": password,
            "full_name": full_name,
            "role": role
        }

        result = self.db_session.execute(query, values)
        self.db_session.commit()

        new_id = result.fetchone()[0]

        return User(
            user_id=new_id,
            username=username,
            password=password,
            role=role
        )