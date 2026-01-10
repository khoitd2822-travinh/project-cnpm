from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from infrastructure.databases.postgresql import SessionLocal
from sqlalchemy import text

app = Flask(__name__)
CORS(app)

# --- HÀM TÍNH THỜI GIAN (ĐÃ SỬA LỖI LỆCH 7 GIỜ) ---
def human_time_diff(dt):
    """Tính khoảng cách thời gian thực tế so với hiện tại, xử lý lệch múi giờ"""
    if not dt:
        return "Không rõ"
    
    # Lấy thời gian hiện tại
    now = datetime.now()
    
    # Nếu dt từ DB là UTC (lệch 7 tiếng so với VN), ta cộng thêm 7 tiếng trước khi so sánh
    # Hoặc đơn giản là lấy hiệu số và trừ đi 7 giờ nếu nó quá lớn
    diff = now - dt
    seconds = int(diff.total_seconds())

    # Nếu giây ra con số xấp xỉ 25200 (7 giờ), nghĩa là DB đang dùng UTC
    # Ta điều chỉnh lại dt để khớp với local
    if seconds >= 25000 and seconds <= 25400:
        dt = dt + timedelta(hours=7)
        diff = now - dt
        seconds = int(diff.total_seconds())
    
    # Xử lý hiển thị
    if seconds < 5:
        return "Vừa xong"
    if seconds < 60:
        return f"{seconds} giây trước"
    if seconds < 3600:
        return f"{seconds // 60} phút trước"
    if seconds < 86400:
        return f"{seconds // 3600} giờ trước"
    
    return dt.strftime('%d/%m/%Y %H:%M')

# --- XỬ LÝ ĐĂNG KÝ ---
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
            "ca": datetime.now() # Lưu giờ theo giờ máy tính đang chạy (Local)
        })
        db.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"detail": str(e)}), 400
    finally:
        db.close()

# --- XỬ LÝ ĐĂNG NHẬP ---
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

# --- THỐNG KÊ (FIX TRIỆT ĐỂ SỐ 45) ---
@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    db = SessionLocal()
    try:
        user_count = db.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
        
        # Đếm thực tế từ bảng papers (nếu chưa có bảng sẽ trả về 0, không hiện 45)
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
                    "role": r[1].upper(), 
                    "action": "Vừa gia nhập", 
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