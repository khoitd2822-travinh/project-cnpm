from datetime import datetime
from sqlalchemy import text

class AuditRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_log(self, user_id, action, details):
        query = text("""
            INSERT INTO audit_logs (user_id, action, details, timestamp)
            VALUES (:u, :a, :d, :t)
        """)
        self.db_session.execute(query, {
            "u": user_id,
            "a": action,
            "d": details,
            "t": datetime.now()
        })
        self.db_session.commit()  # 🔥 BẮT BUỘC
