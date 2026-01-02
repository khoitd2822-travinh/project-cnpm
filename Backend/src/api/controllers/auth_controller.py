from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Lấy thêm trường 'role' từ dữ liệu gửi lên, mặc định là 'author'
    role_requested = data.get('role', 'author') 
    
    auth_service = auth_bp.auth_service_factory()
    
    # Truyền role_requested vào service
    success = auth_service.register(
        email=data.get('email'),
        password=data.get('password'),
        full_name=data.get('full_name'),
        role=role_requested 
    )
    
    if success:
        return jsonify({"message": "User registered successfully"}), 201
    return jsonify({"error": "Register failed"}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    print(">>> LOGIN API HIT")
    try:
        data = request.get_json()
        print("DATA:", data)

        auth_service = auth_bp.auth_service_factory()

        # result lúc này là một Object User
        user = auth_service.login(
            data.get("email"),
            data.get("password")
        )

        print("RESULT OBJECT:", user)

        if user:
            # FIX LỖI Ở ĐÂY: Trả về từng trường dữ liệu thay vì trả về cả Object user
            return jsonify({
                "message": "Login successful",
                "token": "fake-jwt-token-for-now", 
                "role": getattr(user, 'role', 'author'), # Lấy role từ object user
                "full_name": getattr(user, 'full_name', ''),
                "email": getattr(user, 'email', '')
            }), 200
            
        return jsonify({"message": "Email hoặc mật khẩu không đúng"}), 401
        
    except Exception as e:
        print(f"🔥 CRITICAL ERROR IN LOGIN: {e}")
        return jsonify({"message": "Lỗi hệ thống nội bộ"}), 500