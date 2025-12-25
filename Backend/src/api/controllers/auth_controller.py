from flask import Blueprint, request, jsonify

# Tạo Blueprint để Flask nhận diện route
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    # Bước 2: Lấy email/pass từ trình duyệt gửi lên
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Bước 3: Gọi AuthService để xử lý logic
    # Lưu ý: Trong app.py bạn sẽ khởi tạo auth_service này
    result = auth_service.login(email, password)

    if result:
        # Bước 15: Trả về 200 OK và Role để React điều hướng
        return jsonify(result), 200
    else:
        # Bước 13: Trả về 401 nếu sai mật khẩu
        return jsonify({"message": "Invalid email or password"}), 401