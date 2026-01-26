# src/admin_endpoints.py
from flask import Blueprint, request, jsonify
from .admin_service import AdminService
# Import kết nối database của dự án bạn
from .database import get_db_connection 

# Tạo một "cổng phụ" cho Admin
admin_router = Blueprint('admin', __name__)

# Khởi tạo Service để sử dụng
db_conn = get_db_connection()
admin_service = AdminService(db_conn)

# 1. API lấy danh sách User để hiện lên Dashboard
@admin_router.route('/admin/users', methods=['GET'])
def get_users():
    users = admin_service.view_all_users()
    # Chuyển dữ liệu từ Postgres sang dạng JSON để ReactJS đọc được
    return jsonify([{"id": u[0], "name": u[1], "email": u[2], "role": u[3]} for u in users])

# 2. API cập nhật quyền (Khi bạn bấm nút "Sửa" trên Dashboard)
@admin_router.route('/admin/update-role', methods=['POST'])
def update_role():
    data = request.json
    user_id = data.get('user_id')
    new_role = data.get('new_role')
    
    admin_service.update_user_role(user_id, new_role)
    return jsonify({"message": "Cập nhật quyền thành công!"})

# 3. API tạo hội nghị (Khi bạn điền Form Setup Conference)
@admin_router.route('/admin/setup-conference', methods=['POST'])
def setup_conf():
    data = request.json
    name = data.get('name')
    deadline = data.get('deadline')
    
    admin_service.setup_conference(name, deadline)
    return jsonify({"message": "Thiết lập hội nghị thành công!"})

# 4. API lấy nhật ký (Để hiện lên mục View Active Log)
@admin_router.route('/admin/logs', methods=['GET'])
def get_logs():
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