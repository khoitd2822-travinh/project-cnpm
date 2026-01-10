import os
import sys

# Tự động thêm thư mục cha vào hệ thống để nhận diện module 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import text

# Bây giờ bạn có thể dùng 'from src...' mà không lo lỗi đường dẫn
from infrastructure.databases.postgresql import init_postgresql, SessionLocal

app = Flask(__name__)
CORS(app)

# Khởi tạo DB
init_postgresql(app)
# --- HÀM TÍNH THỜI GIAN ---
def human_time_diff(dt):
    if not dt:
        return "Không rõ"
    now = datetime.now()
    diff = now - dt
    seconds = int(diff.total_seconds())

    if seconds >= 25000 and seconds <= 25400:
        dt = dt + timedelta(hours=7)
        diff = now - dt
        seconds = int(diff.total_seconds())
    
    if seconds < 5: return "Vừa xong"
    if seconds < 60: return f"{seconds} giây trước"
    if seconds < 3600: return f"{seconds // 60} phút trước"
    if seconds < 86400: return f"{seconds // 3600} giờ trước"
    return dt.strftime('%d/%m/%Y %H:%M')

# --- ĐĂNG KÝ ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    db = SessionLocal()
    try:
        query = text("""
            INSERT INTO users (full_name, username, email, password, role, created_at) 
            VALUES (:fn, :un, :em, :pw, :rl, :ca)
        """)
        db.execute(query, {
            "fn": data['full_name'],
            "un": data['email'],
            "em": data['email'],
            "pw": data['password'],
            "rl": data['role'],
            "ca": datetime.now()
        })
        db.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"detail": str(e)}), 400
    finally:
        db.close()

# --- ĐĂNG NHẬP ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    db = SessionLocal()
    try:
        query = text("SELECT full_name, role, password FROM users WHERE email = :em")
        user = db.execute(query, {"em": data['username']}).fetchone()
        if user and user[2] == data['password']:
            return jsonify({
                "status": "success",
                "user": {"name": user[0], "role": user[1]},
                "token": "fake-token"
            })
        return jsonify({"detail": "Sai tài khoản hoặc mật khẩu"}), 401
    finally:
        db.close()

# --- THỐNG KÊ ---
@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    db = SessionLocal()
    try:
        user_count = db.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
        try:
            paper_count = db.execute(text("SELECT COUNT(*) FROM papers")).scalar() or 0
        except:
            paper_count = 0 

        recent = db.execute(text("""
            SELECT full_name, role, created_at 
            FROM users 
            ORDER BY user_id DESC LIMIT 5
        """)).fetchall()

        return jsonify({
            "user_count": user_count,
            "paper_count": paper_count,
            "conf_count": 0,
            "activities": [
                {
                    "name": r[0], 
                    "role": r[1].upper() if r[1] else "USER", 
                    "action": "Vừa tham gia", 
                    "time": human_time_diff(r[2]) 
                } for r in recent
            ]
        })
    finally:
        db.close()

# --- QUẢN LÝ NGƯỜI DÙNG ---
@app.route('/api/admin/users', methods=['GET'])
def get_admin_manage_users():
    db = SessionLocal()
    try:
        users = db.execute(text("SELECT user_id, full_name, email, role FROM users ORDER BY user_id ASC")).fetchall()
        return jsonify([
            {"id": r[0], "name": r[1], "email": r[2], "role": r[3]} for r in users
        ])
    finally:
        db.close()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)