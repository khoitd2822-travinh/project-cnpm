import sys
import os
from flask import Flask, g
from flask_cors import CORS

# ================== FIX IMPORT PATH ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ================== LỚP USER GIẢ LẬP ==================
class User:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

# ================== FLASK APP ==================
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ================== DATABASE ==================
from infrastructure.databases.postgresql import init_postgresql, SessionLocal
init_postgresql(app)

from infrastructure.persistence.user_repository import UserRepository
from infrastructure.persistence.audit_repository import AuditRepository
from services.auth_service import AuthService

# Ghi đè để chắc chắn UserRepository không đòi hỏi sai tham số
UserRepository.__init__ = lambda self, db_session: setattr(self, 'db_session', db_session)

def get_auth_service():
    if "auth_service" not in g:
        db_session = SessionLocal()
        g.db_session = db_session
        g.auth_service = AuthService(
            user_repo=UserRepository(db_session),
            audit_repo=AuditRepository(db_session),
            db_session=db_session
        )
    return g.auth_service

@app.teardown_appcontext
def close_db_session(exception=None):
    db_session = g.pop("db_session", None)
    if db_session:
        db_session.close()

from api.controllers.auth_controller import auth_bp
auth_bp.auth_service_factory = get_auth_service
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def health_check():
    return "Hệ thống đã sẵn sàng!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)