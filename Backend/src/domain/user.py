class User:
    def __init__(self, user_id, username, password_hash, role):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role