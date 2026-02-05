import os
import sys
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

# Thêm đường dẫn module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from infrastructure.databases.postgresql import init_postgresql, SessionLocal
from admin_endpoints import admin_router

app = Flask(__name__)
CORS(app)
init_postgresql(app)

<<<<<<< HEAD
# Register admin blueprint
app.register_blueprint(admin_router, url_prefix='/api')
# --- HÀM TÍNH THỜI GIAN ---
=======
>>>>>>> 4c4953660793c671d9dfe3244d954490d79505d1
def human_time_diff(dt):
    if not dt: return "Không rõ"
    now = datetime.now()
    diff = now - dt
    seconds = int(diff.total_seconds())
    if seconds < 60: return f"{seconds} giây trước"
    if seconds < 3600: return f"{seconds // 60} phút trước"
    if seconds < 86400: return f"{seconds // 3600} giờ trước"
    return dt.strftime('%d/%m/%Y')

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
<<<<<<< HEAD
            "fn": data['full_name'],
            "un": data.get('username') or data['email'],
            "em": data['email'],
            "pw": generate_password_hash(data['password']),
            "rl": data['role'],
=======
            "fn": data['full_name'], 
            "un": data['email'], # FE đang dùng email làm username
            "em": data['email'],
            "pw": data['password'], 
            "rl": data['role'].lower(), # Lưu role chữ thường cho đồng bộ
>>>>>>> 4c4953660793c671d9dfe3244d954490d79505d1
            "ca": datetime.now()
        })
        db.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"detail": "Email đã tồn tại hoặc lỗi hệ thống"}), 400
    finally:
        db.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    db = SessionLocal()
    try:
<<<<<<< HEAD
        query = text("SELECT full_name, role, password FROM users WHERE email = :em")
        user = db.execute(query, {"em": data['username']}).fetchone()
        if user and check_password_hash(user[2], data['password']):
=======
        # Lấy đầy đủ thông tin để kiểm tra
        query = text("SELECT user_id, full_name, role, password FROM users WHERE email = :em")
        user = db.execute(query, {"em": data.get('username')}).fetchone() # data['username'] của FE gửi lên là email
        
        if user and str(user[3]) == str(data.get('password')):
>>>>>>> 4c4953660793c671d9dfe3244d954490d79505d1
            return jsonify({
                "status": "success",
                "user": {
                    "id": int(user[0]), # Đảm bảo là kiểu INT
                    "name": user[1], 
                    "role": user[2].lower() # Chuyển về chữ thường để FE dễ so sánh
                },
                "token": "fake-token"
            })
        return jsonify({"detail": "Sai tài khoản hoặc mật khẩu"}), 401
    finally:
        db.close()

<<<<<<< HEAD
# --- ROOT ENDPOINT ---
@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "Backend is running"})
=======
@app.route('/api/author/submit', methods=['POST', 'OPTIONS'])
def submit_paper():
    if request.method == 'OPTIONS': return jsonify({"status": "ok"}), 200
    data = request.json
    db = SessionLocal()
    try:
        # CHỈNH SỬA: Ép kiểu ID và bắt lỗi undefined
        u_id = data.get('author_id')
        if not u_id or str(u_id) == 'undefined':
            return jsonify({"detail": "Lỗi: Bạn cần Đăng xuất và Đăng nhập lại để cập nhật ID!"}), 400

        query = text("""
            INSERT INTO papers (title, abstract, author_id, status) 
            VALUES (:title, :abs, :author, 'Đang chờ')
        """)
        db.execute(query, {
            "title": data.get('title'),
            "abs": data.get('abstract', ''),
            "author": int(u_id)
        })
        db.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    db = SessionLocal()
    try:
        user_count = db.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
        paper_count = db.execute(text("SELECT COUNT(*) FROM papers")).scalar() or 0
        recent = db.execute(text("SELECT full_name, role, created_at FROM users ORDER BY user_id DESC LIMIT 5")).fetchall()
        return jsonify({
            "user_count": user_count, "paper_count": paper_count, "conf_count": 0,
            "activities": [{"name": r[0], "role": r[1].upper(), "action": "Truy cập", "time": human_time_diff(r[2])} for r in recent]
        })
    finally:
        db.close()

@app.route('/api/author/papers/<int:author_id>', methods=['GET'])
def get_author_papers(author_id):
    db = SessionLocal()
    # Phải SELECT thêm score và comments
    query = text("""
        SELECT paper_id, title, status, score, comments 
        FROM papers 
        WHERE author_id = :aid 
        ORDER BY paper_id ASC
    """)
    result = db.execute(query, {"aid": author_id}).fetchall()
    
    return jsonify([{
        "id": r[0],
        "title": r[1],
        "status": r[2],
        "score": r[3],     # Dữ liệu điểm (ví dụ: 9)
        "comments": r[4]   # Dữ liệu nhận xét (ví dụ: cố gắng phát huy)
    } for r in result])

@app.route('/api/admin/users', methods=['GET'])
def get_admin_manage_users():
    db = SessionLocal()
    try:
        # Lấy dữ liệu từ bảng users
        query = text("SELECT user_id, full_name, email, role FROM users ORDER BY user_id ASC")
        users = db.execute(query).fetchall()
        
        # CHỈNH SỬA CẨN THẬN: 
        # Mình sẽ trả về cả 'name' và 'full_name' để chắc chắn Frontend nhận được
        data = []
        for r in users:
            data.append({
                "id": r[0],
                "name": r[1],        # Thử trường này
                "full_name": r[1],   # Hoặc trường này
                "email": r[2],
                "role": r[3].upper() if r[3] else "AUTHOR"
            })
            
        return jsonify(data), 200
    except Exception as e:
        print(f"Lỗi danh sách người dùng: {e}")
        return jsonify([]), 500
    finally:
        db.close()
>>>>>>> 4c4953660793c671d9dfe3244d954490d79505d1


# --- 4. CHAIR API (Điều phối & Phân công) ---

@app.route('/api/chair/papers', methods=['GET'])
def get_chair_papers():
    db = SessionLocal()
    try:
        # Lấy bài báo kèm tên tác giả (JOIN với bảng users)
        query = text("""
            SELECT p.paper_id, p.title, u.full_name, p.reviewer_id
            FROM papers p
            JOIN users u ON p.author_id = u.user_id
            ORDER BY p.paper_id ASC
        """)
        result = db.execute(query).fetchall()
        
        papers = []
        for r in result:
            # Trả về nhiều tên biến (author, author_name, name) để chắc chắn khớp với FE
            papers.append({
                "id": r[0],
                "title": r[1],
                "author": r[2],       # Frontend có thể dùng cái này
                "author_name": r[2],  # Hoặc cái này
                "name": r[2],         # Hoặc cái này
                "reviewer_id": r[3]
            })
        return jsonify(papers), 200
    except Exception as e:
        print(f"Lỗi Chair Papers: {e}")
        return jsonify([]), 500
    finally:
        db.close()

@app.route('/api/chair/assign', methods=['POST'])
def assign_reviewer():
    data = request.json
    db = SessionLocal()
    try:
        # Cập nhật reviewer_id cho bài báo
        query = text("UPDATE papers SET reviewer_id = :rid WHERE paper_id = :pid")
        db.execute(query, {"rid": data.get('reviewer_id'), "pid": data.get('paper_id')})
        db.commit()
        return jsonify({"status": "success", "message": "Phân công thành công!"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()

@app.route('/api/reviewers', methods=['GET'])
def get_all_reviewers():
    db = SessionLocal()
    try:
        # Lấy danh sách những người có quyền là 'reviewer' để Chair chọn
        query = text("SELECT user_id, full_name FROM users WHERE role = 'reviewer'")
        result = db.execute(query).fetchall()
        return jsonify([{"id": r[0], "name": r[1]} for r in result]), 200
    finally:
        db.close()

@app.route('/api/reviewer/submit-review', methods=['POST'])
def submit_review():
    data = request.json
    db = SessionLocal()
    try:
        query = text("""
            UPDATE papers 
            SET score = :score, 
                comments = :comment, 
                status = 'Đã chấm'
            WHERE paper_id = :pid AND reviewer_id = :rid
        """)
        db.execute(query, {
            "score": float(data.get('score', 0)),
            "comment": data.get('comment', ''),
            "pid": data.get('paper_id'),
            "rid": data.get('reviewer_id', 0)  # Thêm reviewer_id
        })
        db.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        db.rollback()
        print(f"Lỗi submit review: {e}")
        return jsonify({"detail": str(e)}), 500
    finally:
        db.close()

@app.route('/api/reviewer/papers/<int:reviewer_id>', methods=['GET'])
def get_assigned_papers(reviewer_id):
    db = SessionLocal()
    try:
        # In ra màn hình đen (Terminal) để xem ID thực tế là bao nhiêu
        print(f"DEBUG: Reviewer đang yêu cầu bài cho ID = {reviewer_id}")
        
        query = text("""
            SELECT p.paper_id, p.title, u.full_name as author_name, p.status
            FROM papers p
            JOIN users u ON p.author_id = u.user_id
            WHERE p.reviewer_id = :rid
        """)
        result = db.execute(query, {"rid": reviewer_id}).fetchall()
        
        return jsonify([{"id": r[0], "title": r[1], "author_name": r[2], "status": r[3]} for r in result]), 200
    finally:
        db.close()
        
@app.route('/api/author/papers/<int:author_id>', methods=['GET'])
def get_author_results(author_id):
    db = SessionLocal()
    try:
        query = text("""
            SELECT paper_id, title, status, score, comments 
            FROM papers 
            WHERE author_id = :aid
        """)
        result = db.execute(query, {"aid": author_id}).fetchall()
        return jsonify([
            {
                "id": r[0], "title": r[1], "status": r[2], 
                "score": r[3], "comment": r[4]  # Thay comments thành comment
            } for r in result
        ]), 200
    finally:
        db.close()



# ...existing code...

@app.route('/api/reviewer/tasks/<int:reviewer_id>', methods=['GET'])
def get_reviewer_tasks(reviewer_id):
    db = SessionLocal()
    try:
        # Lấy bài báo được phân công cho reviewer này
        query = text("""
            SELECT p.paper_id, p.title, u.full_name as author, 
                   p.status, COALESCE(p.score, 0) as score, 
                   COALESCE(p.comments, '') as comment
            FROM papers p
            JOIN users u ON p.author_id = u.user_id
            WHERE p.reviewer_id = :rid
            ORDER BY p.paper_id ASC
        """)
        result = db.execute(query, {"rid": reviewer_id}).fetchall()
        
        papers = []
        for r in result:
            papers.append({
                "id": r[0],
                "title": r[1],
                "author": r[2],
                "status": r[3] if r[3] in ['Đã chấm', 'pending'] else 'Chờ chấm',
                "score": r[4],
                "comment": r[5]
            })
        
        return jsonify(papers), 200
    except Exception as e:
        print(f"Lỗi reviewer tasks: {e}")
        return jsonify([]), 500
    finally:
        db.close()

# ...existing code...

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)