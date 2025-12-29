from flask import Blueprint, request, jsonify

# Tạo Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    from app import auth_service # Import bên trong hàm để tránh lỗi vòng lặp
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    result = auth_service.login(email, password)

    if result:
        return jsonify(result), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401
    
@auth_bp.route('/register', methods=['POST'])
def register():
    from app import auth_service # BẮT BUỘC PHẢI CÓ DÒNG NÀY Ở ĐÂY
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    # Gọi service xử lý
    result = auth_service.register(email, password, full_name)

    if result:
        return jsonify({"message": "Registration successful"}), 201
    else:
        return jsonify({"message": "Email already exists"}), 400

@auth_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Auth API hoạt động!"}), 200