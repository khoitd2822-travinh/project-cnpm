class User:
    def __init__(self, user_id, username, password, role): # <-- Đổi password_hash thành password
        self.user_id = user_id
        self.username = username
        self.password = password  # <-- Đổi ở đây nữa
        self.role = role