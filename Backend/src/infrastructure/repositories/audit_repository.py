from datetime import datetime

class AuditRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_log(self, user_id, action, details):
        # Thực hiện insert vào bảng AuditLogs như sơ đồ Database
        query = "INSERT INTO AuditLogs (user_id, action, details, timestamp) VALUES (:u, :a, :d, :t)"
        self.db_session.execute(query, {
            "u": user_id, 
            "a": action, 
            "d": details, 
            "t": datetime.now()
        })