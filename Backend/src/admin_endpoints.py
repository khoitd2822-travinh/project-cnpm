# src/admin_endpoints.py
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import text
# Import kết nối database
from infrastructure.databases.postgresql import SessionLocal 

# Tạo một "cổng phụ" cho Admin
admin_router = Blueprint('admin', __name__)

# Helper để lấy DB session
def get_db():
    db = SessionLocal()
    return db

# Helper tính thời gian
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

# 0. API thống kê tổng quan
@admin_router.route('/stats', methods=['GET'])
def get_admin_stats():
    db = get_db()
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

# 1. API lấy danh sách User để hiện lên Dashboard
@admin_router.route('/admin/users', methods=['GET'])
def get_users():
    db = get_db()
    try:
        users = db.execute(text("SELECT user_id, full_name, email, role FROM users ORDER BY user_id ASC")).fetchall()
        return jsonify([{"id": u[0], "name": u[1], "email": u[2], "role": u[3]} for u in users])
    finally:
        db.close()

# 2. API cập nhật quyền (Khi bạn bấm nút "Sửa" trên Dashboard)
@admin_router.route('/admin/update-role', methods=['POST'])
def update_role():
    data = request.json
    user_id = data.get('user_id')
    new_role = data.get('new_role')
    
    db = get_db()
    try:
        query = text("UPDATE users SET role = :role WHERE user_id = :uid")
        db.execute(query, {"role": new_role, "uid": user_id})
        db.commit()
        return jsonify({"message": "Cập nhật quyền thành công!"})
    except Exception as e:
        db.rollback()
        return jsonify({"detail": str(e)}), 400
    finally:
        db.close()

# 3. API tạo hội nghị (Khi bạn điền Form Setup Conference)
@admin_router.route('/admin/setup-conference', methods=['POST'])
def setup_conf():
    data = request.json
    name = data.get('name')
    deadline = data.get('deadline')
    location = data.get('location', 'Online')
    
    db = get_db()
    try:
        query = text("""
            INSERT INTO conference (name, location, submission_deadline) 
            VALUES (:name, :location, :deadline)
        """)
        db.execute(query, {"name": name, "location": location, "deadline": deadline})
        db.commit()
        return jsonify({"message": "Thiết lập hội nghị thành công!"})
    except Exception as e:
        db.rollback()
        return jsonify({"detail": str(e)}), 400
    finally:
        db.close()

# 4. API lấy nhật ký (Để hiện lên mục View Active Log)
@admin_router.route('/admin/logs', methods=['GET'])
def get_logs():
<<<<<<< HEAD
    db = get_db()
    try:
        logs = db.execute(text("""
            SELECT action, timestamp FROM auditlog ORDER BY timestamp DESC LIMIT 20
        """)).fetchall()
        return jsonify([{"action": l[0], "time": l[1]} for l in logs])
    finally:
        db.close()
=======
    logs = admin_service.get_logs() # Giả sử bạn đã viết hàm này trong service
    return jsonify([{"action": l[0], "time": l[1]} for l in logs])


@app.get("/api/author/papers/{author_id}")
async def get_author_papers(author_id: int, db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT p.paper_id, p.title, p.status, p.score, p.comments
            FROM papers p
            WHERE p.author_id = :aid
            ORDER BY p.paper_id DESC
        """)
        result = db.execute(query, {"aid": author_id}).fetchall()
        
        papers = []
        for r in result:
            papers.append({
                "id": r[0],
                "title": r[1],
                "status": r[2],
                "score": r[3],
                "comment": r[4] if r[4] else ""
            })
        return papers
    except Exception as e:
        print(f"Lỗi: {e}")
        return []
>>>>>>> 4c4953660793c671d9dfe3244d954490d79505d1
